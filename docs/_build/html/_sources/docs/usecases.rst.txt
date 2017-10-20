.. _usecases:

Usecases
========

Use case 1: Faceted search to get number of works per license type
------------------------------------------------------------------

Load library

.. code-block:: python

    from habanero import Crossref
    cr = Crossref()

First, do a search like

.. code-block:: python

    res = cr.works(facet = "license:*")

Count number of unique licenses

.. code-block:: python

    res['message']['facets']['license']['value-count']

That's a lot of licenses!

Get licenses with > 1000 works

.. code-block:: python

		gt1000 = {k:v for (k,v) in res['message']['facets']['license']['values'].items() if v > 1000}
		len(gt1000)


Ah, that's only 63

Find the license with the most works

.. code-block:: python

		max(gt1000, key=lambda k: gt1000[k])

That's a license "http://www.elsevier.com/tdm/userlicense/1.0/" from Elsevier
