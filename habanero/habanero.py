import sys

from .request import request
import habanero_utils

class Habanero(object):
    '''
    Habanero: Main habanero class

    Includes methods matching Crossref API routes:
    - /works
    - /members

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

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See ...
        :param offset: [Fixnum] Number of record to start at, from 1 to infinity.
        :param limit: [Fixnum] Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
        the limit and offset parameters are ignored.
        :param sort: [String] Field to sort on, one of score, relevance,
        updated (date of most recent change to metadata. Currently the same as deposited),
        deposited (time of most recent deposit), indexed (time of most recent index), or
        published (publication date). Note: If the API call includes a query, then the sort
        order will be by the relevance score. If no query is included, then the sort order
        will be by DOI update date.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean] Include facet results. Default: false

        :return: Object response class, light wrapper around a dict

        Usage
        >>> from habanero import Habanero
        >>> hb = Habanero()
        >>> hb.works()
        >>> hb.works(ids = '10.1371/journal.pone.0033693')
        >>> x = hb.works(query = "ecology")
        >>> x.status()
        >>> x.message_type()
        >>> x.message_version()
        >>> x.message()
        >>> x.total_results()
        >>> x.items_per_page()
        >>> x.query()
        >>> x.items()
        >>>
        >>> # filters - pass in as a dict
        >>> ## see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#filter-names
        >>> hb.works(filter = {'has_full_text': True})
        >>> hb.works(filter = {'has_funder': True, 'has_full_text': True})
        >>> hb.works(filter = {'award_number': 'CBET-0756451', 'award_funder': '10.13039/100000001'})
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

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See ...
        :param offset: [Fixnum] Number of record to start at, from 1 to infinity.
        :param limit: [Fixnum] Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
        the limit and offset parameters are ignored.
        :param sort: [String] Field to sort on, one of score, relevance,
        updated (date of most recent change to metadata. Currently the same as deposited),
        deposited (time of most recent deposit), indexed (time of most recent index), or
        published (publication date). Note: If the API call includes a query, then the sort
        order will be by the relevance score. If no query is included, then the sort order
        will be by DOI update date.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean] Include facet results. Default: false
        :param works: [Boolean] If true, works returned as well. Default: false

        :return: Object response class, light wrapper around a dict

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
