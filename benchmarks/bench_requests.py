"""Benchmark: time Crossref requests with and without connection reuse

Makes REAL requests to https://api.crossref.org, so run it sparingly. Modes are
interleaved within each round so that network/API drift hits all modes equally.

Modes
-----
default  ``Crossref()`` as shipped: one pooled ``httpx2.Client`` per object,
         reused for every request (with retries on transient failures)
nopool   ``Crossref(client=<shim>)`` where the shim calls the module-level
         ``httpx2.get`` for every request, i.e., one new connection (and TLS
         handshake) per request. This reproduces the behavior from before
         ``Crossref`` held an ``httpx2.Client``. Retries still apply, as they
         do for any ``client`` passed in

Usage::

    python benchmarks/bench_requests.py --modes default
    python benchmarks/bench_requests.py --modes default nopool --rounds 5
    python benchmarks/bench_requests.py --mailto you@example.com --json out.json
"""

import argparse
import json
import statistics
import time

import httpx2

from habanero import Crossref


class PerRequestClient:
    """Mimics the old behavior: a brand new connection for every request"""

    def get(self, url, **kwargs):
        return httpx2.get(url, **kwargs)

    def close(self):
        pass


def make_crossref(mode: str, mailto: str | None) -> Crossref:
    if mode == "default":
        return Crossref(mailto=mailto)
    if mode == "nopool":
        return Crossref(mailto=mailto, client=PerRequestClient())  # type: ignore[arg-type]
    raise ValueError(f"unknown mode: {mode}")


def scenario_by_ids(cr: Crossref, dois: list[str]) -> int:
    """One GET per DOI, sequentially"""
    cr.works(ids=dois)
    return len(dois)


def scenario_cursor(cr: Crossref, dois: list[str]) -> int:
    """Deep paging: 5 pages of 50 items"""
    res = cr.works(
        query="ecology", cursor="*", limit=50, cursor_max=250, select="DOI,title"
    )
    # one response per page when paging; a single dict if everything fit in one
    return len(res) if isinstance(res, list) else 1


SCENARIOS = {"by_ids": scenario_by_ids, "cursor": scenario_cursor}


def timed(mode, mailto, scenario, dois):
    # the client is created lazily, so its construction and first connection
    # are inside the timed region for every mode
    with make_crossref(mode, mailto) as cr:
        start = time.perf_counter()
        n = SCENARIOS[scenario](cr, dois)
        elapsed = time.perf_counter() - start
    return elapsed, n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modes", nargs="+", default=["default"])
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--scenarios", nargs="+", default=list(SCENARIOS))
    ap.add_argument("--n-dois", type=int, default=15)
    ap.add_argument("--mailto", default=None)
    ap.add_argument(
        "--pause",
        type=float,
        default=3.0,
        help="seconds to sleep between timed runs (not timed), to stay under "
        "Crossref's rate limit",
    )
    ap.add_argument("--json", default=None, help="write raw timings to this path")
    args = ap.parse_args()

    # fix the DOI list once so every mode requests the same things
    with Crossref(mailto=args.mailto) as cr:
        res = cr.works(query="ecology", limit=args.n_dois, select="DOI")

    dois = [w["DOI"] for w in res["message"]["items"]]
    print(f"{len(dois)} DOIs; modes={args.modes}; rounds={args.rounds} (+1 warmup)\n")

    results: dict[str, dict[str, list[float]]] = {
        s: {m: [] for m in args.modes} for s in args.scenarios
    }
    counts: dict[str, int] = {}

    for rnd in range(args.rounds + 1):
        # rotate the order each round so no mode is always first
        order = (
            args.modes[rnd % len(args.modes) :] + args.modes[: rnd % len(args.modes)]
        )
        for scenario in args.scenarios:
            for mode in order:
                time.sleep(args.pause)
                elapsed, n = timed(mode, args.mailto, scenario, dois)
                counts[scenario] = n
                if rnd > 0:  # round 0 is warmup (DNS, caches)
                    results[scenario][mode].append(elapsed)

    for scenario, per_mode in results.items():
        print(f"{scenario} ({counts[scenario]} requests per run)")
        for mode, ts in per_mode.items():
            print(
                f"  {mode:8s} median={statistics.median(ts):6.2f}s "
                f"mean={statistics.mean(ts):6.2f}s min={min(ts):6.2f}s "
                f"per-request(median)={1000 * statistics.median(ts) / counts[scenario]:6.0f}ms"
            )
        if "default" in per_mode and "nopool" in per_mode:
            d, p = (
                statistics.median(per_mode["default"]),
                statistics.median(per_mode["nopool"]),
            )
            print(f"  -> default is {p / d:.2f}x as fast as nopool (median)")
        print()

    if args.json:
        with open(args.json, "w") as f:
            json.dump({"counts": counts, "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
