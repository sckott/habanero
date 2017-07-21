"""Tests for Crossref.types"""
import os
import vcr
from nose.tools import *

from habanero import exceptions

from habanero import Crossref
cr = Crossref()

a = {u'items': [{u'id': u'book-section', u'label': u'Book Section'},
  {u'id': u'monograph', u'label': u'Monograph'},
  {u'id': u'report', u'label': u'Report'},
  {u'id': u'book-track', u'label': u'Book Track'},
  {u'id': u'journal-article', u'label': u'Journal Article'},
  {u'id': u'book-part', u'label': u'Part'},
  {u'id': u'other', u'label': u'Other'},
  {u'id': u'book', u'label': u'Book'},
  {u'id': u'journal-volume', u'label': u'Journal Volume'},
  {u'id': u'book-set', u'label': u'Book Set'},
  {u'id': u'reference-entry', u'label': u'Reference Entry'},
  {u'id': u'proceedings-article', u'label': u'Proceedings Article'},
  {u'id': u'journal', u'label': u'Journal'},
  {u'id': u'component', u'label': u'Component'},
  {u'id': u'book-chapter', u'label': u'Book Chapter'},
  {u'id': u'report-series', u'label': u'Report Series'},
  {u'id': u'proceedings', u'label': u'Proceedings'},
  {u'id': u'standard', u'label': u'Standard'},
  {u'id': u'reference-book', u'label': u'Reference Book'},
  {u'id': u'posted-content', u'label': u'Posted Content'},
  {u'id': u'journal-issue', u'label': u'Journal Issue'},
  {u'id': u'dissertation', u'label': u'Dissertation'},
  {u'id': u'dataset', u'label': u'Dataset'},
  {u'id': u'book-series', u'label': u'Book Series'},
  {u'id': u'edited-book', u'label': u'Edited Book'},
  {u'id': u'standard-series', u'label': u'Standard Series'}],
 u'total-results': 26}

@vcr.use_cassette('test/vcr_cassettes/types.yaml')
def test_types():
    "types - basic test"
    res = cr.types()
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert a == res['message']

@vcr.use_cassette('test/vcr_cassettes/types_query.yaml')
def test_types_query():
    "types - param: query - doesn't do anything without works"
    res = cr.types(query = "journal")
    assert a == res['message']

@vcr.use_cassette('test/vcr_cassettes/types_ids.yaml')
def test_types_ids():
    "types - param: ids"
    res = cr.types(ids = "journal")
    assert dict == res.__class__
    assert {u'id': u'journal', u'label': u'Journal'} == res['message']

@vcr.use_cassette('test/vcr_cassettes/types_works.yaml')
def test_types_works():
    "types - param: works"
    res = cr.types(ids = "journal", works = True, limit = 2)
    assert dict == res.__class__
    assert 'work-list' == res['message-type']

# FIXME: not sure why, but the line where we get titles obj is failing with
#   UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 109: ordinal not in range(128)
# def test_types_field_queries():
#     "types - param: kwargs - field queries work as expected"
#     res = cr.types(ids = "journal-article", works = True, query_title = 'gender', rows = 20)
#     titles = [ str(x.get('title')[0]) for x in res['message']['items'] ]
#     assert dict == res.__class__
#     assert 5 == len(res['message'])
#     assert list == titles.__class__
#     assert str == titles[0].__class__

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/types_filters_not_allowed_with_typeid.yaml')
def test_types_query_filters_not_allowed_with_typeid():
    "types - param: kwargs - query filters not allowed on types/type/ route"
    cr.types(ids = "journal-article", query_title = 'gender')

