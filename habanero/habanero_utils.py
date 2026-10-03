import json
import re
from typing import Any

import httpx2

from . import __version__
from .exceptions import IncompatibleParameterError, RequestError


def sub_str(x: str | None, n: int = 3) -> str | None:
    if x is None:
        return None
    else:
        return str(x[:n]) + "***"


def check_kwargs(keys: list, kwargs: dict) -> None:
    for x in range(len(keys)):
        if keys[x] in kwargs:
            mssg = f"The {keys[x]} parameter is not allowed with this method"
            raise IncompatibleParameterError(mssg)


def check_filter_kwarg(kwargs: dict) -> None:
    """Raise if the old `filter` parameter was passed instead of `filters`

    `filter` would otherwise be silently dropped, so the request would run
    with no filters applied at all
    """
    if "filter" in kwargs:
        mssg = (
            "The `filter` parameter is no longer supported; use `filters` "
            "instead, e.g., `filters = {'has_full_text': True}`. Passing "
            "`filter` would have meant no filters were applied at all"
        )
        raise IncompatibleParameterError(mssg)


def check_unknown_kwargs(kwargs: dict) -> None:
    """Raise if any keyword argument is not a field query (`query_<field>`)

    Field queries are the only extra keyword arguments the Crossref methods
    use. Anything else would otherwise be silently dropped, e.g., a typo like
    `qurey_author`, or `rows` instead of `limit`
    """
    unknown = sorted(k for k in kwargs if not k.startswith("query_"))
    if unknown:
        names = ", ".join(f"'{k}'" for k in unknown)
        raise TypeError(
            f"unexpected keyword argument(s): {names}. Only field queries "
            "(`query_<field>`, e.g., `query_author`) are accepted as extra "
            "keyword arguments"
        )


def check_json(x: httpx2.Response) -> None:
    ctype = x.headers["Content-Type"]
    matched = re.match("application/json", ctype)
    if matched is None:
        scode = x.status_code
        if str(x.text) == "Not implemented.":
            scode = 400
        raise RequestError(scode, str(x.text))


def is_json(x: httpx2.Response) -> bool:
    try:
        json.loads(x.content)
    except ValueError:  # JSONDecodeError is a subclass of ValueError
        return False
    return True


def parse_json_err(x: httpx2.Response) -> str:
    msg = x.json()["message"]
    if isinstance(msg, str):
        return msg
    else:
        failed_parse_msg = "failed to parse error message"
        try:
            msg = msg[0]["message"]
        except TypeError:
            msg = failed_parse_msg

        return msg


def make_ua(mailto: str | None = None, ua_string: str | None = None) -> dict[str, str]:
    requa = "python-httpx2/" + httpx2.__version__
    habua = f"habanero/{__version__}"
    ua = requa + " " + habua
    if mailto is not None:
        ua = ua + f" (mailto:{mailto})"
    if ua_string is not None:
        ua = ua + " " + ua_string
    strg = {"User-Agent": ua, "X-USER-AGENT": ua}
    return strg


def filter_dict(x: dict[str, Any | None]) -> dict[str, Any]:
    return {k: v for k, v in x.items() if k.find("query_") == 0 and v is not None}


def rename_query_filters(x: dict) -> dict:
    newkeys = [re.sub("query_", "query.", v) for v in x]
    newkeys = [re.sub("_", "-", v) for v in newkeys]
    mapping = dict(zip(x.keys(), newkeys, strict=True))
    return {mapping[k]: v for k, v in x.items()}


def ifelsestr(x: Any | None) -> str | None:
    z = str(x) if x is not None else x
    return z
