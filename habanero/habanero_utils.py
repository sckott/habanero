import re
import json
import requests
from . import __version__

from .response import Works
from .noworks import NoWorks

# helpers ----------
def converter(x):
    if x.__class__.__name__ == "str":
        return [x]
    else:
        return x


def sub_str(x, n=3):
    if x.__class__.__name__ == "NoneType":
        pass
    else:
        return str(x[:n]) + "***"


def switch_classes(x, path, works):
    if (
        works
        or re.sub("/", "", path) == "works"
        and re.sub("/", "", path) != "licenses"
    ):
        return Works(result=x)
    else:
        return NoWorks(result=x)


def check_kwargs(keys, kwargs):
    for x in range(len(keys)):
        if keys[x] in kwargs.keys():
            mssg = "The %s parameter is not allowed with this method" % keys[x]
            raise Exception(mssg)


def check_json(x):
    ctype = x.headers["Content-Type"]
    matched = re.match("application/json", ctype)
    if matched.__class__.__name__ == "NoneType":
        scode = x.status_code
        if str(x.text) == "Not implemented.":
            scode = 400
        raise RequestError(scode, str(x.text))


def is_json(x):
    try:
        json.loads(x.content)
    except ValueError as e:  # JSONDecodeError is a subclass of ValueError
        return False
    return True


def parse_json_err(x):
    return x.json()["message"][0]["message"]


def make_ua(mailto=None, ua_string=None):
    requa = "python-requests/" + requests.__version__
    habua = "habanero/%s" % __version__
    ua = requa + " " + habua
    if mailto is not None:
        ua = ua + " (mailto:%s)" % mailto
    if ua_string is not None:
        if not isinstance(ua_string, str):
            raise TypeError("ua_string must be a str")
        ua = ua + " " + ua_string
    strg = {"User-Agent": ua, "X-USER-AGENT": ua}
    return strg


def filter_dict(x):
    return dict((k, x[k]) for k, v in x.items() if k.find("query_") == 0)


def rename_query_filters(x):
    newkeys = [re.sub("container_title", "container-title", v) for v in x]
    newkeys = [re.sub("query_", "query.", v) for v in newkeys]
    mapping = dict(zip(x.keys(), newkeys))
    return {mapping[k]: v for k, v in x.items()}


def ifelsestr(x):
    z = str(x) if x is not None else x
    return z
