import pytest
from httpx import HTTPError

from habanero import Crossref, exceptions

cr = Crossref()


@pytest.mark.vcr
def test_journals():
    """journals - basic test"""
    res = cr.journals(limit=1)
    assert isinstance(res, dict)
    assert isinstance(res["message"], dict)
    assert 1 == res["message"]["items-per-page"]


@pytest.mark.vcr
def test_journals_query():
    """journals - param: query"""
    res = cr.journals(query="ecology", limit=2)
    assert isinstance(res, dict)
    assert 2 == res["message"]["items-per-page"]
    assert "journal-list" == res["message-type"]


@pytest.mark.vcr
def test_journals_ids():
    """journals - param: ids"""
    res = cr.journals(ids=["1803-2427", "2326-4225"])
    assert isinstance(res, list)
    assert isinstance(res[0], dict)
    assert "journal" == res[0]["message-type"]


@pytest.mark.vcr
def test_journals_works():
    """journals - param: works"""
    res1 = cr.journals(
        ids="2167-8359", query="ecology", works=True, sort="score", order="asc"
    )
    scores1 = [x["score"] for x in res1["message"]["items"]]
    res2 = cr.journals(
        ids="2167-8359", query="ecology", works=True, sort="score", order="desc"
    )
    scores2 = [x["score"] for x in res2["message"]["items"]]
    assert isinstance(res1, dict)
    assert "work-list" == res1["message-type"]
    assert max(scores1) == scores1[-1]
    assert min(scores2) == scores2[-1]


@pytest.mark.vcr
def test_journals_filter_fails_noidsworks():
    with pytest.raises(exceptions.RequestError):
        cr.journals(filter={"from_pub_date": "2014-03-03"})


@pytest.mark.vcr
def test_journals_filter_fails_noids():
    with pytest.raises(exceptions.RequestError):
        cr.journals(works=True, filter={"has_assertion": True})


@pytest.mark.vcr
def test_journals_fail_limit():
    with pytest.raises(exceptions.RequestError):
        cr.journals(limit="things")


@pytest.mark.vcr
def test_journals_fail_sort():
    with pytest.raises(exceptions.RequestError):
        cr.journals(sort="things")


@pytest.mark.vcr
def test_journals_field_queries():
    """journals - param: kwargs - field queries work as expected"""
    res = cr.journals(
        ids="2167-8359",
        works=True,
        query_bibliographic="fish",
        filter={"type": "journal-article"},
    )
    titles = [x.get("title")[0] for x in res["message"]["items"]]
    assert isinstance(res, dict)
    assert 5 == len(res["message"])
    assert isinstance(titles, list)
    assert isinstance(titles[0], str)


@pytest.mark.vcr
def test_journals_field_queries_not_allowed_with_dois():
    with pytest.raises(HTTPError):
        cr.journals(ids="2167-8359", query_bibliographic="fish")


@pytest.mark.vcr
def test_journals_bad_id_warn():
    """journals - param: warn"""
    with pytest.warns(UserWarning):
        out = cr.journals(ids="4444-4444", warn=True)
    assert out is None


@pytest.mark.vcr
def test_journals_mixed_ids_warn():
    """journals - param: warn"""
    with pytest.warns(UserWarning):
        out = cr.journals(ids=["1803-2427", "4444-4444"], warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None


@pytest.mark.vcr
def test_journals_bad_id_works_warn():
    """journals - param: warn"""
    with pytest.warns(UserWarning):
        out = cr.journals(ids="4444-4444", works=True, warn=True)
    assert out is None


@pytest.mark.vcr
def test_journals_mixed_ids_works_warn():
    """""journals - param: warn""" ""
    with pytest.warns(UserWarning):
        out = cr.journals(
            ids=["1803-2427", "4444-4444", "2167-8359"], works=True, warn=True
        )
    assert len(out) == 3
    assert len([x for x in out if x]) == 2
    assert isinstance(out[0], dict)
    assert isinstance(out[2], dict)
    assert out[1] is None
