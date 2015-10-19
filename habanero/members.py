class Members(object):
  '''
  Search Crossref members

  :param ids: member ids.

  Usage
  >>> from habanero import Habanero
  >>> hb = Habanero()
  >>> hb.members(ids = 98)
  >>> # get works
  >>> hb.members.works(ids = 98)
  '''
  def __init__(self, ids = None, query = None, filter = None,
    offset = None, limit = None, sample = None, sort = None,
    order = None, facet = None, **kwargs):

    self.ids = ids
    self.query = query
    self.filter = filter
    self.offset = offset
    self.limit = limit
    self.sample = sample
    self.sort = sort
    self.order = order
    self.facet = facet
    self.url = self.base_url + "/members/"

    url = self.url
    if(self.ids.__class__.__name__ == 'NoneType'):
        pass
    else:
        url = url + self.ids

    return request(url, self.ids, self.query, self.filter,
      self.offset, self.limit, self.sample, self.sort,
      self.order, self.facet, **kwargs)

  # def works()
  #   pass

def request(url, ids = None, query = None, filter = None,
      offset = None, limit = None, sample = None, sort = None,
      order = None, facet = None, **kwargs):

  payload = {'query':query, 'filter':filter, 'offset':offset,
             'rows':limit, 'sample':sample, 'sort':sort,
             'order':order, 'facet':facet}

  tt = requests.get(url, params = payload, **kwargs)
  return tt
