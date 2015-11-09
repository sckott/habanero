import sys

from .request import request
from .cnrequest import CNRequest
from .habanero_utils import sub_str,check_kwargs

class Habanero(object):
    '''
    Habanero: Main habanero class

    Includes methods matching Crossref API routes:

    * /works - :func:`~habanero.Habanero.works`
    * /members - :func:`~habanero.Habanero.members`
    * /prefixes - :func:`~habanero.Habanero.prefixes`
    * /funders - :func:`~habanero.Habanero.funders`
    * /journals - :func:`~habanero.Habanero.journals`
    * /types - :func:`~habanero.Habanero.types`
    * /licenses - :func:`~habanero.Habanero.licenses`

    Also:

    * agency - :func:`~habanero.Habanero.agency`
    * content negotiation - :func:`~habanero.Habanero.content_negotiation`

    Doing setup::

        from habanero import Habanero
        hb = Habanero()
        # set a different base url
        Habanero(base_url = "http://some.other.url")
        # set an api key
        Habanero(api_key = "123456")

    '''
    def __init__(self, base_url = "http://api.crossref.org",
        cn_base_url = "http://dx.doi.org", api_key = None):

        self.base_url = base_url
        self.cn_base_url = cn_base_url
        self.api_key = api_key

    def __repr__(self):
      return """< %s \nURL: %s\nKEY: %s\nCN-URL: %s\n>""" % (type(self).__name__,
        self.base_url, sub_str(self.api_key), self.cn_base_url)

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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.works()
            hb.works(ids = '10.1371/journal.pone.0033693')
            x = hb.works(query = "ecology")
            x.status()
            x.message_type()
            x.message_version()
            x.message()
            x.total_results()
            x.items_per_page()
            x.query()
            x.items()

            # Get full text links
            x = hb.works(filter = {'has_full_text': True})
            x

            # Parse output to various data pieces
            x = hb.works(filter = {'has_full_text': True})
            ## get doi for each item
            [ z['DOI'] for z in x.result['message']['items'] ]
            ## get doi and url for each item
            [ {"doi": z['DOI'], "url": z['URL']} for z in x.result['message']['items'] ]
            ### print every doi
            for i in x.result['message']['items']:
                 print i['DOI']

            # filters - pass in as a dict
            ## see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#filter-names
            hb.works(filter = {'has_full_text': True})
            hb.works(filter = {'has_funder': True, 'has_full_text': True})
            hb.works(filter = {'award_number': 'CBET-0756451', 'award_funder': '10.13039/100000001'})
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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.members(ids = 98)
            # get works
            hb.members(ids = 98, works = True)
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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.prefixes(ids = "10.1016")
            hb.prefixes(ids = ['10.1016','10.1371','10.1023','10.4176','10.1093'])
            # get works
            hb.prefixes(ids = "10.1016", works = True)
            # Limit number of results
            hb.prefixes(ids = "10.1016", works = True, limit = 3)
            # Sort and order
            hb.prefixes(ids = "10.1016", works = True, sort = "relevance", order = "asc")
        '''
        check_kwargs(["query"], kwargs)
        res = request(self.base_url, "/prefixes/", ids,
          query = None, filter = filter, offset = offset, limit = limit,
          sample = sample, sort = sort, order = order, facet = facet,
          works = works, **kwargs)
        return res

    def funders(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):
        '''
        Search Crossref funders

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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.funders(ids = '10.13039/100000001')
            hb.funders(query = "NSF")
            # get works
            hb.funders(ids = '10.13039/100000001', works = True)
        '''
        res = request(self.base_url, "/funders/", ids,
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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.journals(ids = "2167-8359")
            hb.journals()
            hb.journals(ids = "2167-8359", works = True)
            hb.journals(ids = ['1803-2427', '2326-4225'])
            hb.journals(query = "ecology")
            hb.journals(query = "peerj")
            hb.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "asc")
            hb.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "desc")
            hb.journals(ids = "2167-8359", works = True, filter = {'from_pub_date': '2014-03-03'})
            hb.journals(ids = '1803-2427', works = True)
            hb.journals(ids = '1803-2427', works = True, sample = 1)
            hb.journals(limit: 2)
        '''
        res = request(self.base_url, "/journals/", ids,
          query, filter, offset, limit, sample, sort,
          order, facet, works, **kwargs)
        return res

    def types(self, ids = None, query = None, filter = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, works = False, **kwargs):
        '''
        Search Crossref types

        :param ids: [Array] Type identifier, e.g., journal
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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.types()
            hb.types(ids = "journal")
            hb.types(ids = "journal", works = True)
        '''
        res = request(self.base_url, "/types/", ids,
            query, filter, offset, limit, sample, sort,
            order, facet, works, **kwargs)
        return res

    def licenses(self, query = None, offset = None,
              limit = None, sample = None, sort = None,
              order = None, facet = None, **kwargs):
        '''
        Search Crossref licenses

        :param query: [String] A query string
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
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.licenses()
            hb.licenses(query = "creative")
        '''
        check_kwargs(["ids", "filter", "works"], kwargs)
        res = request(self.base_url, "/licenses/", None,
            query, None, offset, limit, sample, sort,
            order, facet, None, **kwargs)
        return res

    def agency(self, ids, **kwargs):
        '''
        Determine registration agency for DOIs

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Object response class, light wrapper around a dict

        Usage::

            from habanero import Habanero
            hb = Habanero()
            x = hb.agency('10.1371/journal.pone.0033693')
            x.agency()
            x = hb.agency(ids = ['10.1007/12080.1874-1746','10.1007/10452.1573-5125', '10.1111/(issn)1442-9993'])
            [ z.agency() for z in x ]
        '''
        check_kwargs(["query", "filter", "offset", "limit", "sample", "sort",
            "order", "facet", "works"], kwargs)
        res = request(self.base_url, "/works/", ids,
            None, None, None, None, None, None,
            None, None, None, True, **kwargs)
        return res

    def content_negotiation(self, ids = None, format = "bibtex", style = 'apa',
        locale = "en-US", **kwargs):
        '''
        Get citations in various formats from CrossRef

        :param idsc [String] DOIs
        :param format: [String] Format
        :param style: [String] Style
        :param locale: [String] Locale
        :param kwargs: any additional arguments will be passed on to
            `requests.get`

        :return: Hash

        Usage::

            from habanero import Habanero
            hb = Habanero()
            hb.content_negotiation(ids = '10.1126/science.169.3946.635')

            # get citeproc-json
            hb.content_negotiation(ids = '10.1126/science.169.3946.635', format = "citeproc-json")

            # some other formats
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "rdf-xml")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "crossref-xml")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text")

            # return an R bibentry type
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "bibentry")
            hb.content_negotiation(ids = "10.6084/m9.figshare.97218", format = "bibentry")

            # return an apa style citation
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "apa")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "harvard3")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "elsevier-harvard")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "ecoscience")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "heredity")
            hb.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "oikos")

            # Using DataCite DOIs
            ## some formats don't work
            # hb.content_negotiation(ids = "10.5284/1011335", format = "text")
            # hb.content_negotiation(ids = "10.5284/1011335", format = "crossref-xml")
            # hb.content_negotiation(ids = "10.5284/1011335", format = "crossref-tdm")

            ## But most do work
            hb.content_negotiation(ids = "10.5284/1011335", format = "datacite-xml")
            hb.content_negotiation(ids = "10.5284/1011335", format = "rdf-xml")
            hb.content_negotiation(ids = "10.5284/1011335", format = "turtle")
            hb.content_negotiation(ids = "10.5284/1011335", format = "citeproc-json")
            hb.content_negotiation(ids = "10.5284/1011335", format = "ris")
            hb.content_negotiation(ids = "10.5284/1011335", format = "bibtex")
            hb.content_negotiation(ids = "10.5284/1011335", format = "bibentry")
            hb.content_negotiation(ids = "10.5284/1011335", format = "bibtex")

            # many DOIs
            dois = ['10.5167/UZH-30455','10.5167/UZH-49216','10.5167/UZH-503', '10.5167/UZH-38402','10.5167/UZH-41217']
            x = hb.content_negotiation(ids = dois)
        '''
        return CNRequest(self.cn_base_url, ids, format, style, locale, **kwargs)
