import pytest
import vcr
import yaml
from habanero import Crossref

cr = Crossref()

# see https://github.com/sckott/habanero/issues/91


@pytest.mark.vcr
def test_limit_of_zero_with_id():
    "param: limit - zero limit works"
    res = cr.members(ids=2984, works=True, facet="issn:*", limit=0)
    assert 0 == len(res["message"]["items"])


@pytest.mark.vcr
def test_offset_of_zero_with_id():
    "param: offset - zero offset works"
    res = cr.members(ids=2984, works=True, limit=1, offset=0)
    assert 0 == res["message"]["query"]["start-index"]
    with open(
        "test/cassettes/test-pagination_params/test_offset_of_zero_with_id.yaml"
    ) as f:
        x = yaml.safe_load(f)
    uri = x["interactions"][0]["request"]["uri"]
    assert "offset" in uri


@pytest.mark.vcr
def test_limit_of_zero_without_id():
    "param: limit - zero limit works"
    res = cr.members(limit=0)
    assert 0 == len(res["message"]["items"])


@pytest.mark.vcr
def test_offset_of_zero_without_id():
    "param: offset - zero offset works"
    res = cr.members(limit=1, offset=0)
    assert 0 == res["message"]["query"]["start-index"]
    with open(
        "test/cassettes/test-pagination_params/test_offset_of_zero_without_id.yaml"
    ) as f:
        x = yaml.safe_load(f)
    uri = x["interactions"][0]["request"]["uri"]
    assert "offset" in uri
