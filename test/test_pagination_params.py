import pytest

from habanero import Crossref

cr = Crossref()

# see https://github.com/sckott/habanero/issues/91


@pytest.mark.vcr
def test_limit_of_zero_with_id():
    """param: limit - zero limit works"""
    res = cr.members(ids=2984, works=True, facet="issn:*", limit=0)
    assert len(res["message"]["items"]) == 0


@pytest.mark.vcr
def test_offset_of_zero_with_id(vcr):
    """param: offset - zero offset works"""
    res = cr.members(ids=2984, works=True, limit=1, offset=0)
    assert res["message"]["query"]["start-index"] == 0
    uri = vcr.requests[0].uri
    assert "offset" in uri


@pytest.mark.vcr
def test_limit_of_zero_without_id():
    """param: limit - zero limit works"""
    res = cr.members(limit=0)
    assert len(res["message"]["items"]) == 0


@pytest.mark.vcr
def test_offset_of_zero_without_id(vcr):
    """param: offset - zero offset works"""
    res = cr.members(limit=1, offset=0)
    assert res["message"]["query"]["start-index"] == 0
    uri = vcr.requests[0].uri
    assert "offset" in uri
