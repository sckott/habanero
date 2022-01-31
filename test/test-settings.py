import pytest
import vcr
import os
import yaml
from habanero import Crossref

cr_with_ua = Crossref(ua_string="foo bar")
cr_without_ua = Crossref()
cr_with_bad_ua = Crossref(ua_string=5)

vcr_path = "test/cassettes/test-settings/test_ua_string.yaml"


@pytest.mark.vcr(vcr_path)
def test_ua_string():
    "settings (ua_string) - with ua string, works"
    res = cr_with_ua.works(ids="10.1371/journal.pone.0033693")
    x = open(vcr_path, "r").read()
    xy = yaml.safe_load(x)
    heads = xy["interactions"][0]["request"]["headers"]

    assert "foo bar" in heads["User-Agent"][0]
    assert "foo bar" in heads["X-USER-AGENT"][0]


vcr_noua_path = "test/cassettes/test-settings/test_no_ua_string.yaml"


@pytest.mark.vcr(vcr_noua_path)
def test_no_ua_string():
    "settings (ua_string) - without ua string, works"
    res = cr_without_ua.works(ids="10.1371/journal.pone.0033693")
    x = open(vcr_noua_path, "r").read()
    xy = yaml.safe_load(x)
    heads = xy["interactions"][0]["request"]["headers"]

    assert "foo bar" not in heads["User-Agent"][0]
    assert "foo bar" not in heads["X-USER-AGENT"][0]


vcr_path_members = "test/cassettes/test-settings/test_ua_string_members.yaml"


@pytest.mark.vcr(vcr_path_members)
def test_ua_string_members():
    "settings (ua_string) - with ua string, members"
    res = cr_with_ua.members(query="ecology", limit=2)
    x = open(vcr_path_members, "r").read()
    xy = yaml.safe_load(x)
    heads = xy["interactions"][0]["request"]["headers"]

    assert "foo bar" in heads["User-Agent"][0]
    assert "foo bar" in heads["X-USER-AGENT"][0]


vcr_path_prefixes = "test/cassettes/test-settings/test_ua_string_prefixes.yaml"


@pytest.mark.vcr(vcr_path_prefixes)
def test_ua_string_prefixes():
    "settings (ua_string) - with ua string, prefixes"
    res = cr_with_ua.prefixes(ids="10.1016", works=True, sample=2)
    x = open(vcr_path_prefixes, "r").read()
    xy = yaml.safe_load(x)
    heads = xy["interactions"][0]["request"]["headers"]

    assert "foo bar" in heads["User-Agent"][0]
    assert "foo bar" in heads["X-USER-AGENT"][0]


vcr_path_registration_agency = (
    "test/cassettes/test-settings/test_ua_string_registration_agency.yaml"
)


@pytest.mark.vcr(vcr_path_registration_agency)
def test_ua_string_registration_agency():
    "settings (ua_string) - with ua string, registration_agency"
    res = cr_with_ua.registration_agency("10.1126/science.169.3946.635")
    x = open(vcr_path_registration_agency, "r").read()
    xy = yaml.safe_load(x)
    heads = xy["interactions"][0]["request"]["headers"]

    assert "foo bar" in heads["User-Agent"][0]
    assert "foo bar" in heads["X-USER-AGENT"][0]


def test_ua_string_errors():
    "settings (ua_string) - fails well"
    with pytest.raises(TypeError):
        cr_with_bad_ua.works(ids="10.1371/journal.pone.0033693")


# NOTE: the two test blocks above using cassettes is super hacky
# - i can't find a way to inspect the request headers that get sent
# - so just inspecting the request headers recorded in the cassette
# - i.e., re-running to record cassettes from scratch will fail
# - on the first run, but then suceed after that
