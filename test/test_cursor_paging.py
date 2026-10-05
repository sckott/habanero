"""Cursor paging edge cases, using a mock transport (no network)"""

import httpx2
import pytest

from habanero import Crossref


def _page(dois, cursor, total=100):
    return {
        "status": "ok",
        "message-type": "work-list",
        "message": {
            "items": [{"DOI": d} for d in dois],
            "total-results": total,
            "next-cursor": cursor,
        },
    }


def _ok(*args, **kwargs):
    return httpx2.Response(200, json=_page(*args, **kwargs))


def _stub(*outcomes, max_calls=20):
    """Crossref served by a mock transport that returns each outcome in turn
    (the last one repeats). Fails the test if called more than `max_calls`
    times, which guards against runaway paging."""
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) > max_calls:
            raise AssertionError(f"more than {max_calls} requests: paging runaway")
        return outcomes[min(len(calls), len(outcomes)) - 1]

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Crossref(client=client), calls


def _dois(res):
    return [w["DOI"] for p in res for w in p["message"]["items"]]


def _bad_request():
    # 400 (not retried) with a non-JSON body: _req warns/returns None
    return httpx2.Response(400, text="bad request")


# --- warn=True --------------------------------------------------------------


def test_warn_failure_midway_keeps_pages_so_far():
    cr, calls = _stub(_ok(["a", "b"], "c1"), _bad_request())

    with pytest.warns(UserWarning, match="400"):
        res = cr.works(query="x", cursor="*", limit=2, cursor_max=10, warn=True)

    assert isinstance(res, list)
    assert _dois(res) == ["a", "b"]
    assert len(calls) == 2


def test_warn_failure_on_later_page_after_several_pages():
    cr, _ = _stub(_ok(["a", "b"], "c1"), _ok(["c", "d"], "c2"), _bad_request())

    with pytest.warns(UserWarning, match="400"):
        res = cr.works(query="x", cursor="*", limit=2, cursor_max=10, warn=True)

    assert _dois(res) == list("abcd")


def test_warn_failure_on_first_page_returns_none():
    cr, _ = _stub(_bad_request())

    with pytest.warns(UserWarning, match="400"):
        res = cr.works(query="x", cursor="*", warn=True)

    assert res is None


# --- cursor_max -------------------------------------------------------------


@pytest.mark.parametrize("progress_bar", [False, True])
def test_cursor_max_none_pages_until_everything_is_retrieved(progress_bar):
    cr, calls = _stub(
        _ok(["a", "b"], "c1", total=4),
        _ok(["c", "d"], "c2", total=4),
    )

    res = cr.works(
        query="x",
        cursor="*",
        limit=2,
        cursor_max=None,
        progress_bar=progress_bar,
    )

    assert isinstance(res, list)
    assert _dois(res) == list("abcd")
    assert len(calls) == 2


def test_cursor_max_none_stops_when_cursor_runs_out():
    cr, calls = _stub(_ok(["a", "b"], "c1", total=100), _ok(["c"], None, total=100))

    res = cr.works(query="x", cursor="*", limit=2, cursor_max=None)

    assert _dois(res) == list("abc")
    assert len(calls) == 2


@pytest.mark.parametrize("bad", [4.0, 4.5, "thing", [5], {"a": 1}])
def test_cursor_max_must_be_an_int(bad):
    cr, calls = _stub(_ok(["a"], "c1"))

    with pytest.raises(TypeError):
        cr.works(query="x", cursor="*", cursor_max=bad)
    assert calls == []


@pytest.mark.parametrize("bad", [4.0, 4.5, "thing"])
def test_cursor_max_must_be_an_int_ids_route(bad):
    cr, calls = _stub(_ok(["a"], "c1"))

    with pytest.raises(ValueError, match="cursor_max"):
        cr.members(ids=98, works=True, cursor="*", cursor_max=bad)
    assert calls == []


# --- empty pages ------------------------------------------------------------


def test_empty_page_with_next_cursor_stops_paging():
    cr, calls = _stub(_ok(["a", "b"], "c1", total=100), _ok([], "c2", total=100))

    res = cr.works(query="x", cursor="*", limit=2, cursor_max=1000)

    assert _dois(res) == ["a", "b"]
    assert len(calls) == 2  # first page + the one empty page, then stop


def test_empty_page_with_no_cursor_cap_stops_paging():
    cr, calls = _stub(_ok(["a", "b"], "c1", total=100), _ok([], "c2", total=100))

    res = cr.works(query="x", cursor="*", limit=2, cursor_max=None)

    assert _dois(res) == ["a", "b"]
    assert len(calls) == 2


def test_empty_page_stops_paging_with_progress_bar():
    cr, calls = _stub(_ok(["a", "b"], "c1", total=100), _ok([], "c2", total=100))

    res = cr.works(query="x", cursor="*", limit=2, cursor_max=1000, progress_bar=True)

    assert _dois(res) == ["a", "b"]
    assert len(calls) == 2
