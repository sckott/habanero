VALID_SELECTS: list[str] = [
    "DOI",
    "ISBN",
    "ISSN",
    "URL",
    "abstract",
    "accepted",
    "alternative-id",
    "approved",
    "archive",
    "article-number",
    "assertion",
    "author",
    "chair",
    "clinical-trial-number",
    "container-title",
    "content-created",
    "content-domain",
    "contributor",
    "created",
    "degree",
    "deposited",
    "editor",
    "event",
    "funder",
    "group-title",
    "indexed",
    "is-referenced-by-count",
    "issn-type",
    "issue",
    "issued",
    "license",
    "link",
    "member",
    "original-title",
    "page",
    "posted",
    "prefix",
    "published",
    "published-online",
    "published-print",
    "publisher",
    "publisher-location",
    "reference",
    "references-count",
    "relation",
    "resource",
    "score",
    "short-container-title",
    "short-title",
    "standards-body",
    "subject",
    "subtitle",
    "title",
    "translator",
    "type",
    "update-policy",
    "update-to",
    "updated-by",
    "volume",
]


def validate_select(select: str | list[str] | None) -> None:
    """Validate the select string against the list of valid selects.
    Usage::

      validate_select("created")
      validate_select("deposited")
      validate_select("published")
      validate_select("created,published")
      # bad
      validate_select("notarealselect")
      # list
      validate_select(["created", "deposited", "published"])
      # bad list
      validate_select(["created", "deposited", "notarealselect"])
    """
    if select is None:
        return

    if isinstance(select, list):
        for s in select:
            if s not in VALID_SELECTS:
                raise ValueError(f"Invalid select name: {s}")
    else:
        if "," in select:
            for s in select.split(","):
                if s not in VALID_SELECTS:
                    raise ValueError(f"Invalid select name: {s}")
        else:
            if select not in VALID_SELECTS:
                raise ValueError(f"Invalid select name: {select}")
