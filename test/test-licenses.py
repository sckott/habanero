"""Tests for Crossref.licenses"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

a = {u'items': [{u'URL': u'http://creativecommons.org/licenses/by-nc-nd/3.0/',
   u'work-count': 9},
  {u'URL': u'http://creativecommons.org/licenses/by-nc-nd/4.0/',
   u'work-count': 4},
  {u'URL': u'http://creativecommons.org/licenses/by-nc-sa/4.0',
   u'work-count': 1},
  {u'URL': u'http://creativecommons.org/licenses/by/3.0/', u'work-count': 6},
  {u'URL': u'http://creativecommons.org/licenses/by/4.0/', u'work-count': 3},
  {u'URL': u'http://doi.wiley.com/10.1002/tdm_license_1', u'work-count': 93},
  {u'URL': u'http://link.aps.org/licenses/aps-default-license',
   u'work-count': 17},
  {u'URL': u'http://onlinelibrary.wiley.com/termsAndConditions',
   u'work-count': 3},
  {u'URL': u'http://www.acm.org/publications/policies/copyright_policy#Background',
   u'work-count': 1},
  {u'URL': u'http://www.elsevier.com/open-access/userlicense/1.0/',
   u'work-count': 11},
  {u'URL': u'http://www.elsevier.com/tdm/userlicense/1.0/',
   u'work-count': 456},
  {u'URL': u'https://creativecommons.org/licenses/by-nc/4.0/',
   u'work-count': 199}],
 u'items-per-page': 20,
 u'query': {u'search-terms': u'aps', u'start-index': 0},
 u'total-results': 12}

def test_licenses():
    "types - basic test"
    res = cr.licenses()
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 139 == len(res.result['message']['items'])

def test_licenses_query():
    "types - param: query - doesn't do anything without works"
    res = cr.licenses(query = "aps")
    assert a == res.message()
