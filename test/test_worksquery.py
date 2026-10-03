from unittest.mock import patch

import httpx2
import pytest

from habanero import Crossref, WorksQuery

cr = Crossref()
q = WorksQuery(cr)


def test_worksquery_basics():
    """WorksQuery: basic structure"""
    res = q.query("zika").filters(from_pub_date="2020")

    assert isinstance(res, WorksQuery)
    assert hasattr(res, "types")


def test_worksquery_instances_are_immutable():
    """WorksQuery: instances are immutable"""
    base = WorksQuery(cr).query("zika").filters(from_pub_date="2020")
    asc = base.sort("published").order("asc")
    desc = base.sort("published").order("desc")

    assert asc.url != desc.url
    assert "asc" in asc.url
    assert "desc" in desc.url


def test_worksquery_iter_returns_iterable():
    """WorksQuery: iterating yields individual work dicts"""
    fake_items = [{"DOI": "10.1234/a"}, {"DOI": "10.1234/b"}]
    fake_response = {"message": {"items": fake_items}}

    with patch.object(WorksQuery, "execute", return_value=fake_response):
        result = list(q.query("zika"))

    assert isinstance(result, list)
    assert result == fake_items


@pytest.mark.vcr
def test_worksquery_execute():
    """WorksQuery: execute method returns expected response"""
    query = q.query("ecology").select("DOI", "title", "author", "published").limit(3)
    res = query.execute()

    assert isinstance(res, dict)
    assert "message" in res
    assert "items" in res["message"]
    assert len(res["message"]["items"]) == 3


def test_worksquery_same_as_wrapped_method_mocked():
    """WorksQuery: same result as the wrapped method"""
    fake_response = {
        "status": "ok",
        "message": {
            "items": [
                {
                    "DOI": "10.1111/a",
                    "title": ["Ecology A"],
                    "published": {"date-parts": [[2021, 1]]},
                },
                {
                    "DOI": "10.1111/b",
                    "title": ["Ecology B"],
                    "published": {"date-parts": [[2021, 2]]},
                },
                {
                    "DOI": "10.1111/c",
                    "title": ["Ecology C"],
                    "published": {"date-parts": [[2021, 3]]},
                },
            ]
        },
    }

    with patch.object(cr, "works", return_value=fake_response):
        query = q.query("ecology").select("DOI", "title", "published").limit(3)
        result_WorksQuery = query.execute()
        result_works = cr.works(
            query="ecology", select=["DOI", "title", "published"], limit=3
        )

    assert result_WorksQuery == result_works


def _stub_get(monkeypatch):
    """Replace httpx2.get with a stub that records params and makes no request"""
    calls = []

    def fake_get(url, params=None, **kwargs):
        calls.append((url, params))
        body = {
            "status": "ok",
            "message-type": "work-list",
            "message": {"items": [{"DOI": "10.1/a"}], "total-results": 1},
        }
        return httpx2.Response(
            200,
            json=body,
            headers={"Content-Type": "application/json"},
            request=httpx2.Request("GET", url),
        )

    monkeypatch.setattr(httpx2, "get", fake_get)
    return calls


def test_worksquery_filters_accumulates_and_is_immutable():
    """WorksQuery: filters() merges with earlier filters, original unchanged"""
    base = WorksQuery(cr).filters(from_pub_date="2020")
    more = base.filters(has_funder="true")

    assert base._params["filters"] == {"from_pub_date": "2020"}
    assert more._params["filters"] == {"from_pub_date": "2020", "has_funder": "true"}


def test_worksquery_filters_execute_sends_filter(monkeypatch):
    """WorksQuery: execute() with filters() runs and sends the filter param"""
    calls = _stub_get(monkeypatch)
    res = WorksQuery(cr).query("zika").filters(from_pub_date="2020").execute()

    assert res["message"]["items"] == [{"DOI": "10.1/a"}]
    assert len(calls) == 1
    _, params = calls[0]
    assert params["filter"] == "from-pub-date:2020"
    assert params["query"] == "zika"


def test_worksquery_filters_count_sends_filter(monkeypatch):
    """WorksQuery: count() with filters() runs and sends the filter param"""
    calls = _stub_get(monkeypatch)
    n = WorksQuery(cr).filters(from_pub_date="2020", has_funder=True).count()

    assert n == 1
    _, params = calls[0]
    assert params["filter"] == "from-pub-date:2020,has-funder:true"


def test_worksquery_filters_execute_other_endpoint(monkeypatch):
    """WorksQuery: filters() also works for endpoints such as members"""
    calls = _stub_get(monkeypatch)
    WorksQuery(cr).members(98).filters(from_pub_date="2020").execute()

    url, params = calls[0]
    assert url.endswith("/members/98/works")
    assert params["filter"] == "from-pub-date:2020"


@pytest.mark.vcr
def test_worksquery_same_as_wrapped_method_real_requests():
    """WorksQuery: same result as the wrapped method, but real requests"""
    query = q.members(98).select("DOI", "title").limit(3)
    result_WorksQuery = query.execute()
    result_works = cr.members(ids=98, works=True, select=["DOI", "title"], limit=3)

    assert result_WorksQuery == result_works
