import pytest

from habanero import Crossref


@pytest.fixture
def cross_ref():
    return Crossref()


@pytest.mark.vcr
def test_cursor(cross_ref):
    """cursor works - basic test"""
    res = cross_ref.works(query="widget", cursor="*", cursor_max=10)
    assert isinstance(res, dict)
    assert isinstance(res["message"], dict)
    assert len(res) == 4
    assert len(res["message"]) == 6


@pytest.mark.vcr
def test_cursor_max(cross_ref):
    """cursor works - cursor_max works"""
    res1 = cross_ref.works(query="widget", cursor="*", cursor_max=60)
    items1 = [z["message"]["items"] for z in res1]
    items1 = [item for sublist in items1 for item in sublist]
    assert isinstance(res1, list)
    assert len(items1) == 60


def test_cursor_fails_cursor_type(cross_ref):
    with pytest.raises(TypeError):
        cross_ref.works(query="widget", cursor=5)


def test_cursor_fails_cursor_max(cross_ref):
    with pytest.raises(TypeError):
        cross_ref.works(query="widget", cursor="*", cursor_max="thing")
