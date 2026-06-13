VALID_FIELD_QUERIES: list[str] = [
    "query.affiliation",
    "query.author",
    "query.bibliographic",
    "query.chair",
    "query.container-title",
    "query.contributor",
    "query.degree",
    "query.description",
    "query.editor",
    "query.event-acronym",
    "query.event-location",
    "query.event-name",
    "query.event-sponsor",
    "query.event-theme",
    "query.funder-name",
    "query.publisher-location",
    "query.publisher-name",
    "query.standards-body-acronym",
    "query.standards-body-name",
    "query.title",
    "query.translator",
]


def validate_field_queries(query: str | list[str] | None) -> None:
    """Validate field queries against the list of valid field queries.

    Usage::

      validate_field_queries("query.event-acronym")
      validate_field_queries("query.chair")
      validate_field_queries(["query.event-acronym", "query.chair"])
      # bad
      validate_field_queries("nope")
      # list
      validate_field_queries(["query.chair", "query.title"])
      # bad list
      validate_field_queries(["query.chair", "query.title", "nope"])
    """
    if not query:
        return

    if isinstance(query, list):
        for q in query:
            if q not in VALID_FIELD_QUERIES:
                raise ValueError(f"Invalid field query: {q}")
    else:
        if query not in VALID_FIELD_QUERIES:
            raise ValueError(f"Invalid field query: {query}")
