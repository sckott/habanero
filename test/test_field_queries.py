import pytest

from habanero.field_queries import validate_field_queries


def test_validate_field_queries():
    """validate_field_queries"""
    assert validate_field_queries(None) is None
    assert validate_field_queries("") is None

    with pytest.raises(ValueError):
        validate_field_queries("notarealfacet")


def test_validate_field_queries_single_string():
    assert validate_field_queries("query.event-acronym") is None
    assert validate_field_queries("query.chair") is None


def test_validate_field_queries_single_string_bad():
    with pytest.raises(ValueError):
        validate_field_queries("nope")


def test_validate_field_queries_list():
    assert validate_field_queries(["query.event-acronym", "query.chair"]) is None
    assert validate_field_queries(["query.chair", "query.title"]) is None


def test_validate_field_queries_list_bad():
    with pytest.raises(ValueError):
        validate_field_queries(["query.chair", "query.title", "nope"])
