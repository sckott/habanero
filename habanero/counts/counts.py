import requests
from xml.dom import minidom
from ..habanero_utils import make_ua


def citation_count(
    doi, url="http://www.crossref.org/openurl/", key="cboettig@ropensci.org", **kwargs
):
    """
    Get a citation count with a DOI

    :param doi: [String] DOI, digital object identifier
    :param url: [String] the API url for the function (should be left to default)
    :param keyc: [String] your API key

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
    args = dict((k, v) for k, v in args.items() if v)
    res = requests.get(url, params=args, headers=make_ua(), **kwargs)
    xmldoc = minidom.parseString(res.content)
    val = xmldoc.getElementsByTagName("query")[0].attributes["fl_count"].value
    return int(str(val))
