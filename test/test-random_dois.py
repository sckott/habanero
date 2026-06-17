import pytest

from habanero import Crossref

cr = Crossref()


@pytest.mark.vcr
def test_random_dois():
    """random dois"""
    res = cr.random_dois()
    assert isinstance(res, list)
    assert isinstance(res[0], str)
    assert len(res) == 10


@pytest.mark.vcr
def test_random_dois_sample_param():
    """random dois - sample parameter"""
    res = cr.random_dois(3)
    assert len(res) == 3

    res = cr.random_dois(5)
    assert len(res) == 5
