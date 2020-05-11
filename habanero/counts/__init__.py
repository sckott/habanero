# -*- coding: utf-8 -*-

# counts

"""
citation counts
~~~~~~~~~~~~~~~

Get citation count data

Usage::

   from habanero import counts
   cr = Crossref()
   counts.citation_count(doi = "10.1371/journal.pone.0042793"
"""

from .counts import citation_count
