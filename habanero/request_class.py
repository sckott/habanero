import requests
import json
import re

from .filterhandler import filter_handler
from .habanero_utils import switch_classes,check_json,is_json,parse_json_err,make_ua,filter_dict,rename_query_filters
from .exceptions import *

class Request(object):
  '''
  Habanero: request class

  This is the request class for all requests
  '''
  def __init__(self, url, path, query = None, filter = None,
        offset = None, limit = None, sample = None, sort = None,
        order = None, facet = None, cursor = None, cursor_max = None,
        agency = False, **kwargs):
    self.url = url
    self.path = path
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
    self.agency = agency
    self.kwargs = kwargs

  def _url(self):
    tmpurl = self.url + self.path
    return tmpurl.strip("/")

  def do_request(self):
    filt = filter_handler(self.filter)

    if not isinstance(self.cursor_max, (type(None), int)):
      raise ValueError("cursor_max must be of class int")

    payload = {'query':self.query, 'filter':filt, 'offset':self.offset,
               'rows':self.limit, 'sample':self.sample, 'sort':self.sort,
               'order':self.order, 'facet':self.facet, 'cursor':self.cursor}
    payload = dict((k, v) for k, v in payload.items() if v)
    # add query filters
    payload.update(filter_dict(self.kwargs))
    # rename query filters
    payload = rename_query_filters(payload)

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
        cu = out['message'].get('next-cursor')
        res.append(out)
        total = sum([ len(z['message']['items']) for z in res ])
      return res
    else:
      return js

  def _req(self, payload):
    try:
      r = requests.get(self._url(), params = payload, headers = make_ua())
      r.raise_for_status()
    except requests.exceptions.HTTPError:
      try:
        f = r.json()
        raise RequestError(r.status_code, f['message'][0]['message'])
      except:
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
      print(e)
    check_json(r)
    return r.json()
