import pytest
import os
import vcr
from requests import HTTPError
from habanero import Crossref

cr = Crossref()


@pytest.mark.vcr
def test_registration_agency():
    "registration agency"
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@pytest.mark.vcr
def test_registration_agency_unicode():
    "registration agency- unicode"
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@pytest.mark.vcr
def test_registration_agency_bad_request():
    "registration agency - bad request"
    with pytest.raises(HTTPError):
        cr.registration_agency(5)
