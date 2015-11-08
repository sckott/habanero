Python Crossref Client
===========================

Low-level client for the Crossref API.

`habanero` is split up into modules for each of the major groups of API methods.

* `Crossref API docs`_

Other Crossref clients:

* R: rcrossref_
* Ruby: serrano_

.. _habanero: https://github.com/sckott/habanero
.. _rcrossref: https://github.com/ropensci/rcrossref
.. _serrano: https://github.com/sckott/serrano
.. _Crossref API Docs: https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

Installation
-------------

::

    pip install habanero


Example Usage
-------------

Import

::

    import habanero

Initialize a client

::

    hb = Habanero()

Or each module individually as needed.

::

    # Query Crossref works
    x = hb.works(query = "ecology")

    # The output is in the `results` object
    x.results

    # A variety of functions help you drill down into result
    x.status()
    x.message_type()
	  x.message_version()
	  x.message()
	  x.total_results()
	  x.items_per_page()
	  x.query()
	  x.items()


Contents
--------

.. toctree::
   :maxdepth: 2

   api
   works
   exceptions
   Changelog

License
-------

MIT


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

