Splinter plugin for the py.test runner
======================================

.. image:: https://api.travis-ci.org/pytest-dev/pytest-services.png
    :target: https://travis-ci.org/pytest-dev/pytest-services
.. image:: https://pypip.in/v/pytest-services/badge.png
    :target: https://crate.io/packages/pytest-services/
.. image:: https://coveralls.io/repos/pytest-dev/pytest-services/badge.png?branch=master
    :target: https://coveralls.io/r/pytest-dev/pytest-services
.. image:: https://readthedocs.org/projects/pytest-services/badge/?version=latest
    :target: https://readthedocs.org/projects/pytest-services/?badge=latest
    :alt: Documentation Status


Install pytest-services
-----------------------

::

    pip install pytest-services


.. _pytest:  http://pytest.org
.. _pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _memcached:  http://memcached.org
.. _xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _mysql-server: http://dev.mysql.com/

Features
--------

The plugin provides a set of fixtures and utility functions to start service processes for your tests with
pytest_


Fixtures
--------

* run_services
    Determines whethere services should be run or not. False by default if not in distributed environment
    (without pytest-xdist_). Can be manually set to True by overriding this fixture in your test config or
    just by using `--run-services` command line argument (see below).
* memcached
    Start memcached_ instance.
* memcached_connection
    Memcached connection string.
* mysql
    Start mysql-server_ instance.
* mysql_connection
    MySQL connection string.
* xvfb
    Start xvfb_ instance.
* xvfb_display
    Xvfb display to use for connection.


Command-line options
--------------------

* `--run-services`
    Force services to be run even if tests are executed in a non-distributed way (without pytest-xdist_).
* `--xvfb-display`
    Skip xvfb service to run and use provided display.


Example
-------

test_your_test.py:

.. code-block:: python

    import MySQLdb


    def test_some_mysql_stuff(mysql):
        """Test using mysql server."""
        conn = MySQLdb.connect(user='root')


Contact
-------

If you have questions, bug reports, suggestions, etc. please create an issue on
the `GitHub project page <http://github.com/paylogic/pytest-services>`_.


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/paylogic/pytest-services/blob/master/LICENSE.txt>`_


© 2014 Anatoly Bubenkov, Paylogic International and others.
