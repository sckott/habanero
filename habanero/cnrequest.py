import warnings
from typing import Literal, overload

import httpx2
from packaging.version import Version

from .cn_formats import cn_format_headers
from .habanero_utils import make_ua

try:
    import bibtexparser  # type: ignore
except ImportError:
    _has_bibtexparser = False
else:
    _has_bibtexparser = True


def CNRequest(
    url,
    ids,
    citation_format: str = "bibtex",
    style: str = "apa",
    locale: str = "en-US",
    **kwargs,
) -> str | list[str | None]:
    if not isinstance(ids, (str, list)):
        raise TypeError("'ids' must be a str or list of str's")
    if isinstance(ids, list) and not all(isinstance(z, str) for z in ids):
        raise TypeError("'ids' must be a str or list of all str's")

    should_split = isinstance(ids, str)
    if should_split:
        ids = ids.split()

    if len(ids) == 1:
        return make_request(
            url,
            ids[0],
            fail=True,
            for_mat=citation_format,
            style=style,
            locale=locale,
            **kwargs,
        )
    else:
        coll = []
        for i in range(len(ids)):
            tt = make_request(
                url,
                ids[i],
                fail=False,
                for_mat=citation_format,
                style=style,
                locale=locale,
                **kwargs,
            )
            coll.append(tt)

        return coll


@overload
def make_request(
    url: str,
    ids: str,
    fail: Literal[True],
    for_mat: str = "bibtex",
    style: str = "apa",
    locale: str = "en-US",
    **kwargs,
) -> str: ...


@overload
def make_request(
    url: str,
    ids: str,
    fail: Literal[False],
    for_mat: str = "bibtex",
    style: str = "apa",
    locale: str = "en-US",
    **kwargs,
) -> str | None: ...


def make_request(
    url: str,
    ids: str,
    fail: bool,
    for_mat: str = "bibtex",
    style: str = "apa",
    locale: str = "en-US",
    **kwargs,
) -> str | None:
    ty_pe = cn_format_headers[for_mat]

    if for_mat == "citeproc-json":
        url = f"https://api.crossref.org/works/{ids}/{ty_pe}"
    else:
        if for_mat == "text":
            ty_pe = ty_pe + "; style = " + style + "; locale = " + locale
        url = f"{url}/{ids}"

    htype = {"Accept": ty_pe}
    head = dict(make_ua(), **htype)
    r = httpx2.get(url, headers=head, follow_redirects=True, **kwargs)

    # Raise an HTTPError if the status code of the response is 4XX or 5XX
    # or warn if fail=False
    if not r.is_success:
        if fail:
            r.raise_for_status()
        else:
            mssg = f"{r.status_code}: {r.url}"
            warnings.warn(mssg, stacklevel=2)
            return None

    r.encoding = "UTF-8"
    text = r.text
    if for_mat == "bibtex" and _has_bibtexparser:
        bibtexparser_ver = Version(bibtexparser.__version__)
        if bibtexparser_ver.major >= 2:
            text = fix_bibtex(text)
    return text


def fix_bibtex(x: str) -> str:
    parsed = bibtexparser.parse_string(x)
    return bibtexparser.write_string(parsed)
