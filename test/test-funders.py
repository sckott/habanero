"""Tests for Crossref.funders"""
import pytest
import os
import vcr
import requests
from habanero import exceptions

from habanero import Crossref

cr = Crossref()


@vcr.use_cassette("test/vcr_cassettes/funders.yaml")
def test_funders():
    "funders - basic test"
    res = cr.funders(limit=2)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 2 == res["message"]["items-per-page"]


@vcr.use_cassette("test/vcr_cassettes/funders_query.yaml")
def test_funders_query():
    "funders - param: query"
    res = cr.funders(query="NSF", limit=2)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 2 == res["message"]["items-per-page"]


@vcr.use_cassette("test/vcr_cassettes/funders_sample_err.yaml")
def test_funders_sample_err():
    with pytest.raises(exceptions.RequestError):
        cr.funders(sample=2)


@vcr.use_cassette("test/vcr_cassettes/funders_filter_fails_noidsworks.yaml")
def test_funders_filter_fails_noidsworks():
    with pytest.raises(exceptions.RequestError):
        cr.funders(filter={"from_pub_date": "2014-03-03"})


@vcr.use_cassette("test/vcr_cassettes/funders_filter_fails_noids.yaml")
def test_funders_filter_fails_noids():
    with pytest.raises(exceptions.RequestError):
        cr.funders(works=True, filter={"has_assertion": True})


@vcr.use_cassette("test/vcr_cassettes/funders_filter_works.yaml")
def test_funders_filter_works():
    "funders - filter works when used with id and works=True"
    res = cr.funders(
        ids="10.13039/100000001", works=True, filter={"has_assertion": True}
    )
    assert dict == res.__class__
    assert 20 == res["message"]["items-per-page"]


@vcr.use_cassette("test/vcr_cassettes/funders_err_fail_limit.yaml")
def test_funders_fail_limit():
    with pytest.raises(exceptions.RequestError):
        cr.funders(limit="things")


@vcr.use_cassette("test/vcr_cassettes/funders_err_fail_offset.yaml")
def test_funders_fail_offset():
    with pytest.raises(exceptions.RequestError):
        cr.funders(offset="things")


@vcr.use_cassette("test/vcr_cassettes/funders_err_fail_sort.yaml")
def test_funders_fail_sort():
    with pytest.raises(exceptions.RequestError):
        cr.funders(sort="things")


@vcr.use_cassette("test/vcr_cassettes/funders_field_queries.yaml")
def test_funders_field_queries():
    "funders - param: kwargs - field queries work as expected"
    res = cr.funders(
        ids="10.13039/100000001",
        works=True,
        query_container_title="engineering",
        filter={"type": "journal-article"},
        limit=100,
    )
    titles = [x.get("title") for x in res["message"]["items"]]
    assert dict == res.__class__
    assert 5 == len(res["message"])
    assert list == titles.__class__
    assert 100 == len(titles)


@vcr.use_cassette("test/vcr_cassettes/funders_filters_not_allowed_with_dois.yaml")
def test_funders_query_filters_not_allowed_with_dois():
    with pytest.raises(exceptions.RequestError):
        cr.funders(ids="10.13039/100000001", query_container_title="engineering")


@vcr.use_cassette("test/vcr_cassettes/funders_query_title_not_allowed_anymore.yaml")
def test_funders_query_title_not_allowed_anymore():
    with pytest.raises(requests.exceptions.HTTPError):
        res = cr.funders(ids="10.13039/100000001", works=True, query_title="cellular")
