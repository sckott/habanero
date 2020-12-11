"""Tests for registration_agency"""
import os
import vcr
from habanero import Crossref
import pytest
from requests.exceptions import HTTPError

cr = Crossref()


@vcr.use_cassette("test/vcr_cassettes/registration_agency.yaml")
def test_registration_agency():
    "registration agency"
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@vcr.use_cassette("test/vcr_cassettes/registration_agency_unicode.yaml")
def test_registration_agency_unicode():
    "registration agency- unicode"
    res = cr.registration_agency(u"10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@vcr.use_cassette("test/vcr_cassettes/registration_agency_bad_request.yaml")
def test_registration_agency_bad_request():
    "registration agency - bad request"
    with pytest.raises(HTTPError):
        cr.registration_agency(5)
