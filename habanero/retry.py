"""Retry handling for HTTP GET requests

Only GET requests are made, so every request is safe to repeat.
"""

import logging
import math
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx2

logger = logging.getLogger("habanero")

# 429: rate limited. 502/503/504: transient server or gateway problems.
# 500 is deliberately not here: for Crossref it's usually a problem with the
# request itself (e.g., an unsupported CSL style), so repeating it only delays
# the error
RETRY_STATUSES: frozenset[int] = frozenset({429, 502, 503, 504})

# timeouts, dropped/refused connections, and connections closed mid-response.
# Not retried: bad URLs, proxy errors, local protocol errors - repeating won't help
RETRY_EXCEPTIONS: tuple[type[Exception], ...] = (
    httpx2.TimeoutException,
    httpx2.NetworkError,
    httpx2.RemoteProtocolError,
)

# longest we'll sleep between attempts because of exponential backoff
MAX_BACKOFF = 30.0
# if a server asks us to wait longer than this (`Retry-After`), we stop retrying
# and return the error instead of silently blocking for a long time
MAX_RETRY_AFTER = 60.0


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


def backoff_delay(attempt: int, backoff_factor: float) -> float:
    """Seconds to wait before retry number `attempt + 1`: factor * 2**attempt"""
    return min(MAX_BACKOFF, backoff_factor * (2**attempt))


def retry_after_seconds(response: httpx2.Response) -> float | None:
    """Seconds to wait according to a `Retry-After` header, or None

    The header is either a number of seconds or an HTTP date
    """
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    value = value.strip()
    try:
        seconds = float(value)
    except ValueError:
        pass
    else:
        return max(0.0, seconds) if math.isfinite(seconds) else None
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())


class RetryingClient:
    """Wraps an `httpx2.Client`, retrying `get` on transient failures

    Retries when the response status is in `RETRY_STATUSES`, or the request
    raises one of `RETRY_EXCEPTIONS`. Waits for the `Retry-After` header when
    the server sends one, otherwise backs off exponentially:
    `backoff_factor * 2**attempt` seconds.

    Once retries run out, the last response is returned (or the last exception
    raised), so callers handle the final failure exactly as they would without
    any retrying.

    :param client: anything with an `httpx2.Client`-like `get` method
    :param retries: maximum number of retries; 0 turns retrying off
    :param backoff_factor: base wait in seconds for exponential backoff
    """

    def __init__(
        self, client: Any, retries: int = 3, backoff_factor: float = 1.0
    ) -> None:
        self.client = client
        self.retries = retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, **kwargs: Any) -> httpx2.Response:
        attempt = 0
        while True:
            try:
                response = self.client.get(url, **kwargs)
            except RETRY_EXCEPTIONS as e:
                if attempt >= self.retries:
                    raise
                delay = backoff_delay(attempt, self.backoff_factor)
                reason = type(e).__name__
            else:
                if response.status_code not in RETRY_STATUSES:
                    return response
                if attempt >= self.retries:
                    return response
                requested = retry_after_seconds(response)
                if requested is None:
                    delay = backoff_delay(attempt, self.backoff_factor)
                elif requested > MAX_RETRY_AFTER:
                    logger.info(
                        "%s from %s asked us to wait %.0fs (> %.0fs); not retrying",
                        response.status_code,
                        url,
                        requested,
                        MAX_RETRY_AFTER,
                    )
                    return response
                else:
                    delay = requested
                reason = str(response.status_code)

            logger.info(
                "%s for %s; retry %d/%d in %.1fs",
                reason,
                url,
                attempt + 1,
                self.retries,
                delay,
            )
            _sleep(delay)
            attempt += 1
