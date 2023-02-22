========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/crdb/badge/?style=flat
    :target: https://crdb.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/crdb-project/crdb/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/crdb-project/crdb/actions

.. |codecov| image:: https://codecov.io/gh/crdb-project/crdb/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/crdb-project/crdb

.. |version| image:: https://img.shields.io/pypi/v/crdb.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/crdb

.. |wheel| image:: https://img.shields.io/pypi/wheel/crdb.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/crdb

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/crdb.svg
    :alt: Supported versions
    :target: https://pypi.org/project/crdb

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/crdb.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/crdb

.. |commits-since| image:: https://img.shields.io/github/commits-since/crdb-project/crdb/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/crdb-project/crdb/compare/v0.0.0...main



.. end-badges

CRDB Python frontend

* Free software: MIT license

Installation
============

::

    pip install crdb

You can also install the in-development version with::

    pip install https://github.com/crdb-project/crdb/archive/main.zip


Documentation
=============


https://crdb.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
