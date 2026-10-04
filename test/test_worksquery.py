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


def _stub_crossref():
    """A Crossref whose client records (url, params) and makes no real request"""
    calls = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        calls.append((request.url.path, dict(request.url.params)))
        body = {
            "status": "ok",
            "message-type": "work-list",
            "message": {"items": [{"DOI": "10.1/a"}], "total-results": 1},
        }
        return httpx2.Response(200, json=body)

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Crossref(client=client), calls


def _stub_urls():
    """A Crossref whose client records the full URL of each request"""
    urls = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        urls.append(str(request.url))
        body = {
            "status": "ok",
            "message-type": "work-list",
            "message": {"items": [], "total-results": 0},
        }
        return httpx2.Response(200, json=body)

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Crossref(client=client), urls


@pytest.mark.parametrize(
    "build",
    [
        lambda w: w.query("zika"),
        lambda w: w.query("zika", author="Hansen").limit(5),
        lambda w: w.filters(from_pub_date="2020", has_funder=True),
        lambda w: w.filters(award_funder=["10.1/a", "10.1/b"], license_url="x"),
        lambda w: w.query("a b").select("DOI", "title").sort("published").order("asc"),
        lambda w: w.facet("type-name", 10).limit(0),
        lambda w: w.cursor("*", cursor_max=10).limit(2),
        lambda w: w.members(98).filters(from_pub_date="2020").limit(3),
        lambda w: w.members().query("x"),
    ],
)
def test_worksquery_url_matches_actual_request(build):
    """WorksQuery: .url is the URL that is actually requested"""
    stub, urls = _stub_urls()
    query = build(WorksQuery(stub))
    printed = query.url
    query.execute()

    assert urls[0] == printed


def test_worksquery_url_does_not_mutate_filters():
    """WorksQuery: building the url or executing leaves stored filters intact"""
    stub, _ = _stub_urls()
    query = WorksQuery(stub).filters(has_funder=True)
    assert query.url
    query.execute()

    assert query._params["filters"] == {"has_funder": True}


def test_worksquery_filters_accumulates_and_is_immutable():
    """WorksQuery: filters() merges with earlier filters, original unchanged"""
    base = WorksQuery(cr).filters(from_pub_date="2020")
    more = base.filters(has_funder="true")

    assert base._params["filters"] == {"from_pub_date": "2020"}
    assert more._params["filters"] == {"from_pub_date": "2020", "has_funder": "true"}


def test_worksquery_filters_execute_sends_filter():
    """WorksQuery: execute() with filters() runs and sends the filter param"""
    stub, calls = _stub_crossref()
    res = WorksQuery(stub).query("zika").filters(from_pub_date="2020").execute()

    assert res["message"]["items"] == [{"DOI": "10.1/a"}]
    assert len(calls) == 1
    _, params = calls[0]
    assert params["filter"] == "from-pub-date:2020"
    assert params["query"] == "zika"


def test_worksquery_filters_count_sends_filter():
    """WorksQuery: count() with filters() runs and sends the filter param"""
    stub, calls = _stub_crossref()
    n = WorksQuery(stub).filters(from_pub_date="2020", has_funder=True).count()

    assert n == 1
    _, params = calls[0]
    assert params["filter"] == "from-pub-date:2020,has-funder:true"


def test_worksquery_filters_execute_other_endpoint():
    """WorksQuery: filters() also works for endpoints such as members"""
    stub, calls = _stub_crossref()
    WorksQuery(stub).members(98).filters(from_pub_date="2020").execute()

    path, params = calls[0]
    assert path == "/members/98/works"
    assert params["filter"] == "from-pub-date:2020"


@pytest.mark.vcr
def test_worksquery_same_as_wrapped_method_real_requests():
    """WorksQuery: same result as the wrapped method, but real requests"""
    query = q.members(98).select("DOI", "title").limit(3)
    result_WorksQuery = query.execute()
    result_works = cr.members(ids=98, works=True, select=["DOI", "title"], limit=3)

    assert result_WorksQuery == result_works
