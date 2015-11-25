import requests
import json
import re

from .filterhandler import filter_handler
from .habanero_utils import switch_classes
from .exceptions import *

class Request(object):
  '''
  Habanero: request class

  This is the request class for all requests
  '''
  def __init__(self, url, path, ids = None, query = None, filter = None,
        offset = None, limit = None, sample = None, sort = None,
        order = None, facet = None, cursor = None, cursor_max = None,
        works = None, agency = False):
    self.url = url
    self.path = path
    self.ids = ids
    self.query = query
    self.filter = filter
    self.offset = offset
    self.limit = limit
    self.sample = sample
    self.sort = sort
    self.order = order
    self.facet = facet
    self.cursor = cursor
    self.cursor_max = cursor_max
    self.works = works
    self.agency = agency

  def _url(self):
    tmpurl = self.url + self.path
    return tmpurl.strip("/")

  def do_request(self):
    filt = filter_handler(self.filter)

    payload = {'query':self.query, 'filter':filt, 'offset':self.offset,
               'rows':self.limit, 'sample':self.sample, 'sort':self.sort,
               'order':self.order, 'facet':self.facet, 'cursor':self.cursor}
    payload = dict((k, v) for k, v in payload.items() if v)

    js = self._req(payload = payload)
    cu = js['message'].get('next-cursor')
    max_avail = js['message']['total-results']
    res = self._redo_req(js, payload, cu, max_avail)
    return res

  def _redo_req(self, js, payload, cu, max_avail):
    if(cu.__class__.__name__ != 'NoneType' and self.cursor_max > len(js['message']['items'])):
      res = [js]
      total = len(js['message']['items'])
      while(cu.__class__.__name__ != 'NoneType' and self.cursor_max > total and total < max_avail):
        payload['cursor'] = cu
        out = self._req(payload = payload)
        # out = _req(url = url, payload = payload)
        cu = out['message'].get('next-cursor')
        res.append(out)
        total = sum([ len(z['message']['items']) for z in res ])
      return res
    else:
      return js

  def _req(self, payload):
    tt = requests.get(self._url(), params = payload)
    tt.raise_for_status()
    check_json(tt)
    return tt.json()

def check_json(x):
  ctype = x.headers['Content-Type']
  matched = re.match("application/json", ctype)
  if matched.__class__.__name__ == 'NoneType':
    scode = x.status_code
    if str(x.text) == "Not implemented.":
      scode = 400
    raise RequestError(scode, str(x.text))
