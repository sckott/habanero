"""Tests for Crossref.types"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

a = {u'items': [{u'id': u'book-section', u'label': u'Book Section'},
  {u'id': u'monograph', u'label': u'Monograph'},
  {u'id': u'report', u'label': u'Report'},
  {u'id': u'book-track', u'label': u'Book Track'},
  {u'id': u'journal-article', u'label': None},
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
  {u'id': u'journal-issue', u'label': u'Journal Issue'},
  {u'id': u'dissertation', u'label': u'Dissertation'},
  {u'id': u'dataset', u'label': u'Dataset'},
  {u'id': u'book-series', u'label': u'Book Series'},
  {u'id': u'edited-book', u'label': u'Edited Book'},
  {u'id': u'standard-series', u'label': u'Standard Series'}],
 u'total-results': 25}

def test_types():
    "types - basic test"
    res = cr.types()
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 'dict' == res.message().__class__.__name__
    assert a == res.message()

def test_types_query():
    "types - param: query - doesn't do anything without works"
    res = cr.types(query = "journal")
    assert a == res.message()

def test_types_ids():
    "types - param: ids"
    res = cr.types(ids = "journal")
    assert 'ok' == res.status()
    assert 'NoWorks' == res.__class__.__name__
    assert {u'id': u'journal', u'label': u'Journal'} == res.message()

def test_types_works():
    "types - param: works"
    res = cr.types(ids = "journal", works = True, limit = 2)
    assert 'ok' == res.status()
    assert 'Works' == res.__class__.__name__
    assert 'work-list' == res.result['message-type']
