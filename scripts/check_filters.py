"""Check Crossref filters against the filter dictionaries in habanero

Makes REAL requests to https://api.crossref.org for the ``/works``,
``/members`` and ``/funders`` routes, sent through ``Crossref.works``,
``Crossref.members`` and ``Crossref.funders`` so filter names go through the
same conversion as user code (e.g., ``license_url`` -> ``license.url``).

Two checks per route:

1. One tiny request (``limit=0``) per filter in the route's dictionary
   (``works_filter_details``, ``members_filter_details``,
   ``funders_filter_details``). Crossref answers an unknown filter with HTTP
   400 and a message like "Filter X specified but there is no such filter for
   this route". Those are reported as UNAVAILABLE. Any other failure (e.g., a
   400 caused by a bad sample value) is reported as OTHER ERROR.
2. One request with a made-up filter name. The 400 response lists every
   filter the route accepts; any that are missing from the dictionary are
   reported as MISSING from the dictionary.

``KNOWN_UNAVAILABLE`` and ``KNOWN_MISSING`` hold filters we already know
about, so they don't cause a failure. The exit code is:

- 0: nothing new
- 1: a new UNAVAILABLE or MISSING filter, or any OTHER ERROR

It also notes (without failing) entries in those two lists that are no longer
needed, so the lists can be trimmed.

Run daily by ``.github/workflows/check-filters.yml``.

Usage::

    python scripts/check_filters.py
    python scripts/check_filters.py --routes works members --delay 0.5
    python scripts/check_filters.py --mailto you@example.com
"""

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass, field

from habanero import Crossref
from habanero.crossref.filters import (
    funders_filter_details,
    members_filter_details,
    works_filter_details,
)
from habanero.exceptions import RequestError

Value = str | int | bool

FILTER_DETAILS: dict[str, dict[str, dict]] = {
    "works": works_filter_details,
    "members": members_filter_details,
    "funders": funders_filter_details,
}

# filters that Crossref is known to reject on a route; remove one once it works,
# or remove it from the dictionary
KNOWN_UNAVAILABLE: dict[str, set[str]] = {
    "works": {"has_description"},
    "members": set(),
    "funders": set(),
}

# filters Crossref accepts on a route but that aren't in our dictionary yet,
# written the way they'd be named in the dictionary (underscores)
KNOWN_MISSING: dict[str, set[str]] = {
    "works": set(),
    "members": set(),
    "funders": set(),
}

# sample values, used when a filter's name/`possible_values` isn't enough to pick one
VALUE_OVERRIDES: dict[str, dict[str, Value]] = {
    "works": {
        "funder": "10.13039/100000001",
        "funder_doi_asserted_by": "crossref",
        "prefix": "10.1016",
        "member": 78,
        "license_url": "http://creativecommons.org/licenses/by/4.0/",
        "license_version": "vor",
        "license_delay": 0,
        "full_text_version": "vor",
        "full_text_type": "application/pdf",
        "full_text_application": "text-mining",
        "archive": "Portico",
        "orcid": "http://orcid.org/0000-0002-8442-8025",
        "ror_id": "https://ror.org/02mhbdp94",
        "isbn": "9780262033848",
        "issn": "1097-4547",
        "type": "journal-article",
        "type_name": "Journal Article",
        "doi": "10.5555/12345678",
        "updates": "10.5555/12345678",
        "update_type": "correction",
        "container_title": "Nature",
        "award_number": "CBET-0756451",
        "award_funder": "10.13039/100000001",
        "gte_award_amount": 1000,
        "lte_award_amount": 100000,
        "assertion_group": "ExaMplEGroup",
        "assertion": "orcid",
        "alternative_id": "abc123",
        "article_number": "1",
        "group_title": "Biology",
        "clinical_trial_number": "NCT00000000",
        "content_domain": "example.com",
        "relation_type": "is-referenced-by",
        "relation_object": "10.5555/12345678",
        "relation_object_type": "doi",
    },
    "members": {
        "prefix": "10.1016",
        "backfile_doi_count": 100,
        "current_doi_count": 100,
    },
    "funders": {
        "location": "France",
    },
}

