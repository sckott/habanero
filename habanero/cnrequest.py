import requests
import json
import warnings

from .habanero_utils import switch_classes, make_ua
from .cn_formats import *


def CNRequest(url, ids, format=None, style=None, locale=None, **kwargs):
    if not isinstance(ids, (str, list)):
        raise TypeError("'ids' must be a str or list of str's")
    if isinstance(ids, list):
        if not all([isinstance(z, str) for z in ids]):
            raise TypeError("'ids' must be a str or list of all str's")
    should_split = False
    try:
        # Python 2
        if isinstance(ids, (str, unicode)):
            should_split = True
    except NameError:
        # Python 3
        if isinstance(ids, str):
            should_split = True
    if should_split:
        ids = ids.split()

    if len(ids) == 1:
        return make_request(url, ids[0], format, style, locale, fail=True, **kwargs)
    else:
        coll = []
        for i in range(len(ids)):
            tt = make_request(url, ids[i], format, style, locale, fail=False, **kwargs)
            coll.append(tt)

        if len(coll) == 1:
            coll = coll[0]
        return coll


def make_request(url, ids, format, style, locale, fail, **kwargs):
    type = cn_format_headers[format]

    if format == "citeproc-json":
        url = "http://api.crossref.org/works/" + ids + "/" + type
    else:
        if format == "text":
            type = type + "; style = " + style + "; locale = " + locale
        url = url + "/" + ids

    htype = {"Accept": type}
    head = dict(make_ua(), **htype)
    r = requests.get(url, headers=head, allow_redirects=True, **kwargs)

    # Raise an HTTPError if the status code of the response is 4XX or 5XX
    # or warn if fail=False
    if not r.ok:
        if fail:
            r.raise_for_status()
        else:
            mssg = "%s: %s" % (r.status_code, r.url)
            warnings.warn(mssg)
            return None

    # set encoding
    r.encoding = "UTF-8"
    return r.text
