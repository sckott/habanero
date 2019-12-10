"""Tests for user agent strings via the ua_string setting"""
import os
import vcr
import yaml
from nose.tools import *
from habanero import Crossref

cr_with_ua = Crossref(ua_string = "foo bar")
cr_without_ua = Crossref()
cr_with_bad_ua = Crossref(ua_string = 5)

vcr_path = 'test/vcr_cassettes/setting_ua_string.yaml'
@vcr.use_cassette(vcr_path)
def test_ua_string():
    "settings (ua_string) - with ua string"
    res = cr_with_ua.works(ids = '10.1371/journal.pone.0033693')
    x = open(vcr_path, "r").read()
    xy = yaml.load(x)
    heads = xy['interactions'][0]['request']['headers']
    
    assert 'foo bar' in heads['User-Agent'][0]
    assert 'foo bar' in heads['X-USER-AGENT'][0]

vcr_noua_path = 'test/vcr_cassettes/setting_no_ua_string.yaml'
@vcr.use_cassette(vcr_noua_path)
def test_no_ua_string():
    "settings (ua_string) - without ua string"
    res = cr_without_ua.works(ids = '10.1371/journal.pone.0033693')
    x = open(vcr_noua_path, "r").read()
    xy = yaml.load(x)
    heads = xy['interactions'][0]['request']['headers']
    
    assert 'foo bar' not in heads['User-Agent'][0]
    assert 'foo bar' not in heads['X-USER-AGENT'][0]

@raises(TypeError)
def test_ua_string_errors():
    "settings (ua_string) - fails well"
    cr_with_bad_ua.works(ids = '10.1371/journal.pone.0033693')

# NOTE: the two test blocks above using cassettes is super hacky
# - i can't find a way to inspect the request headers that get sent
# - so just inspecting the request headers recorded in the cassette
# - i.e., re-running to record cassettes from scratch will fail 
# - on the first run, but then suceed after that
