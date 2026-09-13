import pytest

from habanero.sort import validate_sort


def test_validate_sort_none():
    assert validate_sort(None) is None


def test_validate_sort_valid():
    assert validate_sort("created") is None
    assert validate_sort("deposited") is None
    assert validate_sort("published") is None


def test_validate_sort_invalid():
    with pytest.raises(ValueError):
        validate_sort("notarealfacet")
