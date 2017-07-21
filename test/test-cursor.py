"""Tests for cursor"""
from nose.tools import *
import os
import vcr
from habanero import exceptions
from requests import exceptions as ex

from habanero import Crossref
cr = Crossref()

@vcr.use_cassette('test/vcr_cassettes/cursor.yaml')
def test_cursor():
    "cursor works - basic test"
    res = cr.works(query = "widget", cursor = "*", cursor_max = 10)
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert 4 == len(res)
    assert 6 == len(res['message'])

@vcr.use_cassette('test/vcr_cassettes/cursor_cursormax.yaml')
def test_cursor_max():
    "cursor works - cursor_max works"
    res1 = cr.works(query = "widget", cursor = "*", cursor_max = 60)
    items1 = [ z['message']['items'] for z in res1 ]
    items1 = [ item for sublist in items1 for item in sublist ]
    res2 = cr.works(query = "widget", cursor = "*", cursor_max = 40)
    items2 = [ z['message']['items'] for z in res2 ]
    items2 = [ item for sublist in items2 for item in sublist ]
    assert list == res1.__class__
    assert list == res2.__class__
    assert 60 == len(items1)
    assert 40 == len(items2)

@raises(ex.HTTPError)
@vcr.use_cassette('test/vcr_cassettes/cursor_err1.yaml')
def test_cursor_fails_cursor_value():
    "cursor works - fails when cursor value bad"
    cr.works(query = "widget", cursor = "thing")

@raises(ValueError)
@vcr.use_cassette('test/vcr_cassettes/cursor_err2.yaml')
def test_cursor_fails_cursor_max():
    "cursor works - fails when cursor_max value bad"
    cr.works(query = "widget", cursor = "*", cursor_max = "thing")
