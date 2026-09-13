import pytest

from habanero import Crossref

cr_with_ua = Crossref(ua_string="foo bar")
cr_without_ua = Crossref()
cr_with_bad_ua = Crossref(ua_string=5)  # type: ignore


@pytest.mark.vcr
def test_ua_string(vcr):
    """settings (ua_string) - with ua string, works"""
    cr_with_ua.works(ids="10.1371/journal.pone.0033693")
    heads = vcr.requests[0].headers

    assert "foo bar" in heads["user-agent"]
    assert "foo bar" in heads["x-user-agent"]


@pytest.mark.vcr
def test_no_ua_string(vcr):
    """settings (ua_string) - without ua string, works"""
    cr_without_ua.works(ids="10.1371/journal.pone.0033693")
    heads = vcr.requests[0].headers

    assert "foo bar" not in heads["user-agent"]
    assert "foo bar" not in heads["x-user-agent"]


@pytest.mark.vcr
def test_ua_string_registration_agency(vcr):
    """settings (ua_string) - with ua string, registration_agency"""
    cr_with_ua.registration_agency("10.1126/science.169.3946.635")
    heads = vcr.requests[0].headers

    assert "foo bar" in heads["user-agent"]
    assert "foo bar" in heads["x-user-agent"]


def test_ua_string_errors():
    """settings (ua_string) - fails well"""
    with pytest.raises(TypeError):
        cr_with_bad_ua.works(ids="10.1371/journal.pone.0033693")
