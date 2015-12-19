Changelog
=========

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
