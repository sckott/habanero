import copy
from collections.abc import Iterable, Iterator
from typing import Any

from .crossref import Crossref


class WorksQuery(Iterable[dict[str, Any]]):
    """
    Query builder for the Crossref API's works endpoint.

    Iterating over an instance (``for item in q``) yields individual work
    records as ``dict[str, Any]``.  Calling :meth:`execute` returns the raw
    Crossref API response as ``dict[str, Any]`` (the full envelope including
    ``message``, ``status``, etc.).  Calling :meth:`count` returns an ``int``.
    Calling :meth:`url` returns a ``str``.

    All builder methods (:meth:`query`, :meth:`filter`, :meth:`sort`,
    :meth:`order`, :meth:`select`, :meth:`facet`, :meth:`limit`,
    :meth:`cursor`) return a new :class:`WorksQuery` instance — the original
    is never mutated.

    :rtype: :class:`WorksQuery`

    Usage::

      from habanero import Crossref, WorksQuery
      cr = Crossref(mailto="myrmecocystus@gmail.com")
      q = WorksQuery(cr)

      # chain methods, nothing fires yet
      (
        q.query("climate change")
          .query(author="Hansen")
          .query(publisher_name="plos")
          .filter(from_pub_date="2010", has_funder="true")
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
      base = WorksQuery(cr).query("zika").filter(from_pub_date="2020")
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
        return iter(data["message"]["items"])

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

    def filter(self, **kwargs) -> "WorksQuery":
        new_filter = {**self._params.get("filter", {}), **kwargs}
        return self._clone(filter=new_filter)

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

    def cursor(self, value: str = "*", cursor_max: float = 5000) -> "WorksQuery":
        return self._clone(cursor=value, cursor_max=cursor_max)

    @property
    def url(self) -> str:
        from urllib.parse import urlencode

        base = "https://api.crossref.org"
        if self._endpoint == "works":
            path = "/works"
        else:
            path = (
                f"/{self._endpoint}/{self._ids}/works"
                if self._ids
                else f"/{self._endpoint}/works"
            )
        flat = {
            k: str(v)
            for k, v in self._params.items()
            if not isinstance(v, (dict, list))
        }
        return f"{base}{path}?{urlencode(flat)}"

    def count(self) -> int:
        params = {k: v for k, v in self._params.items() if k != "limit"}
        if self._endpoint == "works":
            result = self._cr.works(**params, limit=0)
        else:
            method = getattr(self._cr, self._endpoint)
            result = method(ids=self._ids, works=True, **params, limit=0)
        assert isinstance(result, dict)
        return result["message"]["total-results"]

    def _call_method(self, **extra_params) -> dict[str, Any] | list[dict[str, Any]]:
        params = {**self._params, **extra_params}
        if self._endpoint == "works":
            return self._cr.works(**params)
        method = getattr(self._cr, self._endpoint)
        return method(ids=self._ids, works=True, **params)

    def execute(self) -> dict[str, Any]:
        if self._result is None:
            result = self._call_method()
            assert isinstance(result, dict)
            self._result = result
        return self._result
