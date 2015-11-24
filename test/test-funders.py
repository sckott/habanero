"""Tests for Crossref.funders"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

a = {u'items': [{u'alt-names': [u'EMBO'],
   u'id': u'100004410',
   u'location': u'Germany',
   u'name': u'European Molecular Biology Organization',
   u'replaced-by': [],
   u'replaces': [],
   u'tokens': [u'european',
    u'molecular',
    u'biology',
    u'organization',
    u'embo'],
   u'uri': u'http://dx.doi.org/10.13039/100004410'},
  {u'alt-names': [u'AERA'],
   u'id': u'100005165',
   u'location': u'United States',
   u'name': u'American Educational Research Association',
   u'replaced-by': [],
   u'replaces': [],
   u'tokens': [u'american',
    u'educational',
    u'research',
    u'association',
    u'aera'],
   u'uri': u'http://dx.doi.org/10.13039/100005165'}],
 u'items-per-page': 2,
 u'query': {u'search-terms': None, u'start-index': 0},
 u'total-results': 10902}

def test_funders():
    "funders - basic test"
    res = cr.funders(limit = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 'dict' == res.message().__class__.__name__
    assert a == res.message()

def test_funders_query():
    "funders - param: query"
    res = cr.funders(query = "NSF", limit = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 2 == res.result['message']['items-per-page']

def test_funders_sample():
    "funders - param: sample - ignored b/c works not requested"
    res = cr.funders(sample = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 20 == res.result['message']['items-per-page']
