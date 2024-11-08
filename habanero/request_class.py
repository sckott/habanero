import math
import warnings

import httpx
from tqdm import tqdm  # type: ignore
from urllib3.exceptions import ConnectTimeoutError

from .exceptions import RequestError
from .filterhandler import filter_handler
from .habanero_utils import (
    check_json,
    filter_dict,
    ifelsestr,
    make_ua,
    rename_query_filters,
)


class Request(object):
    """
    Habanero: request class

    This is the request class for all requests
    """

    def __init__(
        self,
        mailto,
        ua_string,
        timeout,
        url,
        path,
        query=None,
        filter=None,
        offset=None,
        limit=None,
        sample=None,
        sort=None,
        order=None,
        facet=None,
        select=None,
        cursor=None,
        cursor_max=None,
        agency=False,
        progress_bar=False,
        **kwargs,
    ):
        self.mailto = mailto
        self.ua_string = ua_string
        self.timeout = timeout
        self.url = url
        self.path = path
        self.query = query
        self.filter = filter
        self.offset = offset
        self.limit = limit
        self.sample = sample
        self.sort = sort
        self.order = order
        self.facet = facet
        self.select = select
        self.cursor = cursor
        self.cursor_max = cursor_max
        self.agency = agency
        self.progress_bar = progress_bar
        self.kwargs = kwargs

    def _url(self):
        tmpurl = self.url + self.path
        return tmpurl.strip("/")

    def do_request(self, should_warn=False):
        filt = filter_handler(self.filter)
        if self.select.__class__ is list:
            self.select = ",".join(self.select)

        if not isinstance(self.cursor_max, (type(None), int)):
            raise ValueError("cursor_max must be of class int")

        payload = {
            "query": self.query,
            "filter": filt,
            "offset": self.offset,
            "rows": self.limit,
            "sample": self.sample,
            "sort": self.sort,
            "order": self.order,
            "facet": self.facet,
            "select": self.select,
            "cursor": self.cursor,
        }
        # convert limit/offset to str before removing None
        # b/c 0 (zero) is falsey, so that param gets dropped
        payload["offset"] = ifelsestr(payload["offset"])
        payload["rows"] = ifelsestr(payload["rows"])
        # remove params with value None
        payload = dict((k, v) for k, v in payload.items() if v)
        # add query filters
        payload.update(filter_dict(self.kwargs))
        # rename query filters
        payload = rename_query_filters(payload)

        js = self._req(payload=payload, should_warn=should_warn)
        if js is None:
            return js
        cu = js["message"].get("next-cursor")
        max_avail = js["message"]["total-results"]
        res = self._redo_req(js, payload, cu, max_avail, should_warn)
        return res

    def _redo_req(self, js, payload, cu, max_avail, should_warn):
        if cu.__class__.__name__ != "NoneType" and self.cursor_max > len(
            js["message"]["items"]
        ):
            res = [js]
            total = len(js["message"]["items"])

            # progress bar setup
            if self.progress_bar:
                actual_max = (
                    self.cursor_max if self.cursor_max is not None else max_avail
                )
                if max_avail < actual_max:
                    actual_max = max_avail
                runs = math.ceil(actual_max / (self.limit or 20))
                pbar = tqdm(total=runs - 1)

            while (
                cu.__class__.__name__ != "NoneType"
                and self.cursor_max > total
                and total < max_avail
            ):
                payload["cursor"] = cu
                out = self._req(payload=payload, should_warn=should_warn)
                cu = out["message"].get("next-cursor")
                res.append(out)
                total = sum([len(z["message"]["items"]) for z in res])
                if self.progress_bar:
                    pbar.update(1)
            if self.progress_bar:
                pbar.close()
            return res
        else:
            return js

    def _req(self, payload, should_warn):
        r = None
        try:
            r = httpx.get(
                self._url(),
                params=payload,
                headers=make_ua(self.mailto, self.ua_string),
                timeout=self.timeout,
            )
            r.raise_for_status()
        except httpx.HTTPStatusError:
            try:
                f = r.json()
                raise RequestError(r.status_code, f["message"][0]["message"])
            except:
                if should_warn:
                    mssg = "%s: %s" % (r.status_code, r.reason_phrase)
                    warnings.warn(mssg)
                    return None
                else:
                    r.raise_for_status()
        except ConnectTimeoutError as e:
            raise httpx.ConnectTimeout(e, r)
        except httpx.HTTPError as e:
            # print(e)
            raise RuntimeError(e)
        else:
            if not r:
                raise RuntimeError("An unknown problem occurred with an HTTP request")

            check_json(r)
            return r.json()
