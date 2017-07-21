"""Tests for Crossref.licenses"""
import os
import vcr
from nose.tools import *

from habanero import Crossref
cr = Crossref()

@vcr.use_cassette('test/vcr_cassettes/licenses.yaml')
def test_licenses():
    "licenses - basic test"
    res = cr.licenses()
    assert dict == res.__class__
    assert 130 < len(res['message']['items'])

@vcr.use_cassette('test/vcr_cassettes/licenses_query.yaml')
def test_licenses_query():
    "licenses - param: query - doesn't do anything without works"
    res = cr.licenses(query = "aps")
    assert {u'search-terms': u'aps', u'start-index': 0} == res['message']['query']
