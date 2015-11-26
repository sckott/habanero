"""Tests for Crossref.funders"""
import os
from nose.tools import *

from habanero import Crossref
cr = Crossref()

def test_funders():
    "funders - basic test"
    res = cr.funders(limit = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.result.__class__.__name__
    assert 'dict' == res.message().__class__.__name__
    assert 2 == res.message()['items-per-page']

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
