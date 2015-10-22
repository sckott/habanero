import requests
import json

from .response import Response

def request(url, path, ids = None, query = None, filter = None,
        offset = None, limit = None, sample = None, sort = None,
        order = None, facet = None, works = None, **kwargs):

  url = url + path

  if(ids.__class__.__name__ == 'NoneType'):
      pass
  else:
    if works:
      url = url + str(ids) + "/works"
    else:
      url = url + str(ids)

  url = url.strip("/")

  payload = {'query':query, 'filter':filter, 'offset':offset,
             'rows':limit, 'sample':sample, 'sort':sort,
             'order':order, 'facet':facet}
  payload = dict((k, v) for k, v in payload.iteritems() if v)

  tt = requests.get(url, params = payload, **kwargs)
  tt_out = Response(result = tt.json())
  return tt_out
