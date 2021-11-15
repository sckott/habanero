import pytest
import os
import requests
from habanero import exceptions, Crossref
from requests.exceptions import HTTPError

cr = Crossref()


@pytest.mark.vcr
def test_funders():
    "funders - basic test"
    res = cr.funders(limit=2)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 2 == res["message"]["items-per-page"]


@pytest.mark.vcr
def test_funders_query():
    "funders - param: query"
    res = cr.funders(query="NSF", limit=2)
    assert dict == res.__class__
    assert dict == res["message"].__class__
    assert 2 == res["message"]["items-per-page"]


@pytest.mark.vcr
def test_funders_sample_err():
    with pytest.raises(exceptions.RequestError):
        cr.funders(sample=2)


@pytest.mark.vcr
def test_funders_filter_fails_noidsworks():
    with pytest.raises(exceptions.RequestError):
        cr.funders(filter={"from_pub_date": "2014-03-03"})


@pytest.mark.vcr
def test_funders_filter_fails_noids():
    with pytest.raises(exceptions.RequestError):
        cr.funders(works=True, filter={"has_assertion": True})


@pytest.mark.vcr
def test_funders_filter_works():
    "funders - filter works when used with id and works=True"
    res = cr.funders(
        ids="10.13039/100000001", works=True, filter={"has_assertion": True}
    )
    assert dict == res.__class__
    assert 20 == res["message"]["items-per-page"]


@pytest.mark.vcr
def test_funders_fail_limit():
    with pytest.raises(KeyError):
        cr.funders(limit="things")


@pytest.mark.vcr
def test_funders_fail_offset():
    with pytest.raises(KeyError):
        cr.funders(offset="things")


@pytest.mark.vcr
def test_funders_fail_sort():
    with pytest.raises(exceptions.RequestError):
        cr.funders(sort="things")


@pytest.mark.vcr
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


@pytest.mark.vcr
def test_funders_query_filters_not_allowed_with_dois():
    with pytest.raises(HTTPError):
        cr.funders(ids="10.13039/100000001", query_container_title="engineering")


@pytest.mark.vcr
def test_funders_bad_id_warn():
    "funders - param: warn"
    with pytest.warns(UserWarning):
        out = cr.funders(ids="10.13039/notarealdoi", warn=True)
    assert out is None


@pytest.mark.vcr
def test_funders_mixed_ids_warn():
    "funders - param: warn"
    with pytest.warns(UserWarning):
        out = cr.funders(ids=["10.13039/100000001", "10.13039/notarealdoi"], warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None


@pytest.mark.vcr
def test_funders_bad_id_works_warn():
    "funders - param: warn"
    with pytest.warns(UserWarning):
        out = cr.funders(ids="10.13039/notarealdoi", works=True, warn=True)
    assert out is None


@pytest.mark.vcr
def test_funders_mixed_ids_works_warn():
    "funders - param: warn"
    with pytest.warns(UserWarning):
        out = cr.funders(
            ids=["10.13039/100000001", "10.13039/notarealdoi"], works=True, warn=True
        )
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None
