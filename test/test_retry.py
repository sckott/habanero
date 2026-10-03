from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx2
import pytest

import habanero.retry as retry_mod
from habanero import Crossref, RequestError
from habanero.retry import RetryingClient, retry_after_seconds

WORK = {"status": "ok", "message-type": "work", "message": {"DOI": "10.1/a"}}


@pytest.fixture
def sleeps(monkeypatch):
    """Record requested sleeps instead of actually sleeping"""
    recorded: list[float] = []
    monkeypatch.setattr(retry_mod, "_sleep", recorded.append)
    return recorded


def _client(handler) -> httpx2.Client:
    return httpx2.Client(transport=httpx2.MockTransport(handler))


def _sequence(*outcomes):
    """Handler that returns/raises each outcome in turn; the last one repeats"""
    calls: list[httpx2.Request] = []

    def handler(request):
        calls.append(request)
        outcome = outcomes[min(len(calls), len(outcomes)) - 1]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return handler, calls


def _resp(status, **kwargs):
    return httpx2.Response(status, **kwargs)


# --- RetryingClient ---------------------------------------------------------


@pytest.mark.parametrize("status", [429, 502, 503, 504])
def test_retries_retryable_status_then_succeeds(status, sleeps):
    handler, calls = _sequence(_resp(status), _resp(200, json=WORK))
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=1.0)

    r = rc.get("https://x.test/works/1")

    assert r.status_code == 200
    assert len(calls) == 2
    assert sleeps == [1.0]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 500])
def test_does_not_retry_other_statuses(status, sleeps):
    handler, calls = _sequence(_resp(status))
    rc = RetryingClient(_client(handler), retries=3)

    r = rc.get("https://x.test/works/1")

    assert r.status_code == status
    assert len(calls) == 1
    assert sleeps == []


def test_exponential_backoff_and_returns_last_response_when_exhausted(sleeps):
    handler, calls = _sequence(_resp(503))
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=0.5)

    r = rc.get("https://x.test/works/1")

    assert r.status_code == 503  # last response handed back to the caller
    assert len(calls) == 4  # 1 try + 3 retries
    assert sleeps == [0.5, 1.0, 2.0]


def test_backoff_is_capped(sleeps):
    handler, _ = _sequence(_resp(503))
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=100)

    rc.get("https://x.test/works/1")

    assert sleeps == [retry_mod.MAX_BACKOFF] * 3


def test_retries_zero_turns_retrying_off(sleeps):
    handler, calls = _sequence(_resp(429), _resp(200, json=WORK))
    rc = RetryingClient(_client(handler), retries=0)

    assert rc.get("https://x.test/works/1").status_code == 429
    assert len(calls) == 1
    assert sleeps == []


def test_retry_after_seconds_is_honored(sleeps):
    handler, _ = _sequence(
        _resp(429, headers={"Retry-After": "7"}), _resp(200, json=WORK)
    )
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=1.0)

    assert rc.get("https://x.test/works/1").status_code == 200
    assert sleeps == [7.0]


def test_retry_after_too_long_gives_up_without_sleeping(sleeps):
    handler, calls = _sequence(
        _resp(429, headers={"Retry-After": "3600"}), _resp(200, json=WORK)
    )
    rc = RetryingClient(_client(handler), retries=3)

    assert rc.get("https://x.test/works/1").status_code == 429
    assert len(calls) == 1
    assert sleeps == []


def test_unparseable_retry_after_falls_back_to_backoff(sleeps):
    handler, _ = _sequence(
        _resp(503, headers={"Retry-After": "soon"}), _resp(200, json=WORK)
    )
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=2.0)

    rc.get("https://x.test/works/1")
    assert sleeps == [2.0]


def test_retry_after_parsing():
    assert retry_after_seconds(_resp(429, headers={"Retry-After": "5"})) == 5.0
    assert retry_after_seconds(_resp(429, headers={"Retry-After": "-5"})) == 0.0
    assert retry_after_seconds(_resp(429, headers={"Retry-After": "inf"})) is None
    assert retry_after_seconds(_resp(429, headers={"Retry-After": "nan"})) is None
    assert retry_after_seconds(_resp(429)) is None

    when = datetime.now(timezone.utc) + timedelta(seconds=30)
    date = format_datetime(when, usegmt=True)
    secs = retry_after_seconds(_resp(429, headers={"Retry-After": date}))
    assert secs is not None and 25 < secs <= 30

    past = format_datetime(datetime.now(timezone.utc) - timedelta(hours=1), usegmt=True)
    assert retry_after_seconds(_resp(429, headers={"Retry-After": past})) == 0.0


@pytest.mark.parametrize(
    "exc",
    [
        httpx2.ConnectError("refused"),
        httpx2.ConnectTimeout("slow"),
        httpx2.ReadTimeout("slow"),
        httpx2.ReadError("reset"),
        httpx2.RemoteProtocolError("closed early"),
    ],
)
def test_retries_transient_exceptions(exc, sleeps):
    handler, calls = _sequence(exc, exc, _resp(200, json=WORK))
    rc = RetryingClient(_client(handler), retries=3, backoff_factor=1.0)

    assert rc.get("https://x.test/works/1").status_code == 200
    assert len(calls) == 3
    assert sleeps == [1.0, 2.0]


