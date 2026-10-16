from typing import no_type_check

import pytest

from habanero import counts

EMAIL = "some.email@gmail.com"


@pytest.mark.vcr
def test_citation_count():
    """citation count - basic test"""
    res = counts.citation_count(doi="10.1371/journal.pone.0042793", email=EMAIL)
    assert isinstance(res, int)
    assert res > 0


@pytest.mark.vcr
def test_citation_count_positional_email():
    """citation count - email can be passed positionally"""
    res = counts.citation_count("10.1371/journal.pone.0042793", EMAIL)
    assert isinstance(res, int)
    assert res > 0


@no_type_check
@pytest.mark.vcr
def test_citation_count_key_deprecated():
    """citation count - `key` still works but raises a DeprecationWarning"""
    with pytest.warns(DeprecationWarning, match="`key` parameter is deprecated"):
        res = counts.citation_count(doi="10.1371/journal.pone.0042793", key=EMAIL)
    assert isinstance(res, int)
    assert res > 0


@no_type_check
@pytest.mark.vcr
def test_citation_count_email_preferred_over_key():
    """citation count - `email` is used when both `email` and `key` are given"""
    with pytest.warns(DeprecationWarning):
        res = counts.citation_count(
            doi="10.1371/journal.pone.0042793", email=EMAIL, key="ignored"
        )
    assert isinstance(res, int)
    assert res > 0


@no_type_check
def test_citation_count_email_required():
    """citation count - raises ValueError when no email is given"""
    with pytest.raises(ValueError, match="`email` is required"):
        counts.citation_count(doi="10.1371/journal.pone.0042793")


@pytest.mark.vcr
def test_citation_count_doi_not_found():
    """citation count - raises ValueError when the DOI is not found"""
    with pytest.raises(ValueError, match="citedby-count not found"):
        counts.citation_count(doi="10.1016/j.fbr.2012", email=EMAIL)
