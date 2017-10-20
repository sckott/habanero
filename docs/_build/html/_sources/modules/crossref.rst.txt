.. _crossref-modules:

===============
crossref module
===============

crossref module API:

* `works`
* `members`
* `prefixes`
* `funders`
* `journals`
* `types`
* `licenses`
* `registration_agency`
* `random_dois`

Example usage:

.. code-block:: python

    from habanero import Crossref
    cr = Crossref()
    cr.works()
    cr.works(ids = '10.1371/journal.pone.0033693')
    cr.works(query = "ecology")


crossref API
============


.. py:module:: habanero

.. automethod:: Crossref.works
.. automethod:: Crossref.members
.. automethod:: Crossref.prefixes
.. automethod:: Crossref.funders
.. automethod:: Crossref.journals
.. automethod:: Crossref.types
.. automethod:: Crossref.licenses
.. automethod:: Crossref.registration_agency
.. automethod:: Crossref.random_dois
