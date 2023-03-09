======================
CRDB Python frontend
======================

|CRDB|

|docs| |github-ci| |version| |wheel| |supported-versions| |supported-implementations|

This is Python frontend to the CRDB, a database with published data from cosmic ray measurements. The official website of the CRDB with online-viewer and documentation on the database is https://lpsc.in2p3.fr/crdb. The frontend also installs a command-line interface called `crdb` to conveniently download data.

The Python frontend internally uses the REST API of CRDB to download data from the database. A tutorial on using the REST API directly can be found at the  `CRDB tutorial repository <https://github.com/crdb-project/tutorial>`_. The repository also `contains example code on how to make standard plots <https://github.com/crdb-project/tutorial/blob/master/gallery.ipynb>`_ using the `crdb` Python frontend.

.. start-badges

.. |docs| image:: https://readthedocs.org/projects/crdb/badge/?style=flat
    :target: https://crdb.readthedocs.io/
    :alt: Documentation Status

.. |github-ci| image:: https://github.com/crdb-project/crdb/actions/workflows/test.yml/badge.svg
    :alt: Foo
    :target: https://github.com/crdb-project/crdb/actions/workflows/test.yml

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


.. end-badges


Installation
============

::

    pip install crdb


Documentation
=============

The official website of the CRDB has documentation on the database, see https://lpsc.in2p3.fr/crdb. To obtain documentation for the `crdb` Python package, just use `help(crdb)` in the Python interpreter. The command-line frontend comes with built-in help, just run::

    crdb --help

.. |CRDB| image:: https://lpsc.in2p3.fr/crdb/img/crdb_logo.svg
    :target: https://lpsc.in2p3.fr/crdb