def test_reraises_last_exception_when_exhausted(sleeps):
    handler, calls = _sequence(httpx2.ReadTimeout("slow"))
    rc = RetryingClient(_client(handler), retries=2)

    with pytest.raises(httpx2.ReadTimeout):
        rc.get("https://x.test/works/1")
    assert len(calls) == 3
    assert len(sleeps) == 2


def test_does_not_retry_non_transient_exceptions(sleeps):
    handler, calls = _sequence(httpx2.UnsupportedProtocol("ftp://"))
    rc = RetryingClient(_client(handler), retries=3)

    with pytest.raises(httpx2.UnsupportedProtocol):
        rc.get("https://x.test/works/1")
    assert len(calls) == 1
    assert sleeps == []


def test_kwargs_are_passed_on_every_attempt(sleeps):
    handler, calls = _sequence(_resp(429), _resp(200, json=WORK))
    rc = RetryingClient(_client(handler), retries=3)

    rc.get("https://x.test/works", params={"q": "a"}, headers={"X-Test": "1"})

    assert [c.url.params["q"] for c in calls] == ["a", "a"]
    assert [c.headers["x-test"] for c in calls] == ["1", "1"]


# --- through the Crossref class ---------------------------------------------


def test_crossref_works_by_id_retries_429(sleeps):
    handler, calls = _sequence(_resp(429), _resp(200, json=WORK))
    cr = Crossref(client=_client(handler))

    res = cr.works(ids="10.1/a")

    assert res["message"]["DOI"] == "10.1/a"
    assert len(calls) == 2
    assert len(sleeps) == 1


def test_crossref_by_id_error_after_retries_is_unchanged(sleeps):
    handler, calls = _sequence(_resp(503))
    cr = Crossref(client=_client(handler), retries=2)

    with pytest.raises(httpx2.HTTPStatusError):
        cr.works(ids="10.1/a")
    assert len(calls) == 3


def test_crossref_warn_still_applies_after_retries_are_exhausted(sleeps):
    handler, calls = _sequence(_resp(503))
    cr = Crossref(client=_client(handler), retries=1)

    with pytest.warns(UserWarning, match="503"):
        res = cr.works(ids=["10.1/a", "10.1/b"], warn=True)
    assert res == [None, None]
    assert len(calls) == 4  # 2 ids x (1 try + 1 retry)


def test_crossref_query_route_retries_and_raises_request_error(sleeps):
    err = {"status": "failed", "message": [{"message": "slow down"}]}
    handler, calls = _sequence(_resp(429, json=err))
    cr = Crossref(client=_client(handler), retries=2)

    with pytest.raises(RequestError) as exc:
        cr.members(query="x")
    assert exc.value.status_code == 429
    assert len(calls) == 3


def test_crossref_cursor_paging_survives_a_429_midway(sleeps):
    def page(items, cursor):
        return {
            "status": "ok",
            "message-type": "work-list",
            "message": {"items": items, "total-results": 4, "next-cursor": cursor},
        }

    handler, calls = _sequence(
        _resp(200, json=page([{"DOI": "a"}, {"DOI": "b"}], "c1")),
        _resp(429),
        _resp(200, json=page([{"DOI": "c"}, {"DOI": "d"}], "c2")),
    )
    cr = Crossref(client=_client(handler))

    res = cr.works(query="x", cursor="*", limit=2, cursor_max=4)

    assert isinstance(res, list)
    assert [w["DOI"] for p in res for w in p["message"]["items"]] == list("abcd")
    assert len(calls) == 3
    assert len(sleeps) == 1


def test_crossref_works_by_works_route_retries(sleeps):
    """the `works=True` route (Request class) retries too"""
    body = {
        "status": "ok",
        "message-type": "work-list",
        "message": {"items": [], "total-results": 0},
    }
    handler, calls = _sequence(_resp(502), _resp(200, json=body))
    cr = Crossref(client=_client(handler))

    cr.members(ids=98, works=True)
    assert len(calls) == 2


def test_crossref_retry_settings_read_on_each_request(sleeps):
    handler, calls = _sequence(_resp(503))
    cr = Crossref(client=_client(handler), retries=0)

    with pytest.raises(httpx2.HTTPStatusError):
        cr.works(ids="10.1/a")
    assert len(calls) == 1

    cr.retries = 2
    cr.backoff_factor = 0.25
    with pytest.raises(httpx2.HTTPStatusError):
        cr.works(ids="10.1/a")
    assert len(calls) == 1 + 3
    assert sleeps == [0.25, 0.5]


def test_crossref_non_retryable_error_is_not_retried(sleeps):
    handler, calls = _sequence(_resp(404))
    cr = Crossref(client=_client(handler))

    with pytest.raises(httpx2.HTTPStatusError):
        cr.works(ids="10.1/notreal")
    assert len(calls) == 1
    assert sleeps == []


def test_crossref_retry_defaults():
    cr = Crossref()
    assert cr.retries == 3
    assert cr.backoff_factor == 1.0


@pytest.mark.parametrize(
    "kwargs, exc",
    [
        ({"retries": -1}, ValueError),
        ({"retries": 1.5}, TypeError),
        ({"retries": "3"}, TypeError),
        ({"retries": True}, TypeError),
        ({"backoff_factor": -0.1}, ValueError),
        ({"backoff_factor": "1"}, TypeError),
    ],
)
def test_crossref_retry_settings_validated(kwargs, exc):
    with pytest.raises(exc):
        Crossref(**kwargs)
