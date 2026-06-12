import pytest

from habanero.facets import validate_facets


def test_validate_facets_valid_single():
    assert validate_facets("created:3") is None
    assert validate_facets("deposited:1") is None


def test_validate_facets_valid_comma_string():
    assert validate_facets("published:4,created:3") is None


def test_validate_facets_invalid_name():
    with pytest.raises(ValueError):
        validate_facets("notarealfacet")


def test_validate_facets_invalid_value():
    with pytest.raises(ValueError, match="Invalid facet value: abc"):
        validate_facets("affiliation:3,issn:abc,ror-id:*")
