"""Tests for Crossref.works"""
import os
import vcr
from nose.tools import *
from habanero import Crossref
from habanero import RequestError
cr = Crossref()

a = '{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2015,6,9]],"timestamp":1433817308344},"reference-count":0,"publisher":"Public Library of Science (PLoS)","issue":"3","DOI":"10.1371\\/journal.pone.0033693","type":"journal-article","page":"e33693","update-policy":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.corrections_policy","source":"CrossRef","title":["Methylphenidate Exposure Induces Dopamine Neuron Loss and Activation of Microglia in the Basal Ganglia of Mice"],"prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1371","volume":"7","author":[{"affiliation":[],"family":"Sadasivan","given":"Shankar"},{"affiliation":[],"family":"Pond","given":"Brooks B."},{"affiliation":[],"family":"Pani","given":"Amar K."},{"affiliation":[],"family":"Qu","given":"Chunxu"},{"affiliation":[],"family":"Jiao","given":"Yun"},{"affiliation":[],"family":"Smeyne","given":"Richard J."}],"member":"http:\\/\\/id.crossref.org\\/member\\/340","container-title":["PLoS ONE"],"deposited":{"date-parts":[[2014,3,5]],"timestamp":1393977600000},"score":1.0,"subtitle":[],"editor":[{"affiliation":[],"family":"Borlongan","given":"Cesario V."}],"issued":{"date-parts":[[2012,3,21]]},"URL":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.0033693","ISSN":["1932-6203"],"subject":["Agricultural and Biological Sciences(all)","Medicine(all)","Biochemistry, Genetics and Molecular Biology(all)"]}}'

@vcr.use_cassette('test/vcr_cassettes/works_oneid.yaml')
def test_works_with_one_id():
    "works - param: ids, one DOI"
    res = cr.works(ids = '10.1371/journal.pone.0033693')
    assert dict == res.__class__
    assert 4 == len(res)
    assert 'work' == res['message-type']

@vcr.use_cassette('test/vcr_cassettes/works_manyids.yaml')
def test_works_with_many_ids():
    "works - param: ids, many DOIs"
    dois = ['10.1016/j.neurobiolaging.2010.03.024', '10.1002/jor.1100150407',
    '10.1038/srep16696', '10.1109/icdcsw.2003.1203662', '10.3892/ijo_00000353']
    res = cr.works(ids = dois)
    assert list == res.__class__
    assert 5 == len(res)
    assert [4, 4, 4, 4, 4] == [ len(x) for x in res ]
    assert 'work' == [ x['message-type'] for x in res ][0]
    assert dois[0] == res[0]['message']['DOI']

# def test_works_doesnt_allow_cursor_with_ids_input():
#     "works - param: ids, cursor not supported with DOIs"
#     res1 = cr.works(ids = '10.1016/j.neurobiolaging.2010.03.024', cursor = "*")
#     res2 = cr.works(ids = '10.1016/j.neurobiolaging.2010.03.024')
#     assert res1 == res2

@vcr.use_cassette('test/vcr_cassettes/works_no_id_withlimit.yaml')
def test_works_no_id_withlimit():
    "works - param: limit, no other inputs"
    res = cr.works(limit = 2)
    assert dict == res.__class__
    assert 5 == len(res['message'])
    assert 2 == len(res['message']['items'])

@vcr.use_cassette('test/vcr_cassettes/works_query.yaml')
def test_works_query():
    "works - param: query"
    res = cr.works(query = "ecology", limit = 2)
    assert dict == res.__class__
    assert 5 == len(res['message'])

@vcr.use_cassette('test/vcr_cassettes/works_sample.yaml')
def test_works_sample():
    "works - param: sample"
    res = cr.works(sample = 2)
    assert dict == res.__class__
    assert 5 == len(res['message'])

# FIXME: this is constantly failing for unknown reason
# def test_works_filter():
#     "works - param: filter"
#     res = cr.works(filter = {'has_full_text': True}, limit = 3)
#     assert dict == res.__class__
#     assert 5 == len(res['message'])

@vcr.use_cassette('test/vcr_cassettes/works_field_queries.yaml')
def test_works_field_queries():
    "works - param: kwargs - field queries work as expected"
    res = cr.works(query = "ecology", query_author = 'carl boettiger')
    auths = [ x['author'][0]['family'] for x in res['message']['items'] ]
    assert dict == res.__class__
    assert 5 == len(res['message'])
    assert "Boettiger" in auths

@raises(RequestError)
@vcr.use_cassette('test/vcr_cassettes/works_query_filters_not_allowed_with_dois.yaml')
def test_works_query_filters_not_allowed_with_dois():
    "works - param: kwargs - query filters not allowed on works/DOI/ route"
    cr.works(ids = '10.1371/journal.pone.0033693', query_author = 'carl boettiger')
