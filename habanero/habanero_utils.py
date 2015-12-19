import re

from .response import Works
from .noworks import NoWorks

# helpers ----------
def converter(x):
  if(x.__class__.__name__ == 'str'):
      return [x]
  else:
      return x

def sub_str(x, n = 3):
  if(x.__class__.__name__ == 'NoneType'):
    pass
  else:
    return str(x[:n]) + '***'

def switch_classes(x, path, works):
  if works or re.sub("/", "", path) == "works" and re.sub("/", "", path) != "licenses":
  	return Works(result = x)
  else:
  	return NoWorks(result = x)

def check_kwargs(keys, kwargs):
  for x in range(len(keys)):
    if keys[x] in kwargs.keys():
      mssg = "The %s parameter is not allowed with this method" % keys[x]
      raise Exception(mssg)

def check_json(x):
  ctype = x.headers['Content-Type']
  matched = re.match("application/json", ctype)
  if matched.__class__.__name__ == 'NoneType':
    scode = x.status_code
    if str(x.text) == "Not implemented.":
      scode = 400
    raise RequestError(scode, str(x.text))
