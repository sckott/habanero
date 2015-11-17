habanero
========

.. image:: https://img.shields.io/pypi/v/habanero.svg
   :target: https://pypi.python.org/pypi/habanero

.. image:: https://readthedocs.org/projects/habanero/badge/?version=latest
   :target: http://habanero.rtfd.org/

.. image:: https://travis-ci.org/sckott/habanero.svg
   :target: https://travis-ci.org/sckott/habanero

.. image:: https://coveralls.io/repos/sckott/habanero/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/habanero?branch=master

This is a low level client for working with Crossref's search API. It's been named to be more generic, as other organizations are/will adopt Crossref's search API, making it possible to ineract with all from one client.

`Crossref API docs <https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md](https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md>`__

Other Crossref API clients:

- Ruby: `serrano`, `<https://github.com/sckott/serrano>`__
- R: `rcrossref`, `<https://github.com/ropensci/rcrossref>`__

`habanero` includes methods matching Crossref API routes:

- `/works`
- `/members`
- `/prefixes`
- `/funders`
- `/journals`
- `/types`
- `/licenses`

Other methods

- `registration_agency` - get DOI minting agency
- `content_negotiation` - get citations in a variety of formats
- `citation_count` - get citation count for a DOI

Installation
------------

Stable version

::

  pip install habanero

Dev version

::

    sudo pip install git+git://github.com/sckott/habanero.git#egg=habanero

    # OR

    git clone git@github.com:sckott/habanero.git
    cd habanero
    make install

Usage
-----

Initialize

::

    from habanero import Crossref
    cr = Crossref()

Works route

::

  x = cr.works(query = "ecology")
  x.status()
  x.message()
  x.total_results()
  x.items()

Members route

::

  cr.members(ids = 98, works = True)


Contents
--------

.. toctree::
   :maxdepth: 2

   api
   filters
   counts
   cn
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