# a name Crossref won't have, used to provoke the "Valid filters ..." message
BOGUS_FILTER = "habanero_bogus_filter"

VALID_FILTERS_RE = re.compile(r"Valid filters for this route are:\s*(.+)$", re.DOTALL)


@dataclass
class RouteReport:
    route: str
    ok: list[str] = field(default_factory=list)
    unavailable: dict[str, str] = field(default_factory=dict)  # name -> detail
    other_errors: dict[str, str] = field(default_factory=dict)  # name -> detail
    missing: list[str] = field(default_factory=list)  # valid in API, not in dict

    @property
    def new_unavailable(self) -> list[str]:
        return sorted(set(self.unavailable) - KNOWN_UNAVAILABLE[self.route])

    @property
    def now_working(self) -> list[str]:
        return sorted(KNOWN_UNAVAILABLE[self.route] - set(self.unavailable))

    @property
    def new_missing(self) -> list[str]:
        return sorted(set(self.missing) - KNOWN_MISSING[self.route])

    @property
    def now_in_dictionary(self) -> list[str]:
        return sorted(KNOWN_MISSING[self.route] - set(self.missing))

    @property
    def failed(self) -> bool:
        return bool(self.new_unavailable or self.new_missing or self.other_errors)


def sample_value(route: str, name: str, details: dict) -> Value:
    overrides = VALUE_OVERRIDES[route]
    if name in overrides:
        return overrides[name]
    if name.startswith(("from_", "until_")):
        return "2020-01-01"
    if details["possible_values"] is None:
        return True  # has_* style boolean filters
    raise ValueError(
        f"no sample value for {route} filter {name!r}; add it to VALUE_OVERRIDES"
    )


def call(cr: Crossref, route: str, filters: dict[str, Value]) -> None:
    getattr(cr, route)(filters=filters, limit=0)


def normalize(api_name: str) -> str:
    """API filter name -> dictionary style, e.g., license.url -> license_url"""
    return re.sub(r"[-.]", "_", api_name)


def check_filter(cr: Crossref, route: str, name: str, value: Value) -> tuple[str, str]:
    """Returns (status, detail) where status is OK, UNAVAILABLE or OTHER ERROR"""
    try:
        call(cr, route, {name: value})
    except RequestError as e:
        detail = f"{e.status_code}: {e.error}"
        if e.status_code == 400 and "no such filter" in str(e.error).lower():
            return "UNAVAILABLE", detail
        return "OTHER ERROR", detail
    except Exception as e:  # noqa: BLE001 - network errors, non-JSON bodies, etc.
        return "OTHER ERROR", f"{type(e).__name__}: {e}"
    return "OK", ""


def valid_filters(cr: Crossref, route: str) -> set[str]:
    """Names of all filters the route accepts, in dictionary style

    Raises ValueError if the API response doesn't have the expected list
    """
    try:
        call(cr, route, {BOGUS_FILTER: "x"})
    except RequestError as e:
        match = VALID_FILTERS_RE.search(str(e.error))
        if match:
            names = (n.strip() for n in match.group(1).split(","))
            return {normalize(n) for n in names if n}
        raise ValueError(f"unexpected error message: {e}") from e
    raise ValueError("request with a made-up filter unexpectedly succeeded")


def check_route(cr: Crossref, route: str, delay: float) -> RouteReport:
    report = RouteReport(route)
    details = FILTER_DETAILS[route]

    for name, d in details.items():
        value = sample_value(route, name, d)
        status, detail = check_filter(cr, route, name, value)
        print(f"{status:<12} {route}: {name} = {value}")
        if status == "OK":
            report.ok.append(name)
        elif status == "UNAVAILABLE":
            report.unavailable[name] = detail
        else:
            report.other_errors[name] = detail
        time.sleep(delay)

    try:
        api_names = valid_filters(cr, route)
    except (ValueError, RequestError) as e:
        report.other_errors["<valid filters list>"] = str(e)
        print(f"OTHER ERROR  {route}: could not get valid filters list: {e}")
    else:
        report.missing = sorted(api_names - set(details))
        for name in report.missing:
            print(f"MISSING      {route}: {name} (valid in API, not in dictionary)")
    return report


