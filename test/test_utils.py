from habanero.habanero_utils import filter_dict


def test_filter_dict_drops_none_query_values():
    """filter_dict - drops None query values

    See https://github.com/sckott/habanero/issues/232
    """
    out = filter_dict({"query_1": 1, "query_2": None, "query_3": 3})
    assert len(out) == 2
    assert out["query_1"] == 1
    assert out["query_3"] == 3
