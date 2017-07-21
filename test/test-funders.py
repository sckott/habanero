"""Tests for Crossref.funders"""
import os
import vcr
from nose.tools import *
from habanero import exceptions

from habanero import Crossref
cr = Crossref()

@vcr.use_cassette('test/vcr_cassettes/funders.yaml')
def test_funders():
    "funders - basic test"
    res = cr.funders(limit = 2)
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert 2 == res['message']['items-per-page']

@vcr.use_cassette('test/vcr_cassettes/funders_query.yaml')
def test_funders_query():
    "funders - param: query"
    res = cr.funders(query = "NSF", limit = 2)
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert 2 == res['message']['items-per-page']

@vcr.use_cassette('test/vcr_cassettes/funders_sample.yaml')
def test_funders_sample():
    "funders - param: sample - ignored b/c works not requested"
    res = cr.funders(sample = 2)
    assert dict == res.__class__
    assert 20 == res['message']['items-per-page']

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_filter_fails_noidsworks.yaml')
def test_funders_filter_fails_noidsworks():
    "funders - filter fails, no ids or works"
    cr.funders(filter = {'from_pub_date': '2014-03-03'})

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_filter_fails_noids.yaml')
def test_funders_filter_fails_noids():
    "funders - filter fails, no ids"
    cr.funders(works = True, filter = {'has_assertion': True})

@vcr.use_cassette('test/vcr_cassettes/funders_filter_works.yaml')
def test_funders_filter_works():
    "funders - filter works when used with id and works=True"
    res = cr.funders(ids = '10.13039/100000001', works = True, filter = {'has_assertion': True})
    assert dict == res.__class__
    assert 20 == res['message']['items-per-page']

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_err_fail_limit.yaml')
def test_funders_fail_limit():
    "funders - fails on wrong input type to limit"
    cr.funders(limit = 'things')

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_err_fail_offset.yaml')
def test_funders_fail_offset():
    "funders - fails on wrong input type to offset"
    cr.funders(offset = 'things')

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_err_fail_sort.yaml')
def test_funders_fail_sort():
    "funders - fails on wrong input type to offset"
    cr.funders(sort = 'things')

@vcr.use_cassette('test/vcr_cassettes/funders_field_queries.yaml')
def test_funders_field_queries():
    "funders - param: kwargs - field queries work as expected"
    res = cr.funders(ids = "10.13039/100000001", works = True, query_container_title = 'engineering', filter = {'type': 'journal-article'}, limit = 100)
    titles = [ x.get('title') for x in res['message']['items'] ]
    assert dict == res.__class__
    assert 5 == len(res['message'])
    assert list == titles.__class__
    assert 100 == len(titles)

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/funders_filters_not_allowed_with_dois.yaml')
def test_funders_query_filters_not_allowed_with_dois():
    "funders - param: kwargs - query filters not allowed on works/funderid/ route"
    cr.funders(ids = "10.13039/100000001", query_container_title = 'engineering')
