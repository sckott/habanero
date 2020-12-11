"""Tests for Crossref.journals"""
import pytest
import os
import vcr
from habanero import exceptions
from habanero import Crossref

cr = Crossref()


@vcr.use_cassette("test/vcr_cassettes/journals.yaml")
def test_journals():
    "journals - basic test"
    res = cr.journals(limit=1)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 1 == res["message"]["items-per-page"]


@vcr.use_cassette("test/vcr_cassettes/journals_query.yaml")
def test_journals_query():
    "journals - param: query"
    res = cr.journals(query="ecology", limit=2)
    assert dict == res.__class__
    assert 2 == res["message"]["items-per-page"]
    assert "journal-list" == res["message-type"]


@vcr.use_cassette("test/vcr_cassettes/journals_ids.yaml")
def test_journals_ids():
    "journals - param: ids"
    res = cr.journals(ids=["1803-2427", "2326-4225"])
    assert list == res.__class__
    assert dict == res[0].__class__
    assert "journal" == res[0]["message-type"]


@vcr.use_cassette("test/vcr_cassettes/journals_works.yaml")
def test_journals_works():
    "journals - param: works"
    res1 = cr.journals(
        ids="2167-8359", query="ecology", works=True, sort="score", order="asc"
    )
    scores1 = [x["score"] for x in res1["message"]["items"]]
    res2 = cr.journals(
        ids="2167-8359", query="ecology", works=True, sort="score", order="desc"
    )
    scores2 = [x["score"] for x in res2["message"]["items"]]
    assert dict == res1.__class__
    assert "work-list" == res1["message-type"]
    assert max(scores1) == scores1[-1]
    assert min(scores2) == scores2[-1]


@vcr.use_cassette("test/vcr_cassettes/journals_filter_fails_noidsworks.yaml")
def test_journals_filter_fails_noidsworks():
    with pytest.raises(exceptions.RequestError):
        cr.journals(filter={"from_pub_date": "2014-03-03"})


@vcr.use_cassette("test/vcr_cassettes/journals_filter_fails_noidsworks.yaml")
def test_journals_filter_fails_noidsworks():
    with pytest.raises(exceptions.RequestError):
        cr.journals(filter={"from_pub_date": "2014-03-03"})


@vcr.use_cassette("test/vcr_cassettes/journals_filter_fails_noids.yaml")
def test_journals_filter_fails_noids():
    with pytest.raises(exceptions.RequestError):
        cr.journals(works=True, filter={"has_assertion": True})


@vcr.use_cassette("test/vcr_cassettes/journals_fail_limit.yaml")
def test_journals_fail_limit():
    with pytest.raises(exceptions.RequestError):
        cr.journals(limit="things")


@vcr.use_cassette("test/vcr_cassettes/journals_fail_offset.yaml")
def test_journals_fail_offset():
    with pytest.raises(exceptions.RequestError):
        cr.journals(offset="things")


@vcr.use_cassette("test/vcr_cassettes/journals_fail_sort.yaml")
def test_journals_fail_sort():
    with pytest.raises(exceptions.RequestError):
        cr.journals(sort="things")


@vcr.use_cassette("test/vcr_cassettes/journals_field_queries.yaml")
def test_journals_field_queries():
    "journals - param: kwargs - field queries work as expected"
    res = cr.journals(
        ids="2167-8359",
        works=True,
        query_bibliographic="fish",
        filter={"type": "journal-article"},
    )
    titles = [x.get("title")[0] for x in res["message"]["items"]]
    assert dict == res.__class__
    assert 5 == len(res["message"])
    assert list == titles.__class__
    assert str == str(titles[0]).__class__


@vcr.use_cassette(
    "test/vcr_cassettes/journals_field_queries_not_allowed_with_dois.yaml"
)
def test_journals_field_queries_not_allowed_with_dois():
    with pytest.raises(exceptions.RequestError):
        res = cr.journals(ids="2167-8359", query_bibliographic="fish")


@vcr.use_cassette("test/vcr_cassettes/journals_query_title_not_allowed_anymore.yaml")
def test_journals_query_title_not_allowed_anymore():
    with pytest.raises(exceptions.RequestError):
        res = cr.journals(query_title="cellular")
