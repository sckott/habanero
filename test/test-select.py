import pytest

from habanero.select import validate_select


def test_validate_select_valid_string():
    assert validate_select("created") is None
    assert validate_select("deposited") is None


def test_validate_select_valid_comma_string():
    assert validate_select("deposited,published") is None


def test_validate_select_valid_list():
    assert validate_select(["deposited", "published"]) is None


def test_validate_select_invalid_string():
    with pytest.raises(ValueError):
        validate_select("notarealfacet")


def test_validate_select_invalid_comma_string():
    with pytest.raises(ValueError):
        validate_select("deposited,notarealfacet")


def test_validate_select_invalid_list():
    with pytest.raises(ValueError):
        validate_select(["deposited", "notarealfacet"])
