"""Tests for Crossref.licenses"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

def test_licenses():
    "licenses - basic test"
    res = cr.licenses()
    assert dict == res.__class__
    assert 130 < len(res['message']['items'])

def test_licenses_query():
    "licenses - param: query - doesn't do anything without works"
    res = cr.licenses(query = "aps")
    assert {u'search-terms': u'aps', u'start-index': 0} == res['message']['query']
