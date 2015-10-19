import sys
import requests
import json

from .response import Response

class Habanero(object):
    '''
    Habanero: Main habanero class

    >>> from habanero import Habanero
    >>>
    >>> hb = Habanero()
    >>> # set a different base url
    >>> Habanero(base_url = "http://some.other.url")
    >>> # set an api key
    >>> Habanero(api_key = "123456")
    '''
    def __init__(self, base_url = "http://api.crossref.org", api_key = None):
        # super(ids, self).__init__()
        self.base_url = base_url
        self.api_key = api_key

    def __repr__(self):
      return """< %s \nURL: %s\nKEY: %s\n>""" % (type(self).__name__,
        self.base_url, sub_str(self.api_key))

    def works(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, **kwargs):
        '''
        Search Crossref works

        :param ids: dois.

        Usage
        >>> from habanero import Habanero
        >>> hb = Habanero()
        >>> hb.works()
        >>> hb.works(ids = '10.1371/journal.pone.0033693')
        >>> hb.works(query = "ecology")
        '''
        res = request(self.base_url, "/works/", ids,
          query, filter, offset, limit, sample, sort,
          order, facet, works = False, **kwargs)
        return res

    def members(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):
        '''
        Search Crossref members

        :param ids: member ids.

        Usage
        >>> from habanero import Habanero
        >>> hb = Habanero()
        >>> hb.members(ids = 98)
        >>> # get works
        >>> hb.members(ids = 98, works = True)
        '''
        res = request(self.base_url, "/members/", ids,
          query, filter, offset, limit, sample, sort,
          order, facet, works, **kwargs)
        return res

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

# helpers ----------
def converter(x):
  if(x.__class__.__name__ == 'str'):
      return [x]
  else:
      return x

def sub_str(x, n = 3):
  if(x.__class__.__name__ == 'NoneType'):
    pass
  else:
    return str(x[:n]) + '***'
