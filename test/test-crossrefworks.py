import pytest
import vcr
from habanero import Crossref, CrossrefWorks

cr = Crossref()

@pytest.mark.vcr
def test_crossrefworks_with_one_id():
    "CrossrefWorks: one DOI"
    res = cr.works(ids="10.1371/journal.pone.0033693")
    x = CrossrefWorks(res)
    assert isinstance(x, CrossrefWorks)
    assert isinstance(x.works, list)
    assert len(x.works) == 1
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith('_') and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))

@pytest.mark.vcr
def test_crossrefworks_with_two_ids():
    "CrossrefWorks: two DOIs"
    res = cr.works(ids=['10.1136/jclinpath-2020-206745', '10.1136/esmoopen-2020-000776'])
    x = CrossrefWorks(res)
    assert isinstance(x, CrossrefWorks)
    assert isinstance(x.works, list)
    assert len(x.works) == 2
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith('_') and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))

@pytest.mark.vcr
def test_crossrefworks_with_many():
    "CrossrefWorks: many DOIs"
    res = cr.members(ids = 98, works = True, limit = 5)
    x = CrossrefWorks(res)
    assert isinstance(x, CrossrefWorks)
    assert isinstance(x.works, list)
    assert len(x.works) == 5
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith('_') and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))
