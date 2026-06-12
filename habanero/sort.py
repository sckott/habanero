VALID_SORTS: list[str] = [
    "created",
    "deposited",
    "indexed",
    "is-referenced-by-count",
    "issued",
    "published",
    "published-online",
    "published-print",
    "references-count",
    "relevance",
    "score",
    "updated",
]


def validate_sort(sort: str | None) -> None:
    """Validate the sort string against the list of valid sorts.
    Usage::

      validate_sort("created")
      validate_sort("deposited")
      validate_sort("published")
      # bad
      validate_sort("notarealfacet")
    """
    if sort is None:
        return

    if sort not in VALID_SORTS:
        raise ValueError(f"Invalid sort name: {sort}")
