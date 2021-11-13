.. _contributing:

Contributing
============

.. important::

    Double check you are reading the most recent version of this document at
    http://habanero.readthedocs.io/en/latest/index.html

Bug reports
-----------

Please report bug reports on our `issue tracker`_.

.. _issue tracker: https://github.com/sckott/habanero/issues


Feature requests
----------------

Please put feature requests on our `issue tracker`_.


Pull requests
-------------

When you submit a PR, you'll see a template that pops up - it's reproduced
here.


- Provide a general summary of your changes in the Title
- Describe your changes in detail
- If the PR closes an issue, make sure to include, e.g., `fix #4` or similar,
  or if it just relates to an issue, make sure to mention it like `#4`
- If introducing a new feature or changing behavior of existing
  methods/functions, include an example if possible to do in brief form
- Did you remember to include tests? Unless you're changing docs/grammar,
  please include new tests for your change


Writing tests
-------------

We're using `pytest` for testing. See the `pytest docs`_ for
help on contributing to or writing tests.

The Makefile has a task for testing with vcr (using fixtures: `make test`) and without (`make test_no_vcr`)

.. _pytest docs: https://docs.pytest.org/en/stable/
