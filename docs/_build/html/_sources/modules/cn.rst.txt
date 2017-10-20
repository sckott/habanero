.. cn-modules:

=========
cn module
=========

cn module API:

* `content_negotiation`

Example usage:

.. code-block:: python

    from habanero import cn
    cn.content_negotiation(ids = '10.1126/science.169.3946.635')
    cn.content_negotiation(ids = '10.1126/science.169.3946.635', format = "citeproc-json")
    cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "rdf-xml")
    cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "crossref-xml")
    cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text")
    cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "bibentry")



cn API
======


.. py:module:: habanero

.. automethod:: cn.content_negotiation
