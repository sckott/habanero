import pytest
import os
import vcr
from habanero import exceptions, Crossref
from requests import exceptions as ex

cr = Crossref()


@pytest.mark.vcr
def test_cursor():
    "cursor works - basic test"
    res = cr.works(query="widget", cursor="*", cursor_max=10)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 4 == len(res)
    assert 6 == len(res["message"])


@pytest.mark.vcr
def test_cursor_max():
    "cursor works - cursor_max works"
    res1 = cr.works(query="widget", cursor="*", cursor_max=60)
    items1 = [z["message"]["items"] for z in res1]
    items1 = [item for sublist in items1 for item in sublist]
    res2 = cr.works(query="widget", cursor="*", cursor_max=40)
    items2 = [z["message"]["items"] for z in res2]
    items2 = [item for sublist in items2 for item in sublist]
    assert list == res1.__class__
    assert list == res2.__class__
    assert 60 == len(items1)
    assert 40 == len(items2)


@pytest.mark.vcr
def test_cursor_fails_cursor_value():
    with pytest.raises(ex.HTTPError):
        cr.works(query="widget", cursor="thing")


@pytest.mark.vcr
def test_cursor_fails_cursor_max():
    with pytest.raises(ValueError):
        cr.works(query="widget", cursor="*", cursor_max="thing")
