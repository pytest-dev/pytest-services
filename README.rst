Services plugin for pytest testing framework
============================================

.. image:: https://api.travis-ci.org/pytest-dev/pytest-services.png
    :target: https://travis-ci.org/pytest-dev/pytest-services
.. image:: https://pypip.in/v/pytest-services/badge.png
    :target: https://crate.io/packages/pytest-services/
.. image:: https://coveralls.io/repos/pytest-dev/pytest-services/badge.svg?branch=master
    :target: https://coveralls.io/r/pytest-dev/pytest-services?branch=master
.. image:: https://readthedocs.org/projects/pytest-services/badge/?version=latest
    :target: https://readthedocs.org/projects/pytest-services/?badge=latest
    :alt: Documentation Status


Install pytest-services
-----------------------

::

    pip install pytest-services


.. _pytest:  http://pytest.org
.. _pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _pytest-splinter: https://pypi.python.org/pypi/pytest-splinter
.. _pytest-bdd: https://pypi.python.org/pypi/pytest-bdd
.. _pytest-django: https://pypi.python.org/pypi/pytest-django
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

Infrastructure fixtures
***********************

* slave_id
    Id of the slave if tests are run using pytest-xdist_. It is set to `local` if tests are not run using
    pytest-xdist_ (with `--dist` command line option set to `load`).
* session_id
    Test session id. Globally unique, and of course also guaranteed to be different for potentially multiple test
    sessions running on same test node via pytest-xdist_.
* watcher_getter
    Function to instantiate test service watcher (popen object). Includes automatic finalization (exiting) of the
    service process, and testing the service before returning the watcher from the function.
    Example of usage for memcached service:

.. code-block:: python

    @pytest.fixture(scope='session')
    def memcached(request, run_services, memcached_socket, watcher_getter):
        """The memcached instance which is ready to be used by the tests."""
        if run_services:
            return watcher_getter(
                name='memcached',
                arguments=['-s', memcached_socket],
                checker=lambda: os.path.exists(memcached_socket))

* services_log
    Logger used for debug logging when managing test services.
* root_dir
    Parent directory for test service artifacts (disk based). Set to `/tmp` by default.
* base_dir
    Base directory for test service artifacts (disk based), unique subdirectory of `root_dir`.
    Automatically removed recursively at the end of the test session.
* temp_dir
    `Temporary` directory (disk based), subfolder of the `base_dir`.
    Used for strictly temporary artifacts (for example - folder where files are uploaded from the user input).
* memory_root_dir
    Parent directory for test service artifacts (memory based). Main idea of having memory base directory is to
    store performance-critical files there. For example - mysql service will use it to store database file, it speeds up
    mysql server a lot, especially database management operations.
    Set to `/var/shm` by default, with a fallback to 'root_dir`. Note that if apparmor is running on your system, most
    likely it will prevent your test service to use it (for example - mysql has it's apparmor profile). You you'll need
    to disable such profile in apparmor configuration.
    Example of disabling apparmor for mysqld:

.. code-block:: sh

    sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
    sudo /etc/init.d/apparmor restart

* memory_base_dir
    Base directory for test service artifacts (memory based), unique subdirectory of `memory_root_dir`.
    Automatically removed recursively at the end of the test session.
* memory_temp_dir
    `Temporary` directory (memory based), subfolder of the `base_dir`.
* lock_dir
    Lock files directory for storing locks created for resource assignment (ports, display, etc). Subfolder of
    `memory_root_dir`.
* run_dir
    Process id and socket files directory (like system-wide `/var/run` but local for test session). Subfolder of
    `memory_root_dir`.
* port_getter
    Function to get unallocated port.
    Automatically ensures locking and un-locking of it on application level via flock.
* display_getter
    Function to get unallocated display.
    Automatically ensures locking and un-locking of it on application level via flock.


Service fixtures
****************

* memcached
    Start memcached_ instance.
* memcached_socket
    Memcached unix socket file name to be used for connection.
* memcached_connection
    Memcached connection string.
* do_memcached_clean
    Determine if memcached should be cleared before every test run. Equals to `run_services` fixture by default.
* mysql
    Start mysql-server_ instance.
* mysql_database_name
    MySQL database name to be created after initialization of the mysql service `system` database.
* mysql_database_getter
    Function with single parameter - database name. To create additional database(s) for tests.
    Used in `mysql_database` fixture which is used by `mysql` one.
* mysql_connection
    MySQL connection string.
* xvfb
    Start xvfb_ instance.
* xvfb_display
    Xvfb display to use for connection.
* xvfb_resolution
    Xvfb display resolution to use. Tuple in form `(1366, 768, 8)`.

Utility functions
*****************

Django settings
^^^^^^^^^^^^^^^

In some cases, there's a need of switching django settings during test run, because several django projects are tested
whithin the single test suite.
`pytest_services.django_settings` simplifies switching of django settings to a single function call:

* setup_django_settings
    Override the enviroment variable and call the _setup method of the settings object to reload them.

Example of usage:

conftest.py:

.. code-block:: python

    from pytest_services import django_settings

    django_settings.clean_django_settings()
    django_settings.setup_django_settings('your.project.settings')

Note that the nice project pytest-django_ doesn't help with the situation, as it's single django project oriented, as
well as standard django testing technique. Single project approach works fine, as long as there are no fixtures to share
between them, but when there are fixtures to share, then you can get benefit of joining several django projects tests
into a single test run, because all session-scoped fixtures will be instantiated only once for all projects tests.
The benefit is only visible if you have big enough test suite and your fixtures are heavy enough.


Command-line options
--------------------

* `--run-services`
    Force services to be run even if tests are executed in a non-distributed way (without pytest-xdist_).
* `--xvfb-display`
    Skip xvfb service to run and use provided display. Useful when you need to run all services except the xvfb_
    to debug your browser tests, if, for example you use pytest-splinter_ with or without pytest-bdd_.

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
the `GitHub project page <https://github.com/pytest-dev/pytest-services>`_.


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/pytest-dev/pytest-services/blob/master/LICENSE.txt>`_


© 2014 Anatoly Bubenkov, Paylogic International and others.
