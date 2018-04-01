"""Tests for random_dois"""
import os
import vcr
from habanero import Crossref
from nose.tools import raises
from requests.exceptions import HTTPError

cr = Crossref()

@vcr.use_cassette('test/vcr_cassettes/random_dois.yaml')
def test_random_dois():
    "random dois"
    res = cr.random_dois()
    assert list == res.__class__
    assert str == res[0].__class__
    assert 10 == len(res)

@vcr.use_cassette('test/vcr_cassettes/random_dois_sample_param.yaml')
def test_random_dois_sample_param():
    "random dois - sample parameter"
    res = cr.random_dois(3)
    assert 3 == len(res)

    res = cr.random_dois(5)
    assert 5 == len(res)
