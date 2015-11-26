"""Tests for Crossref.journals"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

def test_journals():
    "journals - basic test"
    res = cr.journals(limit = 1)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 'dict' == res.message().__class__.__name__
    assert 1 == res.message()['items-per-page']

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
