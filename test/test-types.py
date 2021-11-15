import pytest
import os
import vcr
from habanero import Crossref
from requests.exceptions import HTTPError

cr = Crossref()

a = {
    "items": [
        {"id": "book-section", "label": "Book Section"},
        {"id": "monograph", "label": "Monograph"},
        {"id": "report", "label": "Report"},
        {"id": "peer-review", "label": "Peer Review"},
        {"id": "book-track", "label": "Book Track"},
        {"id": "journal-article", "label": "Journal Article"},
        {"id": "book-part", "label": "Part"},
        {"id": "other", "label": "Other"},
        {"id": "book", "label": "Book"},
        {"id": "journal-volume", "label": "Journal Volume"},
        {"id": "book-set", "label": "Book Set"},
        {"id": "reference-entry", "label": "Reference Entry"},
        {"id": "proceedings-article", "label": "Proceedings Article"},
        {"id": "journal", "label": "Journal"},
        {"id": "component", "label": "Component"},
        {"id": "book-chapter", "label": "Book Chapter"},
        {"id": "proceedings-series", "label": "Proceedings Series"},
        {"id": "report-series", "label": "Report Series"},
        {"id": "proceedings", "label": "Proceedings"},
        {"id": "standard", "label": "Standard"},
        {"id": "reference-book", "label": "Reference Book"},
        {"id": "posted-content", "label": "Posted Content"},
        {"id": "journal-issue", "label": "Journal Issue"},
        {"id": "dissertation", "label": "Dissertation"},
        {"id": "grant", "label": "Grant"},
        {"id": "dataset", "label": "Dataset"},
        {"id": "book-series", "label": "Book Series"},
        {"id": "edited-book", "label": "Edited Book"},
        {"id": "standard-series", "label": "Standard Series"},
    ],
    "total-results": 29,
}


@pytest.mark.vcr
def test_types():
    "types - basic test"
    res = cr.types()
    assert isinstance(res, dict)
    assert isinstance(res["message"], dict)
    assert a == res["message"]


@pytest.mark.vcr
def test_types_query():
    "types - param: query - doesn't do anything without works"
    res = cr.types(query="journal")
    assert a == res["message"]


@pytest.mark.vcr
def test_types_ids():
    "types - param: ids"
    res = cr.types(ids="journal")
    assert dict == res.__class__
    assert {"id": "journal", "label": "Journal"} == res["message"]


@pytest.mark.vcr
def test_types_works():
    "types - param: works"
    res = cr.types(ids="journal", works=True, limit=2)
    assert dict == res.__class__
    assert "work-list" == res["message-type"]


# FIXME: not sure why, but the line where we get titles obj is failing with
#   UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 109: ordinal not in range(128)
# def test_types_field_queries():
#     "types - param: kwargs - field queries work as expected"
#     res = cr.types(ids = "journal-article", works = True, query_bibliographic = 'gender', rows = 20)
#     titles = [ str(x.get('title')[0]) for x in res['message']['items'] ]
#     assert dict == res.__class__
#     assert 5 == len(res['message'])
#     assert list == titles.__class__
#     assert str == titles[0].__class__


@pytest.mark.vcr
def test_types_query_filters_not_allowed_with_typeid():
    "types - param: kwargs - query filters not allowed on types/type/ route"
    with pytest.raises(HTTPError):
        cr.types(ids="journal-article", query_bibliographic="gender")


@pytest.mark.vcr
def test_types_bad_id_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.types(ids="tape", warn=True)
    assert out is None


@pytest.mark.vcr
def test_types_mixed_ids_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.types(ids=["journal-article", "tape"], warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None


@pytest.mark.vcr
def test_types_bad_id_works_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.types(ids="tape", works=True, warn=True)
    assert out is None


@pytest.mark.vcr
def test_types_mixed_ids_works_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.types(ids=["journal-article", "tape"], works=True, warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None
