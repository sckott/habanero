Changelog
=========

1.2 (2022-03-27)
--------------------
* Added class `WorksContainer` to make handling works data easier (#101)
* changed master branch to main in github development repository (#103)
* exclude tests from install (#105)

1.0 (2021-11-12)
--------------------
* fixes to docs/contributing.rst and package level docs for habanero (#89) (#90) thanks @Daniel-Mietchen !
* fix limit and offset internal handling for `request` and `Request` (#91) thanks @Bubblbu !
* `content_negotation` throws warning now on 4xx/5xx status code to allow for bad DOIs alongside good DOIS (#92)
* add example to README for querying `works` by DOI (#93)
* fail better when json is not returned; try json.loads and catch ValueError (JSONDecodeError is a subclass of ValueError) (#97)
* funders, journals, members, prefixes, types and works gain `warn` parameter to optionally throw a warning instead of error if a DOI is not found - not found DOI with `warn=True` returns `None` (#69)

0.7.4 (2020-05-29)
--------------------
* `query.title` filter is deprecated, use `query.bibliographic` instead (#85)

0.7.2 (2019-12-12)
--------------------
* `Crossref()` class gains `ua_string` option to add an additional string to the user-agent sent with every request (#84)

0.7.0 (2019-11-08)
--------------------
* `filter_names()` and `filter_details()` altered to get metadata for works, members and funders filters; and added egs to members and funders methods for using filters (#67)
* many typos fixed (#80) thanks @Radcliffe !
* use of a progress bar is now possible when fetching works route data, only when doing deep paging, see `progress_bar` parameter (#77) (#82)
* `content_negotiation` fixes: `ids` parameter is now required (has no default), and must be a str or list of str (#83)
* no longer testing under Python 2

0.6.2 (2018-10-22)
--------------------
* changelog was missing from the pypi distribution, fixed now (#71)
* fixed `Crossref.registration_agency()` method, borked it up on a previous change (#72)
* set encoding on response text for `content_negotiation()` method to UTF-8 to fix encoding issues (#73)
* fix `Crossref.filter_names()` method; no sort on `dict_keys` (#76)

0.6.0 (2017-10-20)
--------------------
* Added verification and docs for additional Crossref search filters (#62)
* Big improvement to docs on readthedocs (#59)
* Added `mailto` support (#68) (#63) and related added docs about polite pool (#66)
* Added support for `select` parameter (#65)
* Added all new `/works` route filters, and simplified filter option handling within library (#60)

0.5.0 (2017-07-20)
--------------------
* Now using `vcrpy` to mock all unit tests (#54)
* Can now set your own base URL for content negotation (#37)
* Some field queries with `works()` were failing, but now seem to be working, likely due to fixes in Crossref API (#53)
* style input to `content_negotiation` was fixed (#57) (#58) thanks @talbertc-usgs
* Fix to `content_negotiation` when inputting a DOI as a unicode string (#56)

0.3.0 (2017-05-21)
--------------------
* Added more documentation for field queries, describing available fields that support field queries, and how to do field queries (#50)
* `sample` parameter maximum value is 100 - has been for a while, but wasn't updated in Crossref docs (#44)
* Updated docs that `facet` parameter can be a string query in addition to a boolean (#49)
* Documented new 10,000 max value for `/works` requests - that is, for the `offset` parameter - if you need more results than that use `cursor` (see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#deep-paging-with-cursors) (#47)
* Added to docs a bit about rate limiting, their current values, that they can change, and how to show them in verbose curl responses (#45)
* Now using `https://doi.org` for `cn.content_negotation` - and function gains new parameter `url` to  specify different base URLs for content negotiation (#36)
* Fixes to kwargs and fix docs for what can be passed to kwargs  (#41)
* Duplicated names passed to `filter` were not working - fixed now (#48)
* Raise proper HTTP errors when appropriate for `cn.content_negotiation` thanks @jmaupetit (#55)

0.2.6 (2016-06-24)
--------------------
* fixed problem with `cr.works()` where DOIs passed weren't making the correct API request to Crossref (#40)
* added support for field queries to all methods that support `/works` (<https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#field-queries>) (#38)

0.2.2 (2016-03-09)
--------------------
* fixed some example code that included non-working examples (#34)
* fixed bug in `registration_agency()` method, works now! (#35)
* removed redundant `filter_names` and `filter_details` bits in docs

0.2.0 (2016-02-10)
--------------------
* user-agent strings now passed in every http request to Crossref, including a `X-USER-AGENT` header in case the `User-Agent` string is lost (#33)
* added a disclaimer to docs about what is actually searched when searching the Crossref API - that is, only what is returned in the API, so no full text or abstracts are searched (#32)
* improved http error parsing - now passes on the hopefully meaningful error messages from the Crossref API (#31)
* more tests added (#30)
* habanero now supports cursor for deep paging. note that cursor only works with requests to the `/works` route (#18)

0.1.3 (2015-12-02)
--------------------
* Fix wheel file to be a universal to install on python2 and python3 (#25)
* Added method `csl_styles` to get CSL styles for use in content negotiation (#27)
* More documentation for content negotiation (#26)
* Made note in docs that `sample` param ignored unless `/works` used (#24)
* Made note in docs that funders without IDs don't show up on the `/funders` route (#23)

0.1.1 (2015-11-17)
--------------------
* Fix readme

0.1.0 (2015-11-17)
--------------------
* Now compatible with Python 2x and 3x
* `agency()` method changed to `registration_agency()`
* New method `citation_count()` - get citation counts for DOIs
* New method `crosscite()` - get a citation for DOIs, only supports simple text format
* New method `random_dois()` - get a random set of DOIs
* Now importing `xml.dom` to do small amount of XML parsing
* Changed library structure, now with module system, separated into modules for the main Crossref search API (i.e., `api.crossref.org`) including higher level methods (e.g., `registration_agency`), content negotiation, and citation counts.

0.0.6 (2015-11-09)
--------------------
* First pypi release
