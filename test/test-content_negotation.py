import warnings
import re

import pytest
from requests.exceptions import HTTPError

from habanero import cn

bibtex = "@article{Frank_1970,\n\tdoi = {10.1126/science.169.3946.635},\n\turl = {http://dx.doi.org/10.1126/science.169.3946.635},\n\tyear = 1970,\n\tmonth = {aug},\n\tpublisher = {American Association for the Advancement of Science ({AAAS})},\n\tvolume = {169},\n\tnumber = {3946},\n\tpages = {635--641},\n\tauthor = {H. S. Frank},\n\ttitle = {The Structure of Ordinary Water: New data and interpretations are yielding new insights into this fascinating substance},\n\tjournal = {Science}\n}"
cjson = '{"indexed":{"date-parts":[[2015,9,18]],"date-time":"2015-09-18T16:11:22Z","timestamp":1442592682239},"reference-count":0,"publisher":"American Association for the Advancement of Science (AAAS)","issue":"3946","DOI":"10.1126\\/science.169.3946.635","type":"journal-article","created":{"date-parts":[[2006,10,5]],"date-time":"2006-10-05T12:56:56Z","timestamp":1160053016000},"page":"635-641","source":"CrossRef","title":"The Structure of Ordinary Water: New data and interpretations are yielding new insights into this fascinating substance","prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1126","volume":"169","author":[{"affiliation":[],"family":"Frank","given":"H. S."}],"member":"http:\\/\\/id.crossref.org\\/member\\/221","container-title":"Science","deposited":{"date-parts":[[2011,6,27]],"date-time":"2011-06-27T21:18:25Z","timestamp":1309209505000},"score":1.0,"subtitle":[],"issued":{"date-parts":[[1970,8,14]]},"URL":"http:\\/\\/dx.doi.org\\/10.1126\\/science.169.3946.635","ISSN":["0036-8075","1095-9203"]}'


@pytest.mark.vcr
def test_content_negotiation():
    """content negotiation - default - bibtex"""
    res = cn.content_negotiation(ids="10.1126/science.169.3946.635")
    assert str == str(res).__class__


# addresses https://github.com/sckott/habanero/issues/144
# this DOI gives back the month as "sep" instead of "{sep}" as it should
@pytest.mark.vcr
def test_content_negotiation_bad_bibtex():
    """content negotiation - bad bibtex is fixed correctly"""
    month_regex = re.compile(r"\{sep\}")
    res = cn.content_negotiation(ids="10.1139/cjc-2022-0282")
    assert month_regex.search(res) is not None


@pytest.mark.vcr
def test_content_negotiation_with_unicode_doi():
    """content negotiation - unicode"""
    res = cn.content_negotiation(ids="10.1126/science.169.3946.635")
    assert str == str(res).__class__


@pytest.mark.vcr
def test_content_negotiation_citeproc_json():
    """content negotiation - citeproc-json"""
    res = cn.content_negotiation(
        ids="10.1126/science.169.3946.635", format="citeproc-json"
    )
    assert str == str(res).__class__


@pytest.mark.vcr
def test_content_negotiation_alt_url():
    """content negotiation - alternative url"""
    res = cn.content_negotiation(
        ids="10.1126/science.169.3946.635", url="http://doi.org"
    )
    assert str == str(res).__class__


@pytest.mark.vcr
def test_content_negotiation_style():
    """content negotiation - style"""
    res_apa = cn.content_negotiation(
        ids="10.1126/science.169.3946.635", format="text", style="apa"
    )
    res_ieee = cn.content_negotiation(
        ids="10.1126/science.169.3946.635", format="text", style="ieee"
    )
    assert res_apa != res_ieee


# errors
def test_content_negotiation_ids_missing():
    with pytest.raises(TypeError):
        cn.content_negotiation()


def test_content_negotiation_ids_none():
    with pytest.raises(TypeError):
        cn.content_negotiation(ids=None)


@pytest.mark.vcr
def test_content_negotiation_raises_an_http_error_with_bad_requests():
    with pytest.raises(HTTPError):
        cn.content_negotiation(ids="10.1126/foo")


# warnings
@pytest.mark.vcr
def test_content_negotiation_throws_warnings():
    with pytest.warns(UserWarning):
        cn.content_negotiation(ids=["10.1126/science.169.3946.635", "foo"])


@pytest.mark.vcr
def test_content_negotiation_throws_warnings_can_be_suppressed():
    warnings.filterwarnings("ignore")
    x = cn.content_negotiation(ids=["10.1126/science.169.3946.635", "foo"])
    assert isinstance(x, list)
    warnings.filterwarnings("default")
