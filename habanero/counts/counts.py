from typing import Any
from xml.dom import minidom

import requests

from ..habanero_utils import make_ua


def citation_count(
    doi: str,
    url: str = "http://www.crossref.org/openurl/",
    key: str = "cboettig@ropensci.org",
    **kwargs
) -> int:
    """
    Get a citation count with a DOI

    :param doi: DOI, digital object identifier
    :param url: the API url for the function (should be left to default)
    :param key: your API key

    See http://labs.crossref.org/openurl/ for more info on this Crossref API service.

    Usage::

        from habanero import counts
        counts.citation_count(doi = "10.1371/journal.pone.0042793")
        counts.citation_count(doi = "10.1016/j.fbr.2012.01.001")
        # DOI not found
        ## FIXME
        counts.citation_count(doi = "10.1016/j.fbr.2012")
    """
    args = {"id": "doi:" + doi, "pid": key, "noredirect": True}
    new_args: dict[str, Any] = dict((k, v) for k, v in args.items() if v)
    res = requests.get(url, params=new_args, headers=make_ua(), **kwargs)
    xmldoc = minidom.parseString(res.content)
    val = xmldoc.getElementsByTagName("query")[0].attributes["fl_count"].value
    return int(str(val))
