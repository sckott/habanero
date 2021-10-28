from ..cnrequest import CNRequest
from .constants import *


def content_negotiation(
    ids, format="bibtex", style="apa", locale="en-US", url=None, **kwargs
):
    """
    Get citations in various formats from CrossRef

    Supports DOIs from Crossref, Datacite and Medra

    :param ids: [str] required. a single DOI or many DOIs, each a string. If many
        passed in, do so in a list
    :param format: [str] Name of the format. One of "rdf-xml", "turtle", "citeproc-json",
        "citeproc-json-ish", "text", "ris", "bibtex" (Default), "crossref-xml",
        "datacite-xml","bibentry", or "crossref-tdm"
    :param style: [str] A CSL style (for text format only). See :func:`~habanero.cn.csl_styles`
        for options. Default: "apa". If there's a style that CrossRef doesn't support
        you'll get a `(500) Internal Server Error`
    :param locale: [str] Language locale. See `locale.locale_alias`
    :param url: [str] Base URL for the content negotiation request. Default: `https://doi.org`
    :param kwargs: any additional arguments will be passed on to `requests.get`

    :return: string, which can be parsed to various formats depending on what
        format you request (e.g., JSON vs. XML vs. bibtex)

    See https://citation.crosscite.org/docs.html for details

    To make for a nicer user experience, when more than one DOI is passed to
    `ids` we'll throw a warning instead of stopping with an error to be able
    to try to fetch data for all DOIs given. When only one DOI is passed to
    `ids` we will fail with error message. A UserWarning is thrown when a DOI
    is not found or there's a problem with fetching the citation for a DOI.
    You can suppress these warnings with :code:`warnings.filterwarnings('ignore')`.

    Usage::

        from habanero import cn
        cn.content_negotiation(ids = "10.1126/science.169.3946.635")

        # A Medra DOI
        cn.content_negotiation(ids = "10.1400/22888")

        # get citeproc-json
        cn.content_negotiation(ids = '10.1126/science.169.3946.635', format = "citeproc-json")

        # some other formats
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "rdf-xml")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "crossref-xml")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text")

        # return an R bibentry type
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "bibentry")

        # return an apa style citation
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "apa")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "harvard3")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "elsevier-harvard")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "ecoscience")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "heredity")
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "oikos")

        # Using DataCite DOIs
        ## some formats don't work
        # cn.content_negotiation(ids = "10.15468/t4rau8", format = "crossref-xml")

        ## But most do work
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "text")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "crossref-tdm")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "datacite-xml")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "rdf-xml")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "turtle")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "ris")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "bibtex")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "bibentry")
        cn.content_negotiation(ids = "10.15468/t4rau8", format = "bibtex")

        # many DOIs
        dois = ['10.5167/UZH-30455','10.5167/UZH-49216','10.5167/UZH-503', '10.5167/UZH-38402','10.5167/UZH-41217']
        x = cn.content_negotiation(ids = dois)

        # Use a different base url
        url = "http://dx.doi.org"
        cn.content_negotiation(ids = "10.1126/science.169.3946.635", url = url)
    """
    if url is None:
        url = cn_base_url
    return CNRequest(url, ids, format, style, locale, **kwargs)
