habanero
========

|pypi| |docs| |travis| |coverage|

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
============

Stable version

.. code-block:: console

	pip install habanero

Dev version

.. code-block:: console

		sudo pip install git+git://github.com/sckott/habanero.git#egg=habanero

		# OR

		git clone git@github.com:sckott/habanero.git
		cd habanero
		make install

Usage
=====

Initialize

.. code-block:: python

		from habanero import Crossref
		cr = Crossref()

Works route

.. code-block:: python

	x = cr.works(query = "ecology")
	x.status()
	x.message()
	x.total_results()
	x.items()

Members route

.. code-block:: python

	cr.members(ids = 98, works = True)

Meta
====

* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.
* License: MIT; see `LICENSE file <LICENSE>`__

.. |pypi| image:: https://img.shields.io/pypi/v/habanero.svg
   :target: https://pypi.python.org/pypi/habanero

.. |docs| image:: https://readthedocs.org/projects/habanero/badge/?version=latest
   :target: http://habanero.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/habanero.svg
	 :target: https://travis-ci.org/sckott/habanero

.. |coverage| image:: https://coveralls.io/repos/sckott/habanero/badge.svg?branch=master&service=github
	 :target: https://coveralls.io/github/sckott/habanero?branch=master

