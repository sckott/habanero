import warnings

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


def CNRequest(url, ids, format=None, style=None, locale=None, **kwargs):  # noqa: A002 (format)
    if not isinstance(ids, (str, list)):
        raise TypeError("'ids' must be a str or list of str's")
    if isinstance(ids, list) and not all(isinstance(z, str) for z in ids):
        raise TypeError("'ids' must be a str or list of all str's")

    should_split = isinstance(ids, str)
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


def make_request(url, ids, for_mat, style, locale, fail, **kwargs):
    ty_pe = cn_format_headers[for_mat]

    if for_mat == "citeproc-json":
        url = "http://api.crossref.org/works/" + ids + "/" + ty_pe
    else:
        if for_mat == "text":
            ty_pe = ty_pe + "; style = " + style + "; locale = " + locale
        url = url + "/" + ids

    htype = {"Accept": ty_pe}
    head = dict(make_ua(), **htype)
    r = httpx2.get(url, headers=head, follow_redirects=True, **kwargs)

    # Raise an HTTPError if the status code of the response is 4XX or 5XX
    # or warn if fail=False
    if not r.is_success:
        if fail:
            r.raise_for_status()
        else:
            mssg = "%s: %s" % (r.status_code, r.url)
            warnings.warn(mssg, stacklevel=2)
            return None

    r.encoding = "UTF-8"
    text = r.text
    if for_mat == "bibtex" and _has_bibtexparser:
        bibtexparser_ver = Version(bibtexparser.__version__)
        if bibtexparser_ver.major >= 2:
            text = fix_bibtex(text)
    return text


def fix_bibtex(x):
    parsed = bibtexparser.parse_string(x)
    return bibtexparser.write_string(parsed)
