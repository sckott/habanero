import requests
import json

from .habanero_utils import switch_classes,make_ua
from .cn_formats import *

def CNRequest(url, ids = None, format = None, style = None,
        locale = None, **kwargs):

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

  if isinstance(ids, int):
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

  if format == "citeproc-json":
    url = "http://api.crossref.org/works/" + ids + "/" + type
  else:
    if format == "text":
      type = type + "; style = " + style + "; locale = " + locale
    url = url + "/" + ids

  htype = {'Accept': type}
  head = dict(make_ua(), **htype)
  response = requests.get(url, headers = head, allow_redirects = True, **kwargs)

  # Raise an HTTPError if the status code of the response is 4XX or 5XX
  response.raise_for_status()

  return response.text
