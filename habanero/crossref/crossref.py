import sys
import requests
from ..request import request
from ..request_class import Request
from ..habanero_utils import sub_str, check_kwargs
from .filters import (
    works_filter_details,
    members_filter_details,
    funders_filter_details,
)


class Crossref(object):
    """
    Crossref: Class for Crossref search API methods

    |
    |

    **Includes methods matching Crossref API routes**

    * /works - :func:`~habanero.Crossref.works`
    * /members - :func:`~habanero.Crossref.members`
    * /prefixes - :func:`~habanero.Crossref.prefixes`
    * /funders - :func:`~habanero.Crossref.funders`
    * /journals - :func:`~habanero.Crossref.journals`
    * /types - :func:`~habanero.Crossref.types`
    * /licenses - :func:`~habanero.Crossref.licenses`

    Also:

    * registration_agency - :func:`~habanero.Crossref.registration_agency`
    * random_dois - :func:`~habanero.Crossref.random_dois`

    **What am I actually searching when using the Crossref search API?**

    You are using the Crossref search API described at
    https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md.
    When you search with query terms on Crossref servers, they are not
    searching full text, or even abstracts of articles, but only what is
    available in the data that is returned to you. That is, they search
    article titles, authors, etc. For some discussion on this, see
    https://github.com/CrossRef/rest-api-doc/issues/101.

    **The Polite Pool**

    As of September 18th 2017, any API queries that use HTTPS and have
    appropriate contact information will be directed to a special pool
    of API machines that are reserved for polite users. If you connect
    to the Crossref API using HTTPS and provide contact
    information, then they will send you to a separate pool of machines,
    with better control of the performance of these machines because they can
    block abusive users.

    We have been using `https` in `habanero` for a while now, so that's good
    to go. To get into the Polite Pool, also set your mailto email address
    when you instantiate the `Crossref` object. See examples below.

    **Setting a custom user-agent string**

    Using `ua_string` you can set an additional string that will be added
    to the UA string we send in every request, which looks like:
    `python-requests/2.22.0 habanero/0.7.0`. We send that string with
    the headers: `User-Agent` and `X-USER-AGENT`. Turn on verbose curl
    output to see the request headers sent. To unset the `ua_string`
    you set, just initialize a new Crossref class.

    **Doing setup**::

        from habanero import Crossref
        cr = Crossref()
        # set a different base url
        Crossref(base_url = "http://some.other.url")
        # set an api key
        Crossref(api_key = "123456")
        # set a mailto address to get into the "polite pool"
        Crossref(mailto = "foo@bar.com")
        # set an additional user-agent string
        Crossref(ua_string = "foo bar")

    .. _RateLimits:

    **Rate limits**

    See the headers `X-Rate-Limit-Limit` and `X-Rate-Limit-Interval` for current
    rate limits. As of this writing, the limit is 50 requests per second,
    but that could change. In addition, it's not clear what the time is to reset.
    See below for getting header info for your requests.

    .. _CurlOpts:

    **Verbose curl output**::

        import requests
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        from habanero import Crossref
        cr = Crossref()
        cr.works(query = "ecology")

    .. _FieldQueries:

    **Field queries**

    One or more field queries. Field queries are searches on specific fields.
    For example, using `query_author` searches author names instead of full search
    across all fields as would happen by default. Acceptable field
    query parameters are:

    * `query_container_title` - Query container-title aka. publication name
    * `query_author` - Query author given and family names
    * `query_editor` - Query editor given and family names
    * `query_chair` - Query chair given and family names
    * `query_translator` - Query translator given and family names
    * `query_contributor` - Query author, editor, chair and translator given and family names
    * `query_bibliographic` - Query bibliographic information, useful for citation look up. Includes titles, authors, ISSNs and publication years. Crossref retired `query_title`; use this field query instead
    * `query_affiliation` - Query contributor affiliations

    .. _sorting:

    **Sort options**

    * `score` or `relevance` - Sort by relevance score
    * `updated` - Sort by date of most recent change to metadata. Currently the same as deposited.
    * `deposited` - Sort by time of most recent deposit
    * `indexed` - Sort by time of most recent index
    * `published` - Sort by publication date
    * `published-print` - Sort by print publication date
    * `published-online` - Sort by online publication date
    * `issued` - Sort by issued date (earliest known publication date)
    * `is-referenced-by-count` - Sort by number of references to documents
    * `references-count` - Sort by number of references made by documents


    .. _Facets:

    **Facet count options**

    * `affiliation` - Author affiliation. Allowed value: *
    * `year` - Earliest year of publication, synonym for published. Allowed value: *
    * `funder-name` - Funder literal name as deposited alongside DOIs. Allowed value: *
    * `funder-doi` - Funder DOI. Allowed value: *
    * `orcid` - Contributor ORCID. Max value: 100
    * `container-title` - Work container title, such as journal title, or book title. Max value: 100
    * `assertion` - Custom Crossmark assertion name. Allowed value: *
    * `archive` - Archive location. Allowed value: *
    * `update-type` - Significant update type. Allowed value: *
    * `issn` - Journal ISSN (any - print, electronic, link). Max value: 100
    * `published` - Earliest year of publication. Allowed value: *
    * `type-name` - Work type name, such as journal-article or book-chapter. Allowed value: *
    * `license` - License URI of work. Allowed value: *
    * `category-name` - Category name of work. Allowed value: *
    * `relation-type` - Relation type described by work or described by another work with work as object. Allowed value: *
    * `assertion-group` - Custom Crossmark assertion group name. Allowed value: *


    |
    |
    |
    """

    def __init__(
        self,
        base_url="https://api.crossref.org",
        api_key=None,
        mailto=None,
        ua_string=None,
    ):

        self.base_url = base_url
        self.api_key = api_key
        self.mailto = mailto
        self.ua_string = ua_string

    def __repr__(self):
        return (
            """< %s \nURL: %s\nKEY: %s\nMAILTO: %s\nADDITIONAL UA STRING: %s\n>"""
            % (
                type(self).__name__,
                self.base_url,
                sub_str(self.api_key),
                self.mailto,
                self.ua_string,
            )
        )

    def works(
        self,
        ids=None,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref works

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relavant when searching with specific dois.
            Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`.
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used.
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found.
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). default: False
        :param warn: [Boolean] warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.works()
            cr.works(ids = '10.1371/journal.pone.0033693')
            dois = ['10.1371/journal.pone.0033693', ]
            cr.works(ids = dois)
            x = cr.works(query = "ecology")
            x['status']
            x['message-type']
            x['message-version']
            x['message']
            x['message']['total-results']
            x['message']['items-per-page']
            x['message']['query']
            x['message']['items']

            # Get full text links
            x = cr.works(filter = {'has_full_text': True})
            x

            # Parse output to various data pieces
            x = cr.works(filter = {'has_full_text': True})
            ## get doi for each item
            [ z['DOI'] for z in x['message']['items'] ]
            ## get doi and url for each item
            [ {"doi": z['DOI'], "url": z['URL']} for z in x['message']['items'] ]
            ### print every doi
            for i in x['message']['items']:
                 print i['DOI']

            # filters - pass in as a dict
            ## see https://github.com/CrossRef/rest-api-doc#filter-names
            cr.works(filter = {'has_full_text': True})
            cr.works(filter = {'has_funder': True, 'has_full_text': True})
            cr.works(filter = {'award_number': 'CBET-0756451', 'award_funder': '10.13039/100000001'})
            ## to repeat a filter name, pass in a list
            x = cr.works(filter = {'award_funder': ['10.13039/100004440', '10.13039/100000861']}, limit = 100)
            map(lambda z:z['funder'][0]['DOI'], x['message']['items'])

            # Deep paging, using the cursor parameter
            ## this search should lead to only ~215 results
            cr.works(query = "widget", cursor = "*", cursor_max = 100)
            ## this search should lead to only ~2500 results, in chunks of 500
            res = cr.works(query = "octopus", cursor = "*", limit = 500)
            sum([ len(z['message']['items']) for z in res ])
            ## about 167 results
            res = cr.works(query = "extravagant", cursor = "*", limit = 50, cursor_max = 500)
            sum([ len(z['message']['items']) for z in res ])
            ## cursor_max to get back only a maximum set of results
            res = cr.works(query = "widget", cursor = "*", cursor_max = 100)
            sum([ len(z['message']['items']) for z in res ])
            ## cursor_max - especially useful when a request could be very large
            ### e.g., "ecology" results in ~275K records, lets max at 10,000
            ###   with 1000 at a time
            res = cr.works(query = "ecology", cursor = "*", cursor_max = 10000, limit = 1000)
            sum([ len(z['message']['items']) for z in res ])
            items = [ z['message']['items'] for z in res ]
            items = [ item for sublist in items for item in sublist ]
            [ z['DOI'] for z in items ][0:50]
            ### use progress bar
            res = cr.works(query = "octopus", cursor = "*", limit = 500, progress_bar = True)

            # field queries
            res = cr.works(query = "ecology", query_author = 'carl boettiger')
            [ x['author'][0]['family'] for x in res['message']['items'] ]

            # select certain fields to return
            ## as a comma separated string
            cr.works(query = "ecology", select = "DOI,title")
            ## or as a list
            cr.works(query = "ecology", select = ["DOI","title"])

            # set an additional user-agent string
            ## the string is additional because it's added to the UA string we send in every request
            ## turn on verbose curl output to see the request headers sent
            x = Crossref(ua_string = "foo bar")
            x
            x.works(ids = '10.1371/journal.pone.0033693')
            ## unset the additional user-agent string
            x = Crossref()
            x.works(ids = '10.1371/journal.pone.0033693')
        """
        if ids.__class__.__name__ != "NoneType":
            return request(
                self.mailto,
                self.ua_string,
                self.base_url,
                "/works/",
                ids,
                query,
                filter,
                offset,
                limit,
                sample,
                sort,
                order,
                facet,
                select,
                None,
                None,
                None,
                None,
                progress_bar,
                warn,
                **kwargs
            )
        else:
            return Request(
                self.mailto,
                self.ua_string,
                self.base_url,
                "/works/",
                query,
                filter,
                offset,
                limit,
                sample,
                sort,
                order,
                facet,
                select,
                cursor,
                cursor_max,
                None,
                progress_bar,
                **kwargs
            ).do_request(should_warn=warn)

    def members(
        self,
        ids=None,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        works=False,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref members

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
            IMPORTANT: when `works=False` the filters that will work are the members
            filters; when `works=True` the filters that will work are the works filters
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: [Boolean] If true, works returned as well. Default: false
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: [Boolean] warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.members(ids = 98)

            # get works
            res = cr.members(ids = 98, works = True, limit = 3)
            len(res['message']['items'])
            [ z['DOI'] for z in res['message']['items'] ]

            # cursor - deep paging
            res = cr.members(ids = 98, works = True, cursor = "*")
            sum([ len(z['message']['items']) for z in res ])
            items = [ z['message']['items'] for z in res ]
            items = [ item for sublist in items for item in sublist ]
            [ z['DOI'] for z in items ][0:50]
            ## use progress bar
            res = cr.members(ids = 98, works = True, cursor = "*", cursor_max = 500, progress_bar = True)

            # field queries
            res = cr.members(ids = 98, works = True, query_author = 'carl boettiger', limit = 7)
            [ x['author'][0]['family'] for x in res['message']['items'] ]

            # filters (as of this writing, 4 filters are avail., see filter_names())
            res = cr.members(filter = {'has_public_references': True})
        """
        return request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/members/",
            ids,
            query,
            filter,
            offset,
            limit,
            sample,
            sort,
            order,
            facet,
            select,
            works,
            cursor,
            cursor_max,
            None,
            progress_bar,
            warn,
            **kwargs
        )

    def prefixes(
        self,
        ids=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        works=False,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref prefixes

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: [Boolean] If true, works returned as well. Default: false
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: [Boolean] warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.prefixes(ids = "10.1016")
            cr.prefixes(ids = ['10.1016','10.1371','10.1023','10.4176','10.1093'])

            # get works
            cr.prefixes(ids = "10.1016", works = True)

            # Limit number of results
            cr.prefixes(ids = "10.1016", works = True, limit = 3)

            # Sort and order
            cr.prefixes(ids = "10.1016", works = True, sort = "relevance", order = "asc")

            # cursor - deep paging
            res = cr.prefixes(ids = "10.1016", works = True, cursor = "*", limit = 200)
            sum([ len(z['message']['items']) for z in res ])
            items = [ z['message']['items'] for z in res ]
            items = [ item for sublist in items for item in sublist ]
            [ z['DOI'] for z in items ][0:50]
            ## use progress bar
            res = cr.prefixes(ids = "10.1016", works = True, cursor = "*", cursor_max = 200, progress_bar = True)

            # field queries
            res = cr.prefixes(ids = "10.1371", works = True, query_editor = 'cooper', filter = {'type': 'journal-article'})
            eds = [ x.get('editor') for x in res['message']['items'] ]
            [ z for z in eds if z is not None ]
        """
        check_kwargs(["query"], kwargs)
        return request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/prefixes/",
            ids,
            query=None,
            filter=filter,
            offset=offset,
            limit=limit,
            sample=sample,
            sort=sort,
            order=order,
            facet=facet,
            select=select,
            works=works,
            cursor=cursor,
            cursor_max=cursor_max,
            progress_bar=progress_bar,
            should_warn=warn,
            **kwargs
        )

    def funders(
        self,
        ids=None,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        works=False,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref funders

        Note that funders without IDs don't show up on the `/funders` route,
        that is, won't show up in searches via this method

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
            IMPORTANT: when `works=False` the filters that will work are the funders
            filters; when `works=True` the filters that will work are the works filters
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: [Boolean] If true, works returned as well. Default: false
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: [Boolean] warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.funders(ids = '10.13039/100000001')
            cr.funders(query = "NSF")

            # get works
            cr.funders(ids = '10.13039/100000001', works = True)

            # cursor - deep paging
            res = cr.funders(ids = '10.13039/100000001', works = True, cursor = "*", limit = 200)
            sum([ len(z['message']['items']) for z in res ])
            items = [ z['message']['items'] for z in res ]
            items = [ item for sublist in items for item in sublist ]
            [ z['DOI'] for z in items ][0:50]
            ## use progress bar
            res = cr.funders(ids = '10.13039/100000001', works = True, cursor = "*", cursor_max = 200, progress_bar = True)

            # field queries
            res = cr.funders(ids = "10.13039/100000001", works = True, query_container_title = 'engineering', filter = {'type': 'journal-article'})
            eds = [ x.get('editor') for x in res['message']['items'] ]
            [ z for z in eds if z is not None ]

            # filters (as of this writing, only 1 filter is avail., "location")
            cr.funders(filter = {'location': "Sweden"})

            # warn
            cr.funders(ids = '10.13039/notarealdoi')
            cr.funders(ids = '10.13039/notarealdoi', warn=True)
            cr.funders(ids = '10.13039/notarealdoi', works=True, warn=True)
            cr.funders(ids = ['10.13039/100000001','10.13039/notarealdoi'], works=True, warn=True)
            x = cr.funders(ids = ['10.13039/100000001','10.13039/notarealdoi'], warn=True)
            len(x) # 2
            [type(w) for w in x] # [dict, NoneType]
        """
        return request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/funders/",
            ids,
            query,
            filter,
            offset,
            limit,
            sample,
            sort,
            order,
            facet,
            select,
            works,
            cursor,
            cursor_max,
            None,
            progress_bar,
            warn,
            **kwargs
        )

    def journals(
        self,
        ids=None,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        works=False,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref journals

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`.
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: [Boolean] If true, works returned as well. Default: false
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: [Boolean] warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.journals(ids = "2167-8359")
            cr.journals()

            # pass many ids
            cr.journals(ids = ['1803-2427', '2326-4225'])

            # search
            cr.journals(query = "ecology")
            cr.journals(query = "peerj")

            # get works
            cr.journals(ids = "2167-8359", works = True)
            cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "asc")
            cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "desc")
            cr.journals(ids = "2167-8359", works = True, filter = {'from_pub_date': '2014-03-03'})
            cr.journals(ids = '1803-2427', works = True)
            cr.journals(ids = '1803-2427', works = True, sample = 1)
            cr.journals(limit: 2)

            # cursor - deep paging
            res = cr.journals(ids = "2167-8359", works = True, cursor = "*", cursor_max = 200)
            sum([ len(z['message']['items']) for z in res ])
            items = [ z['message']['items'] for z in res ]
            items = [ item for sublist in items for item in sublist ]
            [ z['DOI'] for z in items ][0:50]
            ## use progress bar
            res = cr.journals(ids = "2167-8359", works = True, cursor = "*", cursor_max = 200, progress_bar = True)

            # field queries
            res = cr.journals(ids = "2167-8359", works = True, query_bibliographic = 'fish', filter = {'type': 'journal-article'})
            [ x.get('title') for x in res['message']['items'] ]
        """
        return request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/journals/",
            ids,
            query,
            filter,
            offset,
            limit,
            sample,
            sort,
            order,
            facet,
            select,
            works,
            cursor,
            cursor_max,
            None,
            progress_bar,
            warn,
            **kwargs
        )

    def types(
        self,
        ids=None,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        works=False,
        select=None,
        cursor=None,
        cursor_max=5000,
        progress_bar=False,
        warn=False,
        **kwargs
    ):
        """
        Search Crossref types

        :param ids: [Array] Type identifier, e.g., journal
        :param query: [String] A query string
        :param filter: [Hash] Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: [Fixnum] Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: [String/list(Strings)] Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: [Boolean] If true, works returned as well. Default: false
        :param cursor: [String] Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: [Fixnum] Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: [Boolean] print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.types()
            cr.types(ids = "journal")
            cr.types(ids = "journal-article")
            cr.types(ids = "journal", works = True)

            # deep paging
            res = cr.types(ids = "journal-article", works = True, cursor = "*", cursor_max = 120)
            ## use progress bar
            res = cr.types(ids = "journal-article", works = True, cursor = "*", cursor_max = 120, progress_bar = True)

            # field queries
            res = cr.types(ids = "journal-article", works = True, query_bibliographic = 'gender', rows = 100)
            [ x.get('title') for x in res['message']['items'] ]
        """
        return request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/types/",
            ids,
            query,
            filter,
            offset,
            limit,
            sample,
            sort,
            order,
            facet,
            select,
            works,
            cursor,
            cursor_max,
            None,
            progress_bar,
            warn,
            **kwargs
        )

    def licenses(
        self,
        query=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        **kwargs
    ):
        """
        Search Crossref licenses

        :param query: [String] A query string
        :param offset: [Fixnum] Number of record to start at, from 1 to 10000
        :param limit: [Fixnum] Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sort: [String] Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: [String] Sort order, one of 'asc' or 'desc'
        :param facet: [Boolean/String] Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)

        :return: A dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.licenses()
            cr.licenses(query = "creative")
        """
        check_kwargs(["ids", "filter", "works"], kwargs)
        res = request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/licenses/",
            None,
            query,
            None,
            offset,
            limit,
            None,
            sort,
            order,
            facet,
            None,
            None,
            None,
            None,
            **kwargs
        )
        return res

    def registration_agency(self, ids, **kwargs):
        """
        Determine registration agency for DOIs

        :param ids: [Array] DOIs (digital object identifier) or other identifiers
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples)

        :return: list of DOI minting agencies

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.registration_agency('10.1371/journal.pone.0033693')
            cr.registration_agency(ids = ['10.1007/12080.1874-1746','10.1007/10452.1573-5125', '10.1111/(issn)1442-9993'])
        """
        check_kwargs(
            [
                "query",
                "filter",
                "offset",
                "limit",
                "sample",
                "sort",
                "order",
                "facet",
                "works",
            ],
            kwargs,
        )
        res = request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/works/",
            ids,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
            **kwargs
        )
        if res.__class__ != list:
            k = []
            k.append(res)
        else:
            k = res
        return [z["message"]["agency"]["label"] for z in k]

    def random_dois(self, sample=10, **kwargs):
        """
        Get a random set of DOIs

        :param sample: [Fixnum] Number of random DOIs to return. Default: 10. Max: 100
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples)

        :return: [Array] of DOIs

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.random_dois(1)
            cr.random_dois(10)
            cr.random_dois(50)
            cr.random_dois(100)
        """
        res = request(
            self.mailto,
            self.ua_string,
            self.base_url,
            "/works/",
            None,
            None,
            None,
            None,
            None,
            sample,
            None,
            None,
            None,
            None,
            True,
            None,
            None,
            None,
            **kwargs
        )
        return [z["DOI"] for z in res["message"]["items"]]

    def filter_names(self, type="works"):
        """
        Filter names - just the names of each filter

        Filters are used in the Crossref search API to modify searches.
        As filters are introduced or taken away, we may get out of sync; check
        the docs for the latest https://github.com/CrossRef/rest-api-doc

        :param type: [str] what type of filters, i.e., what API route, matches
            methods here. one of "works", "members", or "funders". Default: "works"

        :return: list

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.filter_names()
            cr.filter_names("members")
            cr.filter_names("funders")
        """
        nms = list(self.filter_details(type).keys())
        nms.sort()
        return nms

    def filter_details(self, type="works"):
        """
        Filter details - filter names, possible values, and description

        Filters are used in the Crossref search API to modify searches.
        As filters are introduced or taken away, we may get out of sync; check
        the docs for the latest https://github.com/CrossRef/rest-api-doc

        :param type: [str] what type of filters, i.e., what API route,
            matches methods here. one of "works", "members", or "funders".
            Default: "works"

        :return: dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.filter_details()
            cr.filter_details("members")
            cr.filter_details("funders")
            # Get descriptions for each filter
            x = cr.filter_details()
            [ z['description'] for z in x.values() ]
        """
        types = ["works", "members", "funders"]
        if type not in types:
            raise ValueError("'type' must be one of " + "', '".join(types))
        return {
            "works": works_filter_details,
            "members": members_filter_details,
            "funders": funders_filter_details,
        }[type]
