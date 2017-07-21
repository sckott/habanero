"""Tests for Crossref.members"""
import os
import vcr
from nose.tools import *

from habanero import exceptions

from habanero import Crossref
cr = Crossref()

a = '{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2015,6,9]],"timestamp":1433817308344},"reference-count":0,"publisher":"Public Library of Science (PLoS)","issue":"3","DOI":"10.1371\\/journal.pone.0033693","type":"journal-article","page":"e33693","update-policy":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.corrections_policy","source":"CrossRef","title":["Methylphenidate Exposure Induces Dopamine Neuron Loss and Activation of Microglia in the Basal Ganglia of Mice"],"prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1371","volume":"7","author":[{"affiliation":[],"family":"Sadasivan","given":"Shankar"},{"affiliation":[],"family":"Pond","given":"Brooks B."},{"affiliation":[],"family":"Pani","given":"Amar K."},{"affiliation":[],"family":"Qu","given":"Chunxu"},{"affiliation":[],"family":"Jiao","given":"Yun"},{"affiliation":[],"family":"Smeyne","given":"Richard J."}],"member":"http:\\/\\/id.crossref.org\\/member\\/340","container-title":["PLoS ONE"],"deposited":{"date-parts":[[2014,3,5]],"timestamp":1393977600000},"score":1.0,"subtitle":[],"editor":[{"affiliation":[],"family":"Borlongan","given":"Cesario V."}],"issued":{"date-parts":[[2012,3,21]]},"URL":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.0033693","ISSN":["1932-6203"],"subject":["Agricultural and Biological Sciences(all)","Medicine(all)","Biochemistry, Genetics and Molecular Biology(all)"]}}'


@vcr.use_cassette('test/vcr_cassettes/members.yaml')
def test_members():
    "members - basic test"
    res = cr.members(limit = 2)
    assert dict == res.__class__
    assert dict == res['message'].__class__

@vcr.use_cassette('test/vcr_cassettes/members_query.yaml')
def test_members_query():
    "members - param: query"
    res = cr.members(query = "ecology", limit = 2)
    assert dict == res.__class__
    assert dict == res['message'].__class__

@vcr.use_cassette('test/vcr_cassettes/members_sample.yaml')
def test_members_sample():
    "members - param: sample"
    res = cr.members(sample = 2)
    assert dict == res.__class__
    assert dict == res['message'].__class__


@raises(Exception)
@vcr.use_cassette('test/vcr_cassettes/members_filter.yaml')
def test_members_filter():
    "members - param: filter"
    cr.members(filter = {'has_full_text': True})

@vcr.use_cassette('test/vcr_cassettes/members_field_queries.yaml')
def test_members_field_queries():
    "members - param: kwargs - field queries work as expected"
    res = cr.members(ids = 98, works = True, query_author = 'carl boettiger', limit = 7)
    auths = [ x['author'][0]['family'] for x in res['message']['items'] ]
    assert dict == res.__class__
    assert 5 == len(res['message'])
    assert list == auths.__class__
    assert str == str(auths[0]).__class__

@raises(exceptions.RequestError)
@vcr.use_cassette('test/vcr_cassettes/members_filters_not_allowed_with_dois.yaml')
def test_members_query_filters_not_allowed_with_dois():
    "members - param: kwargs - query filters not allowed on works/memberid/ route"
    cr.members(ids = 98, query_author = 'carl boettiger')
