import pytest

from habanero import Crossref

cr = Crossref()


def test_filter_names():
    """filter_names"""
    res_works = cr.filter_names()
    res_members = cr.filter_names("members")
    res_funders = cr.filter_names("funders")
    assert isinstance(res_works, list)
    assert isinstance(res_works[0], str)
    assert isinstance(res_members, list)
    assert isinstance(res_members[0], str)
    assert 4 == len(res_members)
    assert isinstance(res_funders, list)
    assert isinstance(res_funders[0], str)
    assert 1 == len(res_funders)


def test_filter_names_errors():
    with pytest.raises(ValueError):
        cr.filter_names("adf")
        cr.filter_names(5)


def test_filter_details():
    """filter_details"""
    res_works = cr.filter_details()
    res_members = cr.filter_details("members")
    res_funders = cr.filter_details("funders")
    assert isinstance(res_works, dict)
    assert isinstance(res_members, dict)
    assert isinstance(res_funders, dict)


def test_filter_details_errors():
    with pytest.raises(ValueError):
        cr.filter_details("adf")
        cr.filter_details(5)
