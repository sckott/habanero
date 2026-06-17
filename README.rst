habanero
========

|pypi| |docs| |ghactions| |coverage| |ruff| |uv|

This is a low level client for working with Crossref's search API. It's been named to be more generic, as other organizations are/will adopt Crossref's search API, making it possible to interact with all from one client.

`Crossref API docs <https://api.crossref.org/swagger-ui/index.html>`__

`habanero docs <https://habanero.readthedocs.io/>`__

Other Crossref API clients:

- Ruby: `serrano`, `<https://github.com/sckott/serrano>`__

Crossref's API issue tracker: https://crossref.atlassian.net/jira/software/c/projects/CR/issues/

Note about searching:

You are using the Crossref search API described at https://api.crossref.org/swagger-ui/index.html. When you search with query terms, on Crossref servers they are not searching full text, or even abstracts of articles, but only what is available in the data that is returned to you. That is, they search article titles, authors, etc. For some discussion on this, see https://gitlab.com/crossref/issues/-/issues/101

Rate limits
-----------

See the headers `X-Rate-Limit-Limit` and `X-Rate-Limit-Interval` for current rate limits.

The Polite Pool
---------------

To get in the polite pool it's a good idea now to include a `mailto` email
address. See docs for more information.


Installation
============

Stable version

.. code-block:: console

  # pip
  pip install habanero

  # uv w/ legacy project setup
  uv pip install habanero
  # uv w/ pyproject.toml
  uv add habanero


If you would like to fix bibtex format citations using content negotiation you'll have to install the optional dependency bibtexparser >= 2.0.0b7 (done for you with optional `[bibtex]`)

.. code-block:: console

  pip install habanero[bibtex]


Dev version

.. code-block:: console

    pip install git+https://github.com/sckott/habanero.git#egg=habanero


Or build it yourself locally

.. code-block:: console

    git clone https://github.com/sckott/habanero.git
    cd habanero
    make install


Meta
====

* Please note that this project is released with a `Contributor Code of Conduct <https://github.com/sckott/habanero/blob/main/CODE_OF_CONDUCT.md>`__. By participating in this project you agree to abide by its terms.
* License: MIT; see `LICENSE file <https://github.com/sckott/habanero/blob/main/LICENSE>`__

.. |pypi| image:: https://badge.fury.io/py/habanero.svg
    :target: https://badge.fury.io/py/habanero
    :alt: pypi

.. |docs| image:: https://readthedocs.org/projects/habanero/badge/?version=latest
   :target: http://habanero.rtfd.org/
   :alt: Docs

.. |ghactions| image:: https://github.com/sckott/habanero/actions/workflows/python.yml/badge.svg?branch=main
   :target: https://github.com/sckott/habanero/actions/workflows/python.yml
   :alt: ghactions

.. |coverage| image:: https://codecov.io/gh/sckott/habanero/branch/main/graph/badge.svg?token=6RrgNAuQmR
   :target: https://codecov.io/gh/sckott/habanero
   :alt: coverage

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |uv| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
    :target: https://github.com/astral-sh/uv
    :alt: uv
