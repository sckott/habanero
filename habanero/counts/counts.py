import warnings
from typing import Any
from xml.dom import minidom
from xml.dom.minidom import Text

import httpx2

from ..habanero_utils import make_ua

OPENURL_BASE: str = "https://doi.crossref.org/openurl"


def citation_count(
    doi: str,
    email: str | None = None,
    key: str | None = None,
    **kwargs,
) -> int:
    """
    Get a citation count with a DOI

    :param doi: DOI, digital object identifier. required.
    :param email: your email address. required.
    :param key: Deprecated, use `email` instead.

    See https://www.crossref.org/documentation/retrieve-metadata/openurl/
    for more info on this Crossref API service.

    Usage::

        from habanero import counts
        counts.citation_count(doi = "10.1371/journal.pone.0042793")
        counts.citation_count(doi = "10.1016/j.fbr.2012.01.001")

        # DOI not found, correctly raises ValueError
        counts.citation_count(doi = "10.1016/j.fbr.2012")
    """
    if key is not None:
        warnings.warn(
            "the `key` parameter is deprecated, use `email` instead",
            DeprecationWarning,
            stacklevel=2,
        )
        if email is None:
            email = key

    if not email:
        raise ValueError("`email` is required")

    args = {"id": "doi:" + doi, "pid": email, "noredirect": True, "format": "unixsd"}
    new_args: dict[str, Any] = {k: v for k, v in args.items() if v}
    res = httpx2.get(OPENURL_BASE, params=new_args, headers=make_ua(), **kwargs)
    xmldoc = minidom.parseString(res.content)
    for item in xmldoc.getElementsByTagName("crm-item"):
        if item.getAttribute("name") == "citedby-count":
            text = "".join(n.data for n in item.childNodes if isinstance(n, Text))
            return int(text)

    raise ValueError(f"citedby-count not found for DOI: {doi}")
