VALID_FACETS: list[str] = [
    "affiliation",
    "archive",
    "assertion",
    "assertion-group",
    "category-name",
    "container-title",
    "funder-doi",
    "funder-name",
    "issn",
    "journal-issue",
    "journal-volume",
    "license",
    "link-application",
    "orcid",
    "published",
    "publisher-name",
    "relation-type",
    "ror-id",
    "source",
    "type-name",
    "update-type",
]


def validate_facets(facets: str | None) -> None:
    """Validate the facets string against the list of valid facets.
    Usage::

      validate_facets("affiliation")
      validate_facets("affiliation:3")
      validate_facets("affiliation:3,issn:5,ror-id:*")
      # bad
      validate_facets("notarealfacet")
      validate_facets("affiliation:3,issn:abc,ror-id:*")
    """
    if facets is None:
        return

    for facet in facets.split(","):
        if ":" in facet:
            facet_name, facet_value = facet.split(":")
            if facet_name not in facets:
                raise ValueError(f"Invalid facet name: {facet_name}")

            if facet_value == "*":
                continue

            try:
                int(facet_value)
            except ValueError:
                raise ValueError(f"Invalid facet value: {facet_value}")
        else:
            if facet not in VALID_FACETS:
                raise ValueError(f"Invalid facet: {facet}")
