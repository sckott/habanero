import httpx2
import pytest

from habanero import Crossref, RequestError

BODY = {
    "status": "ok",
    "message-type": "data-citations-list",
    "message": {
        "total-results": 1,
        "next-page": None,
        "items": [{"relation": "references"}],
    },
}


def _cr(handler, **kwargs):
    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Crossref(client=client, retries=0, **kwargs)


def _capture():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx2.Response(200, json=BODY)

    return handler, calls


def test_data_citations_sends_params_to_beta_route():
    handler, calls = _capture()
    res = _cr(handler).data_citations(
        subject_id="10.1/s",
        object_id="10.1/o",
        member_id=78,
        relation="references",
        from_created_date="2026-01-20T00:00:00",
        until_created_date="2026-01-21T12:00:00",
        page=0,
        limit=0,
    )
    assert res == BODY
    assert calls[0].url.path == "/beta/datacitations"
    assert dict(calls[0].url.params) == {
        "subject-id": "10.1/s",
        "object-id": "10.1/o",
        "member-id": "78",
        "relation": "references",
        "from-created-date": "2026-01-20T00:00:00",
        "until-created-date": "2026-01-21T12:00:00",
        "page": "0",
        "rows": "0",
    }


def test_data_citations_omits_unset_params():
    handler, calls = _capture()
    _cr(handler).data_citations()
    assert dict(calls[0].url.params) == {}


@pytest.mark.parametrize(
    "doi",
    ["https://doi.org/10.1/o", "http://dx.doi.org/10.1/o", "doi:10.1/o", " 10.1/o "],
)
def test_data_citations_strips_doi_prefix(doi):
    handler, calls = _capture()
    _cr(handler).data_citations(object_id=doi)
    assert calls[0].url.params["object-id"] == "10.1/o"


def test_data_citations_sends_mailto():
    handler, calls = _capture()
    _cr(handler, mailto="name@example.com").data_citations()
    assert "mailto:name@example.com" in calls[0].headers["User-Agent"]


def test_data_citations_raises_api_reason():
    def handler(request):
        return httpx2.Response(
            400,
            json={
                "status": "bad-request",
                "reason": "rows must be between 0 and 1000.",
            },
        )

    with pytest.raises(RequestError, match="rows must be between 0 and 1000"):
        _cr(handler).data_citations(limit=1001)


def test_data_citations_non_json_error():
    def handler(request):
        return httpx2.Response(429, text="")

    with pytest.raises(RequestError) as e:
        _cr(handler).data_citations()
    assert e.value.status_code == 429
