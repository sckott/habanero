import copy
import json
import pickle
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx2
import pytest

from habanero import Crossref


class _CountingServer(ThreadingHTTPServer):
    """Local keep-alive HTTP server that counts accepted TCP connections"""

    daemon_threads = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = 0
        self.requests = 0

    def get_request(self):
        sock, addr = super().get_request()
        self.connections += 1
        return sock, addr


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep connections alive

    def do_GET(self):
        self.server.requests += 1  # type: ignore[attr-defined]
        if "cursor" in self.path:
            body = {
                "status": "ok",
                "message-type": "work-list",
                "message": {
                    "items": [{"DOI": "10.1/a"}] * 2,
                    "total-results": 6,
                    "next-cursor": "next",
                },
            }
        elif self.path.split("?")[0].endswith("/works"):
            body = {
                "status": "ok",
                "message-type": "work-list",
                "message": {"items": [{"DOI": "10.1/a"}], "total-results": 1},
            }
        else:
            body = {
                "status": "ok",
                "message-type": "work",
                "message": {"DOI": "10.1/a"},
            }
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


@pytest.fixture
def server(monkeypatch):
    # make sure the sandbox/CI proxy settings don't intercept localhost
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        monkeypatch.delenv(var, raising=False)
        monkeypatch.delenv(var.lower(), raising=False)
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")

    try:
        srv = _CountingServer(("127.0.0.1", 0), _Handler)
    except PermissionError:
        pytest.skip("binding a local socket is not permitted here")
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()


def _base_url(srv):
    return f"http://127.0.0.1:{srv.server_address[1]}"


def test_many_ids_reuse_one_connection(server):
    """requests for many DOIs share a single TCP connection"""
    with Crossref(base_url=_base_url(server)) as cr:
        cr.works(ids=["10.1/a", "10.1/b", "10.1/c", "10.1/d", "10.1/e"])

    assert server.requests == 5
    assert server.connections == 1


def test_cursor_paging_reuses_one_connection(server):
    """every page of a deep-paging request shares a single TCP connection"""
    with Crossref(base_url=_base_url(server)) as cr:
        res = cr.works(query="x", cursor="*", limit=2, cursor_max=6)

    assert isinstance(res, list)
    assert server.requests == 3
    assert server.connections == 1


def test_connection_reused_across_calls_on_same_object(server):
    with Crossref(base_url=_base_url(server)) as cr:
        cr.works(ids="10.1/a")
        cr.works(ids="10.1/b")
        cr.members(ids=98, works=True, limit=2)

    assert server.requests == 3
    assert server.connections == 1


def test_client_is_lazy_and_cached():
    cr = Crossref()
    assert cr._client is None
    c = cr.client
    assert isinstance(c, httpx2.Client)
    assert cr.client is c
    cr.close()


def test_close_closes_owned_client_and_allows_reuse():
    cr = Crossref()
    first = cr.client
    cr.close()
    assert first.is_closed
    assert cr._client is None
    # still usable: a fresh client is created on demand
    second = cr.client
    assert second is not first
    assert not second.is_closed
    cr.close()


def test_close_without_client_is_noop():
    Crossref().close()


def test_context_manager_closes_client():
    with Crossref() as cr:
        c = cr.client
    assert c.is_closed


def test_user_supplied_client_is_not_closed():
    client = httpx2.Client()
    cr = Crossref(client=client)
    assert cr.client is client
    cr.close()
    assert not client.is_closed
    assert cr.client is client
    client.close()


def test_user_supplied_client_receives_requests():
    seen = []

    def handler(request):
        seen.append(request.url.path)
        return httpx2.Response(
            200, json={"status": "ok", "message-type": "work", "message": {}}
        )

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    cr = Crossref(client=client)
    cr.works(ids=["10.1/a", "10.1/b"])
    assert seen == ["/works/10.1/a", "/works/10.1/b"]


def test_per_request_settings_still_follow_the_object():
    """mailto/ua_string/timeout changed after creation are still honored"""
    seen = []

    def handler(request):
        seen.append(request.headers["user-agent"])
        return httpx2.Response(
            200, json={"status": "ok", "message-type": "work", "message": {}}
        )

    cr = Crossref(client=httpx2.Client(transport=httpx2.MockTransport(handler)))
    cr.works(ids="10.1/a")
    cr.mailto = "a@b.com"
    cr.ua_string = "foo bar"
    cr.works(ids="10.1/a")
    assert "mailto" not in seen[0]
    assert "mailto:a@b.com" in seen[1]
    assert "foo bar" in seen[1]


def test_pickle_and_copy_with_open_client():
    cr = Crossref(mailto="a@b.com")
    _ = cr.client  # open it
    for clone in (pickle.loads(pickle.dumps(cr)), copy.copy(cr), copy.deepcopy(cr)):
        assert clone.mailto == "a@b.com"
        assert clone._client is None
    cr.close()
