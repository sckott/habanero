from unittest.mock import patch

import pytest

from habanero import Crossref, WorksQuery

cr = Crossref()
q = WorksQuery(cr)


def test_worksquery_basics():
    """WorksQuery: basic structure"""
    res = q.query("zika").filter(from_pub_date="2020")

    assert isinstance(res, WorksQuery)
    assert hasattr(res, "types")


def test_worksquery_instances_are_immutable():
    """WorksQuery: instances are immutable"""
    base = WorksQuery(cr).query("zika").filter(from_pub_date="2020")
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


@pytest.mark.vcr
def test_worksquery_same_as_wrapped_method_real_requests():
    """WorksQuery: same result as the wrapped method, but real requests"""
    query = q.members(98).select("DOI", "title").limit(3)
    result_WorksQuery = query.execute()
    result_works = cr.members(ids=98, works=True, select=["DOI", "title"], limit=3)

    assert result_WorksQuery == result_works
