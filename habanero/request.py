import requests
import json
import re

from .filterhandler import filter_handler
from .habanero_utils import switch_classes,check_json,is_json,parse_json_err,make_ua,filter_dict,rename_query_filters
from .exceptions import *
from .request_class import Request

def request(mailto, url, path, ids = None, query = None, filter = None,
        offset = None, limit = None, sample = None, sort = None,
        order = None, facet = None, select = None, works = None,
        cursor = None, cursor_max = None, agency = False, 
        progress_bar = False, **kwargs):

  url = url + path

  if cursor_max.__class__.__name__ != 'NoneType':
    if cursor_max.__class__ != int:
      raise ValueError("cursor_max must be of class int")

  filt = filter_handler(filter)
  if select.__class__ is list:
    select = ','.join(select)

  payload = {'query':query, 'filter':filt, 'offset':offset,
             'rows':limit, 'sample':sample, 'sort':sort,
             'order':order, 'facet':facet, 'select':select,
             'cursor':cursor}
  payload = dict((k, v) for k, v in payload.items() if v)
  # add query filters
  payload.update(filter_dict(kwargs))
  # rename query filters
  payload = rename_query_filters(payload)

  if(ids.__class__.__name__ == 'NoneType'):
    url = url.strip("/")
    try:
      r = requests.get(url, params = payload, headers = make_ua(mailto))
      r.raise_for_status()
    except requests.exceptions.HTTPError:
      if is_json(r):
        raise RequestError(r.status_code, parse_json_err(r))
      else:
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
      raise e
    check_json(r)
    coll = r.json()
  else:
    if(ids.__class__.__name__ == "str"):
      ids = ids.split()
    if(ids.__class__.__name__ == "int"):
      ids = [ids]
    coll = []
    for i in range(len(ids)):
      if works:
        res = Request(mailto, url, str(ids[i]) + "/works",
          query, filter, offset, limit, sample, sort,
          order, facet, select, cursor, cursor_max, None, 
          progress_bar, **kwargs).do_request()
        coll.append(res)
      else:
        if agency:
          endpt = url + str(ids[i]) + "/agency"
        else:
          endpt = url + str(ids[i])

        endpt = endpt.strip("/")

        try:
          r = requests.get(endpt, params = payload, headers = make_ua(mailto))
          r.raise_for_status()
        except requests.exceptions.HTTPError:
          if is_json(r):
            raise RequestError(r.status_code, parse_json_err(r))
          else:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
          raise e
        check_json(r)
        js = r.json()
        coll.append(js)

    if len(coll) == 1:
      coll = coll[0]

  return coll
