from pathlib import Path

import pytest
import yaml

from habanero import Crossref

cr = Crossref()

# see https://github.com/sckott/habanero/issues/91


@pytest.mark.vcr
def test_limit_of_zero_with_id():
    """param: limit - zero limit works"""
    res = cr.members(ids=2984, works=True, facet="issn:*", limit=0)
    assert len(res["message"]["items"]) == 0


@pytest.mark.vcr
def test_offset_of_zero_with_id():
    """param: offset - zero offset works"""
    res = cr.members(ids=2984, works=True, limit=1, offset=0)
    assert res["message"]["query"]["start-index"] == 0
    with Path(
        "test/cassettes/test-pagination_params/test_offset_of_zero_with_id.yaml"
    ).open("r") as f:
        x = yaml.safe_load(f)
    uri = x["interactions"][0]["request"]["uri"]
    assert "offset" in uri


@pytest.mark.vcr
def test_limit_of_zero_without_id():
    """param: limit - zero limit works"""
    res = cr.members(limit=0)
    assert len(res["message"]["items"]) == 0


@pytest.mark.vcr
def test_offset_of_zero_without_id():
    """param: offset - zero offset works"""
    res = cr.members(limit=1, offset=0)
    assert res["message"]["query"]["start-index"] == 0
    with Path(
        "test/cassettes/test-pagination_params/test_offset_of_zero_without_id.yaml"
    ).open("r") as f:
        x = yaml.safe_load(f)
    uri = x["interactions"][0]["request"]["uri"]
    assert "offset" in uri