def write_summary(lines: list[str]) -> None:
    """Append markdown to the GitHub Actions job summary, if running there"""
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a") as f:
            f.write("\n".join(lines) + "\n")


def print_report(r: RouteReport) -> None:
    print(f"\n{r.route}: {len(r.ok)} OK, {len(r.unavailable)} unavailable, ", end="")
    print(f"{len(r.other_errors)} other errors, {len(r.missing)} missing")
    for title, rows in (
        ("UNAVAILABLE", r.unavailable),
        ("OTHER ERROR", r.other_errors),
    ):
        for name, detail in rows.items():
            print(f"  {title}: {name}\n      {detail[:300]}")
    for name in r.missing:
        print(f"  MISSING: {name}")


def summary_lines(reports: list[RouteReport]) -> list[str]:
    lines = ["## Crossref filter check", ""]
    lines += [
        "| route | OK | unavailable | other errors | missing |",
        "|---|---|---|---|---|",
    ]
    for r in reports:
        lines.append(
            f"| {r.route} | {len(r.ok)} | {len(r.unavailable)} | "
            f"{len(r.other_errors)} | {len(r.missing)} |"
        )
    sections = (
        ("Newly unavailable filters", "new_unavailable"),
        ("Valid in the API but missing from the dictionary", "new_missing"),
        ("Other errors (see log for details)", None),
        ("In KNOWN_UNAVAILABLE but now working", "now_working"),
        ("In KNOWN_MISSING but now in the dictionary", "now_in_dictionary"),
    )
    for title, attr in sections:
        items = [
            f"- `{r.route}`: `{n}`"
            for r in reports
            for n in (sorted(r.other_errors) if attr is None else getattr(r, attr))
        ]
        if items:
            lines += ["", f"### {title}", "", *items]
    return lines


def print_annotations(reports: list[RouteReport]) -> None:
    """GitHub workflow commands: show up as annotations on the run"""
    for r in reports:
        for n in r.new_unavailable:
            print(
                f"::error title=Filter unavailable::{r.route} filter {n!r} was rejected by Crossref"
            )
        for n in r.new_missing:
            print(
                f"::error title=Filter missing from dictionary::{r.route} filter {n!r} is valid in the API but not in the dictionary"
            )
        for n in r.other_errors:
            print(
                f"::error title=Filter check failed::{r.route} filter {n!r} failed with an unexpected error"
            )
        for n in r.now_working:
            print(
                f"::notice title=Filter works again::{r.route} filter {n!r} is in KNOWN_UNAVAILABLE but now works"
            )
        for n in r.now_in_dictionary:
            print(
                f"::notice title=Stale KNOWN_MISSING entry::{r.route} filter {n!r} is in KNOWN_MISSING but not missing"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--mailto",
        default=os.environ.get("CROSSREF_MAILTO") or None,
        help="email for Crossref's polite pool (default: $CROSSREF_MAILTO)",
    )
    parser.add_argument(
        "--routes",
        nargs="+",
        choices=list(FILTER_DETAILS),
        default=list(FILTER_DETAILS),
        help="routes to check (default: all)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.2, help="seconds between requests"
    )
    args = parser.parse_args()

    with Crossref(mailto=args.mailto) as cr:
        reports = [check_route(cr, route, args.delay) for route in args.routes]

    print("\nSummary\n-------", end="")
    for r in reports:
        print_report(r)

    write_summary(summary_lines(reports))
    print_annotations(reports)
    return 1 if any(r.failed for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
