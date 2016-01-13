"""Tests for Crossref.journals"""
import os
from nose.tools import *
from habanero import exceptions

from habanero import Crossref
cr = Crossref()

def test_journals():
    "journals - basic test"
    res = cr.journals(limit = 1)
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert 1 == res['message']['items-per-page']

def test_journals_query():
    "journals - param: query"
    res = cr.journals(query = "ecology", limit = 2)
    assert dict == res.__class__
    assert 2 == res['message']['items-per-page']
    assert 'journal-list' == res['message-type']

def test_journals_ids():
    "journals - param: ids"
    res = cr.journals(ids = ['1803-2427', '2326-4225'])
    assert list == res.__class__
    assert dict == res[0].__class__
    assert 'journal' == res[0]['message-type']

def test_journals_works():
    "journals - param: works"
    res1 = cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "asc")
    scores1 = [ x['score'] for x in res1['message']['items'] ]
    res2 = cr.journals(ids = "2167-8359", query = 'ecology', works = True, sort = 'score', order = "desc")
    scores2 = [ x['score'] for x in res2['message']['items'] ]
    assert dict == res1.__class__
    assert 'work-list' == res1['message-type']
    assert max(scores1) == scores1[-1]
    assert min(scores2) == scores2[-1]

@raises(exceptions.RequestError)
def test_journals_filter_fails_noidsworks():
    "journals - filter fails, no ids or works"
    cr.journals(filter = {'from_pub_date': '2014-03-03'})

@raises(exceptions.RequestError)
def test_journals_filter_fails_noidsworks():
    "journals - filter fails, no ids or works"
    cr.journals(filter = {'from_pub_date': '2014-03-03'})

@raises(exceptions.RequestError)
def test_journals_filter_fails_noids():
    "journals - filter fails, no ids"
    cr.journals(works = True, filter = {'has_assertion': True})

@raises(exceptions.RequestError)
def test_journals_fail_limit():
    "journals - fails on wrong input type to limit"
    cr.journals(limit = 'things')

@raises(exceptions.RequestError)
def test_journals_fail_offset():
    "journals - fails on wrong input type to offset"
    cr.journals(offset = 'things')

@raises(exceptions.RequestError)
def test_journals_fail_sort():
    "journals - fails on wrong input type to offset"
    cr.journals(sort = 'things')
