import copy
from collections.abc import Iterable, Iterator
from typing import Any

import httpx2

from ..request_class import Request
from .crossref import Crossref


class WorksQuery(Iterable[dict[str, Any]]):
    """
    Query builder for the Crossref API's works endpoint.

    Iterating over an instance (``for item in q``) yields individual work
    records as ``dict[str, Any]``, across all pages when :meth:`cursor` is
    used.  Calling :meth:`execute` returns the raw Crossref API response, the
    same thing the wrapped :class:`~habanero.Crossref` method returns: a
    ``dict[str, Any]`` (the full envelope including ``message``, ``status``,
    etc.), or a ``list`` of such dicts, one per page, when :meth:`cursor`
    paged through several pages.  Calling :meth:`count` returns an ``int``.
    Calling :meth:`url` returns a ``str``.

    All builder methods (:meth:`query`, :meth:`filters`, :meth:`sort`,
    :meth:`order`, :meth:`select`, :meth:`facet`, :meth:`limit`,
    :meth:`cursor`) return a new :class:`WorksQuery` instance — the original
    is never mutated.

    :rtype: :class:`WorksQuery`

    Usage::

      from habanero import Crossref, WorksQuery
      cr = Crossref()
      q = WorksQuery(cr)

      # chain methods, nothing fires yet
      (
        q.query("climate change")
          .query(author="Hansen")
          .query(publisher_name="plos")
          .filters(from_pub_date="2010", has_funder="true")
          .sort("published")
          .order("desc")
          .select("DOI", "title", "author", "published")
          .limit(50)
      )

      # inspect before fetching
      print(q)         # WorksQuery({...params...})
      print(q.url)     # https://api.crossref.org/works?query=...

      # get count without pulling records
      print(q.count()) # e.g. 12483

      # pull records — fires the request here
      for item in q:
          print(item["DOI"], item.get("title"))

      # or execute manually
      q.execute()

      # instances are immutable, so each call returns a new instance
      # so you can chain calls without modifying the original instance
      # compare the two modifications of the `base` query
      base = WorksQuery(cr).query("zika").filters(from_pub_date="2020")
      base.sort("published").order("asc")
      base.sort("published").order("desc")
    """

    def __init__(self, cr: Crossref | None = None):
        self._cr = cr or Crossref()
        self._params = {}
        self._endpoint = "works"
        self._ids = None
        self._result = None

    def __iter__(self) -> Iterator[dict[str, Any]]:
        data = self.execute()
        pages = data if isinstance(data, list) else [data]
        return (item for page in pages for item in page["message"]["items"])

    def __repr__(self):
        ids_part = f", ids={self._ids!r}" if self._ids else ""
        return (
            f"WorksQuery(endpoint={self._endpoint!r}{ids_part}, params={self._params})"
        )

    def _clone(self, **updates):
        clone = copy.copy(self)
        clone._params = copy.deepcopy({**self._params, **updates})
        clone._result = None  # fresh clone shouldn't inherit cached results
        return clone

    def journals(self, ids=None) -> "WorksQuery":
        clone = self._clone()
        clone._endpoint = "journals"
        clone._ids = ids
        return clone

    def members(self, ids=None) -> "WorksQuery":
        clone = self._clone()
        clone._endpoint = "members"
        clone._ids = ids
        return clone

    def funders(self, ids=None) -> "WorksQuery":
        clone = self._clone()
        clone._endpoint = "funders"
        clone._ids = ids
        return clone

    def prefixes(self, ids=None) -> "WorksQuery":
        clone = self._clone()
        clone._endpoint = "prefixes"
        clone._ids = ids
        return clone

    def types(self, ids=None) -> "WorksQuery":
        clone = self._clone()
        clone._endpoint = "types"
        clone._ids = ids
        return clone

    def query(self, q: str | None = None, **kwargs) -> "WorksQuery":
        updates = {}
        if q:
            updates["query"] = q
        for k, v in kwargs.items():
            updates[f"query_{k}"] = v
        return self._clone(**updates)

    def filters(self, **kwargs) -> "WorksQuery":
        new_filters = {**self._params.get("filters", {}), **kwargs}
        return self._clone(filters=new_filters)

    def sort(self, field: str) -> "WorksQuery":
        return self._clone(sort=field)

    def order(self, direction: str) -> "WorksQuery":
        return self._clone(order=direction)

    def select(self, *fields: str) -> "WorksQuery":
        return self._clone(select=list(fields))

    def facet(self, name: str, count: int) -> "WorksQuery":
        existing = self._params.get("facet")
        new_facet = f"{existing},{name}:{count}" if existing else f"{name}:{count}"
        return self._clone(facet=new_facet)

    def limit(self, n: int) -> "WorksQuery":
        return self._clone(limit=n)

    def cursor(self, value: str = "*", cursor_max: int | None = 5000) -> "WorksQuery":
        return self._clone(cursor=value, cursor_max=cursor_max)

    @property
    def url(self) -> str:
        """The URL that :meth:`execute` requests.

        Built with the same code that builds the real request, so it matches
        what is sent. With multiple ``ids`` several requests are made; the URL
        for the first one is returned.
        """
        ids = self._ids
        if isinstance(ids, str):
            ids = ids.split()
        elif isinstance(ids, int):
            ids = [ids]

        if self._endpoint == "works":
            path = "/works"
        elif ids:
            path = f"/{self._endpoint}/{ids[0]}/works"
        else:
            path = f"/{self._endpoint}"

        params = copy.deepcopy(self._params)
        req = Request(
            self._cr.mailto,
            self._cr.ua_string,
            self._cr.timeout,
            self._cr.base_url,
            path,
            params.pop("query", None),
            params.pop("filters", None),
            params.pop("offset", None),
            params.pop("limit", None),
            params.pop("sample", None),
            params.pop("sort", None),
            params.pop("order", None),
            params.pop("facet", None),
            params.pop("select", None),
            params.pop("cursor", None),
            params.pop("cursor_max", 5000),
            **params,
        )
        return str(httpx2.Request("GET", req._url(), params=req.payload()).url)

    def count(self) -> int:
        # cursor/cursor_max are dropped too: count() needs a single request,
        # and paging with limit=0 would only ever return empty pages
        params = {
            k: v
            for k, v in self._params.items()
            if k not in ("limit", "cursor", "cursor_max")
        }
        if self._endpoint == "works":
            result = self._cr.works(**params, limit=0)
        else:
            method = getattr(self._cr, self._endpoint)
            result = method(ids=self._ids, works=True, **params, limit=0)
        if not isinstance(result, dict):
            raise TypeError(
                f"count() expected a single response dict, got {type(result).__name__}"
            )
        return result["message"]["total-results"]

    def _call_method(self, **extra_params) -> dict[str, Any] | list[dict[str, Any]]:
        params = copy.deepcopy({**self._params, **extra_params})
        if self._endpoint == "works":
            return self._cr.works(**params)
        method = getattr(self._cr, self._endpoint)
        return method(ids=self._ids, works=True, **params)

    def execute(self) -> dict[str, Any] | list[dict[str, Any]]:
        """Run the query and return the raw response.

        Returns a ``dict``, or a ``list`` of ``dict`` (one per page) when
        :meth:`cursor` paged through several pages.
        """
        if self._result is None:
            result = self._call_method()
            if not isinstance(result, (dict, list)):
                raise TypeError(
                    "no usable response was returned (the request may have "
                    f"failed); got {type(result).__name__}"
                )
            self._result = result
        return self._result
