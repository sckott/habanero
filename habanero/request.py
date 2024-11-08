import warnings

import httpx

from .exceptions import RequestError
from .filterhandler import filter_handler
from .habanero_utils import (
    check_json,
    filter_dict,
    ifelsestr,
    is_json,
    make_ua,
    parse_json_err,
    rename_query_filters,
)
from .request_class import Request


def request(
    cr,
    path,
    ids=None,
    query=None,
    filter=None,
    offset=None,
    limit=None,
    sample=None,
    sort=None,
    order=None,
    facet=None,
    select=None,
    works=None,
    cursor=None,
    cursor_max=None,
    agency=False,
    progress_bar=False,
    should_warn=False,
    **kwargs,
):
    """HTTP request helper."""
    warning_thrown = False
    url = cr.base_url + path

    if cursor_max.__class__.__name__ != "NoneType":
        if not isinstance(cursor_max, int):
            raise ValueError("cursor_max must be of class int")

    filt = filter_handler(filter)
    if select.__class__ is list:
        select = ",".join(select)

    payload = {
        "query": query,
        "filter": filt,
        "offset": offset,
        "rows": limit,
        "sample": sample,
        "sort": sort,
        "order": order,
        "facet": facet,
        "select": select,
        "cursor": cursor,
    }
    # convert limit/offset to str before removing None
    # b/c 0 (zero) is falsey, so that param gets dropped
    payload["offset"] = ifelsestr(payload["offset"])
    payload["rows"] = ifelsestr(payload["rows"])
    # remove params with value None
    payload = dict((k, v) for k, v in payload.items() if v)
    # add query filters
    payload.update(filter_dict(kwargs))
    # rename query filters
    payload = rename_query_filters(payload)

    if ids.__class__.__name__ == "NoneType":
        url = url.strip("/")
        try:
            r = httpx.get(
                url,
                params=payload,
                headers=make_ua(cr.mailto, cr.ua_string),
                timeout=cr.timeout,
            )
            r.raise_for_status()
        except httpx.HTTPStatusError:
            if is_json(r):
                raise RequestError(r.status_code, parse_json_err(r))
            else:
                r.raise_for_status()
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP Exception for {e.request.url} - {e}")
            # raise RuntimeError(e)
        else:
            if not r:
                raise RuntimeError("An unknown problem occurred with an HTTP request")

            check_json(r)
            coll = r.json()
    else:
        if ids.__class__.__name__ == "str":
            ids = ids.split()
        if ids.__class__.__name__ == "int":
            ids = [ids]
        # should_warn = len(ids) > 1
        coll = []
        for i in range(len(ids)):
            if works:
                res = Request(
                    cr.mailto,
                    cr.ua_string,
                    cr.timeout,
                    url,
                    str(ids[i]) + "/works",
                    query,
                    filter,
                    offset,
                    limit,
                    sample,
                    sort,
                    order,
                    facet,
                    select,
                    cursor,
                    cursor_max,
                    None,
                    progress_bar,
                    **kwargs,
                ).do_request(should_warn=should_warn)
                coll.append(res)
            else:
                if agency:
                    endpt = url + str(ids[i]) + "/agency"
                else:
                    endpt = url + str(ids[i])

                endpt = endpt.strip("/")

                r = httpx.get(
                    endpt,
                    params=payload,
                    headers=make_ua(cr.mailto, cr.ua_string),
                    timeout=cr.timeout,
                )
                if r.status_code > 201 and should_warn:
                    warning_thrown = True
                    mssg = "%s on %s: %s" % (r.status_code, ids[i], r.reason_phrase)
                    warnings.warn(mssg)
                else:
                    r.raise_for_status()

                if warning_thrown:
                    coll.append(None)
                else:
                    check_json(r)
                    js = r.json()
                    coll.append(js)

                warning_thrown = False

        if len(coll) == 1:
            coll = coll[0]

    return coll
