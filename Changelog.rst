.. _changelog:

Changelog
=========

0.1.0 (2015-11-17)
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
* Changed library structure, now with module system, separated into modules for
the main Crossref search API (i.e., `api.crossref.org`) including higher level methods
(e.g., `registration_agency`), content negotiation, and citation counts.

0.0.6 (2015-11-09)
--------------------
* First pypi release
