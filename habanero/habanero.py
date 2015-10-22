import sys

from .request import request
from .habanero_utils import sub_str

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

    def prefixes(self, ids = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):

        '''
        Search Crossref prefixes

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
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
        >>> hb.prefixes(ids = "10.1016")
        >>> hb.prefixes(ids = ['10.1016','10.1371','10.1023','10.4176','10.1093'])
        >>> # get works
        >>> hb.prefixes(ids = "10.1016", works = True)
        >>> # Limit number of results
        >>> hb.prefixes(ids = "10.1016", works = True, limit = 3)
        >>> # Sort and order
        >>> hb.prefixes(ids = "10.1016", works = True, sort = "relevance", order = "asc")
        '''
        res = request(self.base_url, "/prefixes/", ids,
          query = None, filter = filter, offset = offset, limit = limit,
          sample = sample, sort = sort, order = order, facet = facet,
          works = works, **kwargs)
        return res

    def fundref(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):
        '''
        Search Crossref fundref

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
        >>> hb.fundref(ids = '10.13039/100000001')
        >>> hb.fundref(query = "NSF")
        >>> # get works
        >>> hb.fundref(ids = '10.13039/100000001', works = True)
        '''
        res = request(self.base_url, "/fundref/", ids,
          query, filter, offset, limit, sample, sort,
          order, facet, works, **kwargs)
        return res

    def journals(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):
        '''
        Search Crossref journals

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
        >>> hb.journals(ids = "2167-8359")
        >>> hb.journals()
        >>> hb.journals(ids = "2167-8359", works: TRUE)
        >>> hb.journals(ids = ['1803-2427', '2326-4225'])
        >>> hb.journals(query = "ecology")
        >>> hb.journals(query = "peerj")
        >>> hb.journals(ids = "2167-8359", query: 'ecology', works: TRUE, sort: 'score', order: "asc")
        >>> hb.journals(ids = "2167-8359", query: 'ecology', works: TRUE, sort: 'score', order: "desc")
        >>> hb.journals(ids = "2167-8359", works: TRUE, filter: {from_pub_date: '2014-03-03'})
        >>> hb.journals(ids = '1803-2427', works: TRUE)
        >>> hb.journals(ids = '1803-2427', works: TRUE, sample: 1)
        >>> hb.journals(limit: 2)
        '''
        res = request(self.base_url, "/journals/", ids,
          query, filter, offset, limit, sample, sort,
          order, facet, works, **kwargs)
        return res
