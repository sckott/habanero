from typing import no_type_check

import pytest

from habanero import Crossref
from habanero.filterhandler import filter_handler

cr = Crossref()


def test_filter_names():
    """filter_names"""
    res_works = cr.filter_names()
    res_members = cr.filter_names(route="members")
    res_funders = cr.filter_names(route="funders")
    assert isinstance(res_works, list)
    assert isinstance(res_works[0], str)
    assert isinstance(res_members, list)
    assert isinstance(res_members[0], str)
    assert len(res_members) == 3
    assert isinstance(res_funders, list)
    assert isinstance(res_funders[0], str)
    assert len(res_funders) == 1


@no_type_check
def test_filter_names_errors():
    with pytest.raises(ValueError):
        cr.filter_names("adf")
        cr.filter_names(5)


def test_filter_details():
    """filter_details"""
    res_works = cr.filter_details()
    res_members = cr.filter_details(route="members")
    res_funders = cr.filter_details(route="funders")
    assert isinstance(res_works, dict)
    assert isinstance(res_members, dict)
    assert isinstance(res_funders, dict)


@no_type_check
def test_filter_details_errors():
    with pytest.raises(ValueError):
        cr.filter_details("adf")
        cr.filter_details(5)


def test_filter_handler_dotted_names():
    """filter names that Crossref spells with a dot"""
    assert filter_handler({"relation_type": "is-preprint-of"}) == (
        "relation.type:is-preprint-of"
    )
    assert filter_handler({"relation_object": "10.1101/2020.03.22.002386"}) == (
        "relation.object:10.1101/2020.03.22.002386"
    )
    assert filter_handler({"relation_object_type": "doi"}) == (
        "relation.object-type:doi"
    )
    assert filter_handler({"full_text_application": "text-mining"}) == (
        "full-text.application:text-mining"
    )
    assert filter_handler({"award_funder": "10.13039/100000001"}) == (
        "award.funder:10.13039/100000001"
    )
