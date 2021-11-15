import pytest
import os
import vcr
from habanero import exceptions, Crossref
from requests.exceptions import HTTPError

cr = Crossref()

a = '{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2015,6,9]],"timestamp":1433817308344},"reference-count":0,"publisher":"Public Library of Science (PLoS)","issue":"3","DOI":"10.1371\\/journal.pone.0033693","type":"journal-article","page":"e33693","update-policy":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.corrections_policy","source":"CrossRef","title":["Methylphenidate Exposure Induces Dopamine Neuron Loss and Activation of Microglia in the Basal Ganglia of Mice"],"prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1371","volume":"7","author":[{"affiliation":[],"family":"Sadasivan","given":"Shankar"},{"affiliation":[],"family":"Pond","given":"Brooks B."},{"affiliation":[],"family":"Pani","given":"Amar K."},{"affiliation":[],"family":"Qu","given":"Chunxu"},{"affiliation":[],"family":"Jiao","given":"Yun"},{"affiliation":[],"family":"Smeyne","given":"Richard J."}],"member":"http:\\/\\/id.crossref.org\\/member\\/340","container-title":["PLoS ONE"],"deposited":{"date-parts":[[2014,3,5]],"timestamp":1393977600000},"score":1.0,"subtitle":[],"editor":[{"affiliation":[],"family":"Borlongan","given":"Cesario V."}],"issued":{"date-parts":[[2012,3,21]]},"URL":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.0033693","ISSN":["1932-6203"],"subject":["Agricultural and Biological Sciences(all)","Medicine(all)","Biochemistry, Genetics and Molecular Biology(all)"]}}'


@pytest.mark.vcr
def test_prefixes():
    "prefixes - basic test"
    res = cr.prefixes(ids="10.1016")
    assert dict == res.__class__
    assert dict == res["message"].__class__


@pytest.mark.vcr
def test_prefixes_works():
    "prefixes - param: works"
    res = cr.prefixes(ids="10.1016", works=True, sample=2)
    assert dict == res.__class__


@pytest.mark.vcr
def test_prefixes_filter():
    "prefixes - param: filter"
    with pytest.raises(Exception):
        cr.prefixes(filter={"has_full_text": True})


@pytest.mark.vcr
def test_prefixes_field_queries():
    "prefixes - param: kwargs - field queries work as expected"
    res = cr.prefixes(
        ids="10.1371",
        works=True,
        query_editor="cooper",
        filter={"type": "journal-article"},
    )
    eds = [x.get("editor")[0] for x in res["message"]["items"]]
    assert dict == res.__class__
    assert 5 == len(res["message"])
    assert list == eds.__class__
    assert dict == eds[0].__class__


@pytest.mark.vcr
def test_prefixes_query_filters_not_allowed_with_dois():
    "prefixes - param: kwargs - query filters not allowed on prefixes/prefix/ route"
    with pytest.raises(HTTPError):
        cr.prefixes(ids="10.1371", query_editor="cooper")


@pytest.mark.vcr
def test_prefixes_bad_id_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.prefixes(ids="10.9999", warn=True)
    assert out is None


@pytest.mark.vcr
def test_prefixes_mixed_ids_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.prefixes(ids=["10.1371", "10.9999"], warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None


@pytest.mark.vcr
def test_prefixes_bad_id_works_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.prefixes(ids="10.9999", works=True, warn=True)
    assert out is None


@pytest.mark.vcr
def test_prefixes_mixed_ids_works_warn():
    "prefixes - param: warn"
    with pytest.warns(UserWarning):
        out = cr.prefixes(ids=["10.1371", "10.9999"], works=True, warn=True)
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None
