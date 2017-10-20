.. _filters-modules:

=======================
Crossref Search Filters
=======================

crossref module API:

* `filter_names`
* `filter_details`

Example usage:

.. code-block:: python

    from habanero import Crossref
    cr = Crossref()
    cr.filter_names()
    cr.filter_details()


filters API
===========


.. py:module:: habanero

.. automethod:: Crossref.filter_names
.. automethod:: Crossref.filter_details
