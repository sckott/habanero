"""Tests for content_negotation"""
import os
from habanero import cn

bibtex = '@article{Frank_1970,\n\tdoi = {10.1126/science.169.3946.635},\n\turl = {http://dx.doi.org/10.1126/science.169.3946.635},\n\tyear = 1970,\n\tmonth = {aug},\n\tpublisher = {American Association for the Advancement of Science ({AAAS})},\n\tvolume = {169},\n\tnumber = {3946},\n\tpages = {635--641},\n\tauthor = {H. S. Frank},\n\ttitle = {The Structure of Ordinary Water: New data and interpretations are yielding new insights into this fascinating substance},\n\tjournal = {Science}\n}'
cjson = '{"indexed":{"date-parts":[[2015,9,18]],"date-time":"2015-09-18T16:11:22Z","timestamp":1442592682239},"reference-count":0,"publisher":"American Association for the Advancement of Science (AAAS)","issue":"3946","DOI":"10.1126\\/science.169.3946.635","type":"journal-article","created":{"date-parts":[[2006,10,5]],"date-time":"2006-10-05T12:56:56Z","timestamp":1160053016000},"page":"635-641","source":"CrossRef","title":"The Structure of Ordinary Water: New data and interpretations are yielding new insights into this fascinating substance","prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1126","volume":"169","author":[{"affiliation":[],"family":"Frank","given":"H. S."}],"member":"http:\\/\\/id.crossref.org\\/member\\/221","container-title":"Science","deposited":{"date-parts":[[2011,6,27]],"date-time":"2011-06-27T21:18:25Z","timestamp":1309209505000},"score":1.0,"subtitle":[],"issued":{"date-parts":[[1970,8,14]]},"URL":"http:\\/\\/dx.doi.org\\/10.1126\\/science.169.3946.635","ISSN":["0036-8075","1095-9203"]}'

def test_content_negotiation():
    "content negotiation - deafult - bibtex"
    res = cn.content_negotiation(ids = '10.1126/science.169.3946.635')
    assert str == str(res).__class__

def test_content_negotiation_citeproc_json():
    "content negotiation - citeproc-json"
    res = cn.content_negotiation(ids = '10.1126/science.169.3946.635', format = "citeproc-json")
    assert str == str(res).__class__
