import os
import pytest
from habanero import Crossref
from habanero import RequestError

cr = Crossref()


def test_filter_names():
    "filter_names"
    res_works = cr.filter_names()
    res_members = cr.filter_names("members")
    res_funders = cr.filter_names("funders")
    assert list == res_works.__class__
    assert str == res_works[0].__class__
    assert list == res_members.__class__
    assert str == res_members[0].__class__
    assert 4 == len(res_members)
    assert list == res_funders.__class__
    assert str == res_funders[0].__class__
    assert 1 == len(res_funders)


def test_filter_names_errors():
    with pytest.raises(ValueError):
        cr.filter_names("adf")
        cr.filter_names(5)


def test_filter_details():
    "filter_details"
    res_works = cr.filter_details()
    res_members = cr.filter_details("members")
    res_funders = cr.filter_details("funders")
    assert dict == res_works.__class__
    assert dict == res_members.__class__
    assert dict == res_funders.__class__


def test_filter_details_errors():
    with pytest.raises(ValueError):
        cr.filter_details("adf")
        cr.filter_details(5)
