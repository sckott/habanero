import sys
import requests
import json

# class Works(object):
#     """docstring for Works"""
#     def __init__(self, arg):
#         super(Works, self).__init__()
#         self.arg = arg

def works(ids = None, query = None, filter = None, offset = None,
          limit = None, sample = None, sort = None,
          order = None, facet = None, **kwargs):
    '''
    Search Crossref works

    :param ids: dois.

    Usage
    # A basic example
    >>> import habanero
    >>> habanero.works(ids = '10.1371/journal.pone.0033693')
    '''

    url = "http://api.crossref.org/works/"
    payload = {'query':query, 'filter':filter, 'offset':offset,
               'rows':limit, 'sample':sample, 'sort':sort,
               'order':order, 'facet':facet}
    if(ids.__class__.__name__ == 'NoneType'):
        pass
    else:
        url = url + ids

    tt = requests.get(url, params = payload, **kwargs)
    return tt

if __name__ == "__main__":
    import doctest
    doctest.testmod()
