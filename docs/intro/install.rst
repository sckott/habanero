.. _intro-install:

==================
Installation guide
==================

Installing habanero
===================

Stable from pypi

.. code-block:: console

    # pip
    pip install habanero

    # uv w/ legacy project setup
    uv pip install habanero
    # uv w/ pyproject.toml
    uv add habanero


If you need to fix bibtex format citations using content negotiation use

.. code-block:: console

  pip install habanero[bibtex]


Development version

.. code-block:: console

    pip install git+https://github.com/sckott/habanero.git#egg=habanero
