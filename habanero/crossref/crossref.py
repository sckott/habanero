from typing import List, Union, Optional

from ..habanero_utils import check_kwargs, sub_str
from ..request import request
from ..request_class import Request
from .filters import (
    funders_filter_details,
    members_filter_details,
    works_filter_details,
)


class Crossref:
    """
    Crossref: Class for Crossref search API methods

    :param base_url: Base URL to use for http requests
    :param api_key: An API key to send with each http request
    :param mailto: A mailto string, see section below
    :param ua_string: A user agent string, see section below
    :param timeout: curl timeout

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
    `python-httpx/0.27.2 habanero/1.2.6`. We send that string with
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

        import logging
        import httpx
        logging.basicConfig(
            format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG
        )

        from habanero import Crossref
        cr = Crossref()
        cr.works(query = "ecology")

    .. _FieldQueries:

    **Field queries**

    One or more field queries. Field queries are searches on specific fields.
    For example, using `query_author` searches author names instead of full search
    across all fields as would happen by default. Acceptable field
    query parameters have all underscores where Crossref API documentation
    has `.` or `-`. For example, `query.funder-name` using the Crossref API
    should be `query_funder_name`. See "Field queries" under the Crossref API
    documentation for the supported field queries.

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
        base_url: str = "https://api.crossref.org",
        api_key: Optional[str] = None,
        mailto: Optional[str] = None,
        ua_string: Optional[str] = None,
        timeout: int = 5,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.mailto = mailto
        self.ua_string = ua_string
        self.timeout = timeout

    def __repr__(self):
        return (
            """< %s \nURL: %s\nKEY: %s\nMAILTO: %s\nADDITIONAL UA STRING: %s\nTimeout: %s\n>"""
            % (
                type(self).__name__,
                self.base_url,
                sub_str(self.api_key),
                self.mailto,
                self.ua_string,
                self.timeout,
            )
        )

    def works(
        self,
        ids: List[str] | str | None = None,
        query: Optional[str] = None,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref works

        :param ids: DOIs (digital object identifier) or other identifiers
        :param query: A query string
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relavant when searching with specific dois.
            Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. Max: 100
        :param sort: Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`.
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used.
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found.
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). default: False
        :param warn: warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
                self,
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
                **kwargs,
            )
        else:
            return Request(
                self.mailto,
                self.ua_string,
                self.timeout,
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
                **kwargs,
            ).do_request(should_warn=warn)

    def members(
        self,
        ids: List[str] | str | None = None,
        query: Optional[str] = None,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        works: bool = False,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref members

        :param ids: DOIs (digital object identifier) or other identifiers
        :param query: A query string
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
            IMPORTANT: when `works=False` the filters that will work are the members
            filters; when `works=True` the filters that will work are the works filters
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: If true, works returned as well. Default: false
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
            self,
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
            **kwargs,
        )

    def prefixes(
        self,
        ids: List[str] | str,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        works: bool = False,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref prefixes

        :param ids: DOIs (digital object identifier) or other identifiers. required
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: If true, works returned as well. Default: false
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
            self,
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
            **kwargs,
        )

    def funders(
        self,
        ids: List[str] | str | None = None,
        query: Optional[str] = None,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        works: bool = False,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref funders

        Note that funders without IDs don't show up on the `/funders` route,
        that is, won't show up in searches via this method

        :param ids: DOIs (digital object identifier) or other identifiers
        :param query: A query string
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
            IMPORTANT: when `works=False` the filters that will work are the funders
            filters; when `works=True` the filters that will work are the works filters
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relavant when searching with specific dois. Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort: Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: If true, works returned as well. Default: false
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
            self,
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
            **kwargs,
        )

    def journals(
        self,
        ids: List[str] | str | None = None,
        query: Optional[str] = None,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        works: bool = False,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref journals

        :param ids: DOIs (digital object identifier) or other identifiers
        :param query: A query string
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort:  Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order:  Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`.
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: If true, works returned as well. Default: false
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param warn: warn instead of raise error upon HTTP request error. default: False
            Especially helpful when passing in many DOIs where some may lead to request failures.
            Returns `None` when `warn=True` for each DOI that errors.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
            self,
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
            **kwargs,
        )

    def types(
        self,
        ids: List[str] | str | None = None,
        query: Optional[str] = None,
        filter: Optional[dict] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sample: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        works: bool = False,
        select: List[str] | str | None = None,
        cursor: Optional[str] = None,
        cursor_max: float = 5000,
        progress_bar: bool = False,
        warn: bool = False,
        **kwargs,
    ) -> dict:
        """
        Search Crossref types

        :param ids: Type identifier, e.g., journal
        :param query: A query string
        :param filter: Filter options. See examples for usage.
            Accepts a dict, with filter names and their values. For repeating filter names
            pass in a list of the values to that filter name, e.g.,
            `{'award_funder': ['10.13039/100004440', '10.13039/100000861']}`.
            See https://github.com/CrossRef/rest-api-doc#filter-names
            for filter names and their descriptions and :func:`~habanero.Crossref.filter_names`
            and :func:`~habanero.Crossref.filter_details`
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sample: Number of random results to return. when you use the sample parameter,
            the limit and offset parameters are ignored. This parameter only used when works requested. Max: 100
        :param sort:  Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order:  Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param select: Crossref metadata records can be
            quite large. Sometimes you just want a few elements from the schema. You can "select"
            a subset of elements to return. This can make your API calls much more efficient. Not
            clear yet which fields are allowed here.
        :param works: If true, works returned as well. Default: false
        :param cursor: Cursor character string to do deep paging. Default is None.
            Pass in '*' to start deep paging. Any combination of query, filters and facets may be
            used with deep paging cursors. While rows may be specified along with cursor, offset
            and sample cannot be used. Only used if `works=True`
            See https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors
        :param cursor_max: Max records to retrieve. Only used when cursor param used. Because
            deep paging can result in continuous requests until all are retrieved, use this
            parameter to set a maximum number of records. Of course, if there are less records
            found than this value, you will get only those found. Only used if `works=True`
        :param progress_bar: print progress bar. only used when doing deep paging (
            when using cursor parameter). Only used if `works=True`. default: False
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

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
            self,
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
            **kwargs,
        )

    def licenses(
        self,
        query: Optional[str] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        facet: str | bool | None = None,
        **kwargs,
    ) -> dict:
        """
        Search Crossref licenses

        :param query: A query string
        :param offset: Number of record to start at, from 1 to 10000
        :param limit: Number of results to return. Not relevant when searching with specific dois. Default: 20. Max: 1000
        :param sort: Field to sort on. Note: If the API call includes a query, then the sort
            order will be by the relevance score. If no query is included, then the sort order
            will be by DOI update date. See sorting_ for possible values.
        :param order: Sort order, one of 'asc' or 'desc'
        :param facet: Set to `true` to include facet results (default: false).
            Optionally, pass a query string, e.g., `facet=type-name:*` or `facet=license=*`
            See Facets_ for options.
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples and FieldQueries_)
        :rtype: dict

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.licenses()
            cr.licenses(query = "creative")
        """
        check_kwargs(["ids", "filter", "works"], kwargs)
        res = request(
            self,
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
            **kwargs,
        )
        return res

    def registration_agency(self, ids: Union[List[str], str], **kwargs) -> list:
        """
        Determine registration agency for DOIs

        :param ids: DOIs (digital object identifier) or other identifiers
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples)
        :rtype: list

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
            self,
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
            **kwargs,
        )
        if not isinstance(res, list):
            k = []
            k.append(res)
        else:
            k = res
        return [z["message"]["agency"]["label"] for z in k]

    def random_dois(self, sample: int = 10, **kwargs) -> list:
        """
        Get a random set of DOIs

        :param sample: Number of random DOIs to return. Default: 10. Max: 100
        :param kwargs: additional named arguments passed on to `requests.get`, e.g., field
            queries (see examples)
        :rtype: list

        Usage::

            from habanero import Crossref
            cr = Crossref()
            cr.random_dois(1)
            cr.random_dois(10)
            cr.random_dois(50)
            cr.random_dois(100)
        """
        res = request(
            self,
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
            **kwargs,
        )
        return [z["DOI"] for z in res["message"]["items"]]

    def filter_names(self, type: str = "works") -> list:
        """
        Filter names - just the names of each filter

        Filters are used in the Crossref search API to modify searches.
        As filters are introduced or taken away, we may get out of sync; check
        the docs for the latest https://github.com/CrossRef/rest-api-doc

        :param type: what type of filters, i.e., what API route, matches
            methods here. one of "works", "members", or "funders". Default: "works"
        :rtype: list

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

    def filter_details(self, type: str = "works") -> dict:
        """
        Filter details - filter names, possible values, and description

        Filters are used in the Crossref search API to modify searches.
        As filters are introduced or taken away, we may get out of sync; check
        the docs for the latest https://github.com/CrossRef/rest-api-doc

        :param type: what type of filters, i.e., what API route,
            matches methods here. one of "works", "members", or "funders".
            Default: "works"
        :rtype: dict

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
        output: dict[str, dict] = {
            "works": works_filter_details,
            "members": members_filter_details,
            "funders": funders_filter_details,
        }[type]
        return output
