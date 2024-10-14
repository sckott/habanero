import pytest
from httpx import HTTPError

from habanero import Crossref

cr = Crossref()


@pytest.mark.vcr
def test_registration_agency():
    """registration agency"""
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert isinstance(res, list)
    assert isinstance(res[0], str)


@pytest.mark.vcr
def test_registration_agency_unicode():
    """registration agency- unicode"""
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert isinstance(res, list)
    assert isinstance(res[0], str)


@pytest.mark.vcr
def test_registration_agency_bad_request():
    """registration agency - bad request"""
    with pytest.raises(HTTPError):
        cr.registration_agency(5)
