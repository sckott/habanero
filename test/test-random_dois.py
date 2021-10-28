import pytest
import os
import vcr
from habanero import Crossref
from requests.exceptions import HTTPError

cr = Crossref()


@pytest.mark.vcr
def test_random_dois():
    "random dois"
    res = cr.random_dois()
    assert list == res.__class__
    assert str == res[0].__class__
    assert 10 == len(res)


@pytest.mark.vcr
def test_random_dois_sample_param():
    "random dois - sample parameter"
    res = cr.random_dois(3)
    assert 3 == len(res)

    res = cr.random_dois(5)
    assert 5 == len(res)
