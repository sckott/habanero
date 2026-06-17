import pytest

from habanero import Crossref

cr = Crossref()


@pytest.mark.vcr
def test_licenses():
    """licenses - basic test"""
    res = cr.licenses(query="science", limit=2)
    assert isinstance(res, dict)
    assert len(res["message"]["items"]) == 2


@pytest.mark.vcr
def test_licenses_query():
    """licenses - param: query works"""
    res1 = cr.licenses(query="aps")
    res2 = cr.licenses(query="cellular oncology")
    assert res1["message"]["total-results"] < res2["message"]["total-results"]
