"""Tests for Crossref.journals"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

a = {u'items': [{u'ISSN': [u'2151-7290'],
   u'breakdowns': {u'dois-by-issued-year': [[2010, 28],
     [2012, 25],
     [2013, 23],
     [2011, 23],
     [2009, 13]]},
   u'counts': {u'backfile-dois': 89, u'current-dois': 0, u'total-dois': 89},
   u'coverage': {u'award-numbers-backfile': 0.0,
    u'award-numbers-current': 0,
    u'funders-backfile': 0.0,
    u'funders-current': 0,
    u'licenses-backfile': 0.0,
    u'licenses-current': 0,
    u'orcids-backfile': 0.0,
    u'orcids-current': 0,
    u'references-backfile': 0.0,
    u'references-current': 0,
    u'resource-links-backfile': 0.0,
    u'resource-links-current': 0,
    u'update-policies-backfile': 0.0,
    u'update-policies-current': 0},
   u'flags': {u'deposits': True,
    u'deposits-articles': True,
    u'deposits-award-numbers-backfile': False,
    u'deposits-award-numbers-current': False,
    u'deposits-funders-backfile': False,
    u'deposits-funders-current': False,
    u'deposits-licenses-backfile': False,
    u'deposits-licenses-current': False,
    u'deposits-orcids-backfile': False,
    u'deposits-orcids-current': False,
    u'deposits-references-backfile': False,
    u'deposits-references-current': False,
    u'deposits-resource-links-backfile': False,
    u'deposits-resource-links-current': False,
    u'deposits-update-policies-backfile': False,
    u'deposits-update-policies-current': False},
   u'last-status-check-time': 1448348435222,
   u'publisher': u'Muse - Johns Hopkins University Press',
   u'title': u'a/b Auto/Biography Studies'}],
 u'items-per-page': 1,
 u'query': {u'search-terms': None, u'start-index': 0},
 u'total-results': 43208}

def test_journals():
    "journals - basic test"
    res = cr.journals(limit = 1)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 'dict' == res.message().__class__.__name__
    assert a == res.message()

def test_journals_query():
    "journals - param: query"
    res = cr.journals(query = "ecology", limit = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 2 == res.result['message']['items-per-page']
    assert 'journal-list' == res.result['message-type']

def test_journals_ids():
    "journals - param: ids"
    res = cr.journals(ids = ['1803-2427', '2326-4225'])
    assert 'ok' == res[0].status()
    assert 'list' == res.__class__.__name__
    assert 'NoWorks' == res[0].__class__.__name__
    assert 'journal' == res[0].result['message-type']

def test_journals_works():
    "journals - param: works"
    res1 = cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "asc")
    scores1 = [ x['score'] for x in res1.result['message']['items'] ]
    res2 = cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "desc")
    scores2 = [ x['score'] for x in res2.result['message']['items'] ]
    assert 'ok' == res1.status()
    assert 'Works' == res1.__class__.__name__
    assert 'work-list' == res1.result['message-type']
    assert max(scores1) == scores1[-1]
    assert min(scores2) == scores2[-1]
