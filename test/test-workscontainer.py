import pytest
import vcr
from habanero import Crossref, WorksContainer

cr = Crossref()


@pytest.mark.vcr
def test_workscontainer_with_one_id():
    "WorksContainer: one DOI"
    res = cr.works(ids="10.1371/journal.pone.0033693")
    x = WorksContainer(res)
    assert isinstance(x, WorksContainer)
    assert isinstance(x.works, list)
    assert len(x.works) == 1
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith("_") and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))


@pytest.mark.vcr
def test_workscontainer_with_two_ids():
    "WorksContainer: two DOIs"
    res = cr.works(
        ids=["10.1136/jclinpath-2020-206745", "10.1136/esmoopen-2020-000776"]
    )
    x = WorksContainer(res)
    assert isinstance(x, WorksContainer)
    assert isinstance(x.works, list)
    assert len(x.works) == 2
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith("_") and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))


@pytest.mark.vcr
def test_workscontainer_with_many():
    "WorksContainer: many DOIs"
    res = cr.members(ids=98, works=True, limit=5)
    x = WorksContainer(res)
    assert isinstance(x, WorksContainer)
    assert isinstance(x.works, list)
    assert len(x.works) == 5
    for w in dir(x):
        # print(f"{w} {not w.startswith('__')}")
        if not w.startswith("_") and w != "works_handler":
            assert isinstance(getattr(x, w), list)
            # print(isinstance(getattr(x, w), list))


@pytest.mark.vcr
def test_workscontainer_failure_behavior():
    "WorksContainer: failure behavior"
    # bad types
    with pytest.raises(TypeError):
        WorksContainer(5)
        WorksContainer("nope")
        WorksContainer(True)
        WorksContainer(False)
    # length zero
    with pytest.raises(ValueError):
        WorksContainer({})
        WorksContainer([])
    # wrong message-type's
    res = cr.prefixes(ids="10.1016")
    with pytest.raises(TypeError):
        WorksContainer(res)

    res = cr.members(ids=98)
    with pytest.raises(TypeError):
        WorksContainer(res)
