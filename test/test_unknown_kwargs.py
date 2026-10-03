import pytest

from habanero import Crossref
from habanero.habanero_utils import check_unknown_kwargs

cr = Crossref()


def test_check_unknown_kwargs_allows_field_queries():
    assert check_unknown_kwargs({}) is None
    assert (
        check_unknown_kwargs({"query_author": "x", "query_container_title": "y"})
        is None
    )


def test_check_unknown_kwargs_raises():
    with pytest.raises(TypeError, match="'rows'"):
        check_unknown_kwargs({"query_author": "x", "rows": 5})


def test_check_unknown_kwargs_lists_all_names():
    with pytest.raises(TypeError, match="'bar', 'foo'"):
        check_unknown_kwargs({"foo": 1, "bar": 2})


@pytest.mark.parametrize(
    "call",
    [
        lambda: cr.works(query="ecology", foo=1),
        lambda: cr.works(ids="10.1371/journal.pone.0033693", foo=1),
        lambda: cr.members(foo=1),
        lambda: cr.members(ids=98, works=True, foo=1),
        lambda: cr.prefixes("10.1016", foo=1),
        lambda: cr.funders(foo=1),
        lambda: cr.journals(foo=1),
        lambda: cr.types(foo=1),
        lambda: cr.licenses(foo=1),
        lambda: cr.registration_agency("10.1371/journal.pone.0033693", foo=1),
        lambda: cr.random_dois(foo=1),
        lambda: cr.works(query="ecology", qurey_author="typo"),
    ],
)
def test_unknown_kwargs_raise_type_error(call):
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        call()
