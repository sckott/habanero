import requests
import json
import re

from ..habanero_utils import check_json


def csl_styles(**kwargs):
    """
    Get list of styles from https://github.com/citation-style-language/styles

    :param kwargs: any additional arguments will be passed on to `requests.get`

    :return: list, of CSL styles

    Usage::

        from habanero import cn
        cn.csl_styles()
    """
    base = "https://api.github.com/repos/citation-style-language/styles"
    tt = requests.get(base + "/commits?per_page=1", **kwargs)
    tt.raise_for_status()
    check_json(tt)
    commres = tt.json()
    sha = commres[0]["sha"]
    sty = requests.get(base + "/git/trees/" + sha, **kwargs)
    sty.raise_for_status()
    check_json(sty)
    res = sty.json()
    files = [z["path"] for z in res["tree"]]
    matches = [re.search(".csl", g) for g in files]
    csls = [x.string for x in filter(None, matches)]
    return [re.sub(".csl", "", x) for x in csls]
