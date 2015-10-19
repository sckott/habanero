# -*- coding: utf-8 -*-

# habanero

'''
habanero library
~~~~~~~~~~~~~~~~~~~~~

habanero is a low level client for the Crossref search API.
Example usage:

   >>> from habanero import Habanero
   >>> hb = Habanero()
   >>> hb.works(ids = '10.1371/journal.pone.0033693')
'''

from .habanero import Habanero
