"""Tests for cursor"""
import os
from habanero import Crossref
cr = Crossref()

def test_cursor_works():
    "cursor works - basic test"
    res = cr.works(query = "widget", cursor = "*", cursor_max = 10)
    assert dict == res.__class__
    assert dict == res['message'].__class__
    assert 4 == len(res)
    assert 6 == len(res['message'])
