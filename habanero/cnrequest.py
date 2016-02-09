import requests
import json

from .habanero_utils import switch_classes,make_ua
from .cn_formats import *

def CNRequest(url, ids = None, format = None, style = None,
        locale = None, **kwargs):

  if(ids.__class__.__name__ == "str"):
    ids = ids.split()
  if(ids.__class__.__name__ == "int"):
    ids = [ids]

  if(len(ids) == 1):
    return make_request(url, ids[0], format, style, locale, **kwargs)
  else:
    coll = []
    for i in range(len(ids)):
      tt = make_request(url, ids[i], format, style, locale, **kwargs)
      coll.append(tt)

    if len(coll) == 1:
      coll = coll[0]
    return coll

def make_request(url, ids, format, style, locale, **kwargs):
  type = cn_format_headers[format]
  htype = {'Accept': type}
  head = dict(make_ua(), **htype)

  if format == "citeproc-json":
    url = "http://api.crossref.org/works/" + ids + "/" + type
    return requests.get(url, headers = head, allow_redirects = True, **kwargs).text
  else:
    if format == "text":
      type = type + "; style = " + style + "; locale = " + locale
    url = url + "/" + ids
    return requests.get(url, headers = head, allow_redirects = True, **kwargs).text

