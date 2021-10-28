import pytest
import os
import vcr
from habanero import Crossref
from simplejson import JSONDecodeError

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
    res = cr.registration_agency(u"10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@pytest.mark.vcr
def test_registration_agency_bad_request():
    "registration agency - bad request"
    with pytest.raises(JSONDecodeError):
        cr.registration_agency(5)
