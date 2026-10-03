from typing import no_type_check

import httpx2
import pytest

from habanero import Crossref
from habanero.exceptions import IncompatibleParameterError
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


def _stub_crossref():
    """A Crossref whose client records query params and makes no real request"""
    calls = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        calls.append(dict(request.url.params))
        body = {
            "status": "ok",
            "message": {"items": [], "total-results": 0},
        }
        return httpx2.Response(200, json=body)

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Crossref(client=client), calls


def test_filter_kwarg_raises():
    """using `filter` instead of `filters` raises, and no request is made"""
    stub, calls = _stub_crossref()
    with pytest.raises(IncompatibleParameterError, match="filters"):
        stub.works(filter={"has_full_text": True})
    assert calls == []


def test_filter_kwarg_raises_with_ids():
    """the `filter` error also applies when ids are passed"""
    stub, calls = _stub_crossref()
    with pytest.raises(IncompatibleParameterError, match="filters"):
        stub.works(ids="10.1371/journal.pone.0033693", filter={"has_full_text": True})
    assert calls == []


def test_filter_kwarg_raises_other_routes():
    """the `filter` error applies to other routes too"""
    stub, calls = _stub_crossref()
    with pytest.raises(IncompatibleParameterError, match="filters"):
        stub.members(filter={"has_public_references": True})
    with pytest.raises(IncompatibleParameterError, match="filters"):
        stub.funders(filter={"location": "Sweden"})
    assert calls == []


def test_filters_kwarg_does_not_raise():
    """using `filters` correctly works, and the filter is sent"""
    stub, calls = _stub_crossref()
    stub.works(filters={"has_full_text": True})
    assert calls[0]["filter"] == "has-full-text:true"


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
