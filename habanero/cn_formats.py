cn_formats = [
    "rdf-xml",
    "turtle",
    "citeproc-json",
    "citeproc-json-ish",
    "text",
    "ris",
    "bibtex",
    "crossref-xml",
    "datacite-xml",
    "bibentry",
    "crossref-tdm",
]

cn_format_headers = {
    "rdf-xml": "application/rdf+xml",
    "turtle": "text/turtle",
    "citeproc-json": "transform/application/vnd.citationstyles.csl+json",
    "text": "text/x-bibliography",
    "ris": "application/x-research-info-systems",
    "bibtex": "application/x-bibtex",
    "crossref-xml": "application/vnd.crossref.unixref+xml",
    "datacite-xml": "application/vnd.datacite.datacite+xml",
    "bibentry": "application/x-bibtex",
    "crossref-tdm": "application/vnd.crossref.unixsd+xml",
}

cn_types = {
    "rdf-xml": "text/xml",
    "turtle": "text/plain",
    "citeproc-json": "application/json",
    "citeproc-json-ish": "application/json",
    "text": "text/plain",
    "ris": "text/plain",
    "bibtex": "text/plain",
    "crossref-xml": "text/xml",
    "datacite-xml": "text/xml",
    "bibentry": "text/plain",
    "crossref-tdm": "text/xml",
}
