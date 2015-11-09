# -*- coding: utf-8 -*-

# habanero

'''
habanero library
~~~~~~~~~~~~~~~~~~~~~

habanero is a low level client for the Crossref search API.
Example usage:

   >>> from habanero import Habanero
   >>> hb = Habanero()
   >>>
   >>> # setup a different base URL
   >>> Habanero(base_url = "http://some.other.url")
   >>>
   >>> # setup an api key
   >>> Habanero(api_key = "123456")
   >>>
   >>> # Make request against works route
   >>> hb.works(ids = '10.1371/journal.pone.0033693')
   >>>
   >>> # curl options
   >>> ## For example, set a timeout
   >>> hb.works(query = "ecology", timeout=0.1)
   >>>
   >>> ## advanced logging
   >>> ### setup first
   >>> import requests
   >>> import logging
   >>> import httplib as http_client
   >>> http_client.HTTPConnection.debuglevel = 1
   >>> logging.basicConfig()
   >>> logging.getLogger().setLevel(logging.DEBUG)
   >>> requests_log = logging.getLogger("requests.packages.urllib3")
   >>> requests_log.setLevel(logging.DEBUG)
   >>> requests_log.propagate = True
   >>> ### then make request
   >>> hb.works(query = "ecology")
'''

from .habanero import Habanero
from .filters import filters
from .exceptions import *
