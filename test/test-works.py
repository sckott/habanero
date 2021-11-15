import pytest
import os
import vcr
import requests
from habanero import exceptions, Crossref
from requests.exceptions import HTTPError

cr = Crossref()

a = '{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2015,6,9]],"timestamp":1433817308344},"reference-count":0,"publisher":"Public Library of Science (PLoS)","issue":"3","DOI":"10.1371\\/journal.pone.0033693","type":"journal-article","page":"e33693","update-policy":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.corrections_policy","source":"CrossRef","title":["Methylphenidate Exposure Induces Dopamine Neuron Loss and Activation of Microglia in the Basal Ganglia of Mice"],"prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1371","volume":"7","author":[{"affiliation":[],"family":"Sadasivan","given":"Shankar"},{"affiliation":[],"family":"Pond","given":"Brooks B."},{"affiliation":[],"family":"Pani","given":"Amar K."},{"affiliation":[],"family":"Qu","given":"Chunxu"},{"affiliation":[],"family":"Jiao","given":"Yun"},{"affiliation":[],"family":"Smeyne","given":"Richard J."}],"member":"http:\\/\\/id.crossref.org\\/member\\/340","container-title":["PLoS ONE"],"deposited":{"date-parts":[[2014,3,5]],"timestamp":1393977600000},"score":1.0,"subtitle":[],"editor":[{"affiliation":[],"family":"Borlongan","given":"Cesario V."}],"issued":{"date-parts":[[2012,3,21]]},"URL":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.0033693","ISSN":["1932-6203"],"subject":["Agricultural and Biological Sciences(all)","Medicine(all)","Biochemistry, Genetics and Molecular Biology(all)"]}}'


@pytest.mark.vcr
def test_works_with_one_id():
    "works - param: ids, one DOI"
    res = cr.works(ids="10.1371/journal.pone.0033693")
    assert dict == res.__class__
    assert 4 == len(res)
    assert "work" == res["message-type"]


@pytest.mark.vcr
def test_works_with_many_ids():
    "works - param: ids, many DOIs"
    dois = [
        "10.1016/j.neurobiolaging.2010.03.024",
        "10.1002/jor.1100150407",
        "10.1038/srep16696",
        "10.1109/icdcsw.2003.1203662",
        "10.3892/ijo_00000353",
    ]
    res = cr.works(ids=dois)
    assert list == res.__class__
    assert 5 == len(res)
    assert [4, 4, 4, 4, 4] == [len(x) for x in res]
    assert "work" == [x["message-type"] for x in res][0]
    assert dois[0] == res[0]["message"]["DOI"]


# def test_works_doesnt_allow_cursor_with_ids_input():
#     "works - param: ids, cursor not supported with DOIs"
#     res1 = cr.works(ids = '10.1016/j.neurobiolaging.2010.03.024', cursor = "*")
#     res2 = cr.works(ids = '10.1016/j.neurobiolaging.2010.03.024')
#     assert res1 == res2


@pytest.mark.vcr
def test_works_no_id_withlimit():
    "works - param: limit, no other inputs"
    res = cr.works(limit=2)
    assert dict == res.__class__
    assert 5 == len(res["message"])
    assert 2 == len(res["message"]["items"])


@pytest.mark.vcr
def test_works_query():
    "works - param: query"
    res = cr.works(query="ecology", limit=2)
    assert dict == res.__class__
    assert 5 == len(res["message"])


@pytest.mark.vcr
def test_works_sample():
    "works - param: sample"
    res = cr.works(sample=2)
    assert dict == res.__class__
    assert 5 == len(res["message"])


# FIXME: this is constantly failing for unknown reason
# def test_works_filter():
#     "works - param: filter"
#     res = cr.works(filter = {'has_full_text': True}, limit = 3)
#     assert dict == res.__class__
#     assert 5 == len(res['message'])


@pytest.mark.vcr
def test_works_field_queries():
    "works - param: kwargs - field queries work as expected"
    res = cr.works(query="ecology", query_author="carl boettiger")
    auths = [x["author"][0]["family"] for x in res["message"]["items"]]
    assert dict == res.__class__
    assert 5 == len(res["message"])
    assert "Boettiger" in auths


@pytest.mark.vcr
def test_works_query_filters_not_allowed_with_dois():
    "works - param: kwargs - query filters not allowed on works/DOI/ route"
    with pytest.raises(HTTPError):
        cr.works(ids="10.1371/journal.pone.0033693", query_author="carl boettiger")


@pytest.mark.vcr
def test_works_with_select_param():
    "works - param: select"
    res1 = cr.works(query="ecology", select="DOI,title")
    assert list(res1["message"]["items"][0].keys()) == ["DOI", "title"]


@pytest.mark.vcr
def test_works_bad_id_warn():
    "works - param: warn"
    with pytest.warns(UserWarning):
        out = cr.works(ids="10.1371/notarealdoi", warn=True)
    assert out is None


@pytest.mark.vcr
def test_works_mixed_ids_warn():
    "works - param: warn"
    with pytest.warns(UserWarning):
        out = cr.works(
            ids=["10.1371/journal.pone.0033693", "10.1371/notarealdoi"], warn=True
        )
    assert len(out) == 2
    assert isinstance(out[0], dict)
    assert out[1] is None
