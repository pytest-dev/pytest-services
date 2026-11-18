Services plugin for pytest testing framework
============================================

.. image:: https://img.shields.io/pypi/v/pytest-services.svg
   :target: https://pypi.org/project/pytest-services/
.. image:: https://img.shields.io/pypi/pyversions/pytest-services.svg
   :target: https://pypi.org/project/pytest-services/
.. image:: https://github.com/pytest-dev/pytest-services/actions/workflows/test.yml/badge.svg
   :target: https://github.com/pytest-dev/pytest-services/actions/workflows/test.yml
.. image:: https://readthedocs.org/projects/pytest-services/badge/?version=latest
   :target: https://readthedocs.org/projects/pytest-services/?badge=latest
   :alt: Documentation Status

Install pytest-services
-----------------------

::

    pip install pytest-services

To use the ``memcached_client`` fixture, install the ``memcached`` extra, which pulls in ``pylibmc``::

    pip install 'pytest-services[memcached]'


.. _pytest: https://pytest.org
.. _pytest-xdist: https://pypi.org/project/pytest-xdist/
.. _pytest-splinter: https://pypi.org/project/pytest-splinter/
.. _pytest-bdd: https://pypi.org/project/pytest-bdd/
.. _pytest-django: https://pypi.org/project/pytest-django/
.. _memcached: https://memcached.org
.. _xvfb: https://en.wikipedia.org/wiki/Xvfb
.. _mysql-server: https://dev.mysql.com/
.. _mysqlclient: https://pypi.org/project/mysqlclient/

Features
--------

The plugin provides a set of fixtures and utility functions to start service processes for your tests with
pytest_.

Requirements
------------

The service fixtures start real processes, so the corresponding programs must be installed and available on ``PATH``:

* memcached_ for the ``memcached`` fixture.
* mysql-server_ (``mysqld``, ``mysql``, ``my_print_defaults`` and ``mysql_tzinfo_to_sql``) for the ``mysql`` fixture.
* xvfb_ (``Xvfb``) for the ``xvfb`` fixture.

The services rely on POSIX facilities (unix sockets, ``/tmp``, ``/dev/shm``), so they are meant to be run on
Linux or other POSIX systems.


Fixtures
--------

* ``run_services``
    Determines whether services should be run or not. ``False`` by default if not in a distributed environment
    (without pytest-xdist_). Can be manually set to ``True`` by overriding this fixture in your test config or
    just by using the ``--run-services`` command line argument (see below).

Infrastructure fixtures
***********************

* ``worker_id``
    Id of the worker if tests are run using pytest-xdist_. It is set to ``local`` if tests are not run using
    pytest-xdist_.
    Has a deprecated alias ``slave_id`` which will be removed in a future version.
* ``session_id``
    Test session id. Globally unique, and of course also guaranteed to be different for potentially multiple test
    sessions running on same test node via pytest-xdist_.
* ``watcher_getter``
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
                checker=lambda: os.path.exists(memcached_socket),
                # Needed for the correct execution order of finalizers
                request=request,
            )

* ``services_log``
    Logger used for debug logging when managing test services.
* ``root_dir``
    Parent directory for test service artifacts (disk based). Set to ``/tmp`` by default.
* ``base_dir``
    Base directory for test service artifacts (disk based), unique subdirectory of ``root_dir``.
    Automatically removed recursively at the end of the test session.
* ``temp_dir``
    Temporary directory (disk based), subfolder of ``base_dir``.
    Used for strictly temporary artifacts (for example - folder where files are uploaded from the user input).
* ``memory_root_dir``
    Parent directory for test service artifacts (memory based). Main idea of having memory base directory is to
    store performance-critical files there. For example - mysql service will use it to store database file, it speeds up
    mysql server a lot, especially database management operations.
    Set to ``/dev/shm`` by default, if it exists and has enough free space (about 640 MB), with a fallback to
    ``root_dir``. Note that if AppArmor is running on your system, most likely it will prevent your test service from
    using it (for example - mysql has its own AppArmor profile). You'll need to disable such profile in the AppArmor
    configuration.
    Example of disabling AppArmor for mysqld:

.. code-block:: sh

    sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
    sudo /etc/init.d/apparmor restart

* ``memory_base_dir``
    Base directory for test service artifacts (memory based), unique subdirectory of ``memory_root_dir``.
    Automatically removed recursively at the end of the test session.
* ``memory_temp_dir``
    Temporary directory (memory based), subfolder of ``memory_base_dir``.
* ``lock_dir``
    Lock files directory for storing locks created for resource assignment (ports, display, etc). Subfolder of
    ``memory_root_dir``.
* ``run_dir``
    Process id and socket files directory (like system-wide ``/var/run`` but local for test session). Subfolder of
    ``memory_temp_dir``.
* ``port_getter``
    Function to get an unallocated port.
    Automatically ensures locking and un-locking of it on application level via lock files.
* ``display_getter``
    Function to get an unallocated display.
    Automatically ensures locking and un-locking of it on application level via lock files.
* ``lock_resource_timeout``
    Maximum number of seconds to wait for the lock on a resource (port, display) used by ``port_getter`` and
    ``display_getter``. Defaults to ``20``.

Service fixtures
****************

* ``memcached``
    Start memcached_ instance.
* ``memcached_socket``
    Memcached unix socket file name to be used for connection.
* ``memcached_connection``
    Memcached connection string.
* ``memcached_client``
    A ``pylibmc.Client`` instance bound to the service.
    Requires ``pylibmc`` installed (``pip install 'pytest-services[memcached]'``); tests using it are skipped otherwise.
* ``memcached_clean``
    Flushes all memcached data before the test if ``do_memcached_clean`` is ``True``.
    Requires ``pylibmc``, through ``memcached_client``.
* ``do_memcached_clean``
    Determine if memcached should be cleared before every test run by ``memcached_clean``. Equals to
    ``run_services`` fixture by default.
* ``mysql``
    Start mysql-server_ instance and create the test database.
* ``mysql_database_name``
    MySQL database name to be created after initialization of the mysql service ``system`` database.
    Defaults to ``pytest_services_test``.
* ``mysql_database_getter``
    Function with single parameter - database name. To create additional database(s) for tests.
    Used in ``mysql_database`` fixture which is used by ``mysql`` one.
* ``mysql_database``
    Creates the ``mysql_database_name`` database.
* ``mysql_connection``
    MySQL connection string.
* ``mysql_socket``
    MySQL unix socket file name to be used for connection. The server runs with ``--skip-networking``, so connections
    must go through this socket.
* ``mysql_pid``
    MySQL server pid file.
* ``mysql_watcher``
    The ``mysqld`` process watcher.
* ``mysql_data_dir``
    MySQL data directory, created inside ``memory_temp_dir``.
* ``mysql_defaults_file``
    MySQL defaults file (``--defaults-file``) used by the server.
* ``mysql_base_dir``
    MySQL installation base directory, detected from the location of ``my_print_defaults``.
* ``mysql_system_database``
    Initializes the MySQL ``system`` database.
* ``xvfb``
    Start xvfb_ instance.
* ``xvfb_display``
    Xvfb display to use for connection.
* ``xvfb_resolution``
    Xvfb display resolution to use. Tuple in form ``(1366, 768, 8)``.

Utility functions
*****************

Django settings
^^^^^^^^^^^^^^^

.. warning::

    ``pytest_services.django_settings`` is not compatible with current Python and Django versions: it imports
    ``imp`` (removed in Python 3.12) and ``django.core.urlresolvers`` (removed in Django 2.0).

In some cases, there's a need of switching django settings during test run, because several django projects are tested
within the single test suite.
``pytest_services.django_settings`` simplifies switching of django settings to a single function call:

* ``setup_django_settings``
    Override the environment variable and call the ``_setup`` method of the settings object to reload them.
* ``clean_django_settings``
    Remove the ``DJANGO_SETTINGS_MODULE`` environment variable and reset the settings object. The environment
    variable must be set when calling it.

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

* ``--run-services``
    Force services to be run even if tests are executed in a non-distributed way (without pytest-xdist_).
* ``--xvfb-display``
    Skip xvfb service to run and use provided display. Useful when you need to run all services except the xvfb_
    to debug your browser tests, if, for example you use pytest-splinter_ with or without pytest-bdd_.

Example
-------

test_your_test.py (requires mysqlclient_):

.. code-block:: python

    import MySQLdb


    def test_some_mysql_stuff(mysql, mysql_socket, mysql_database_name):
        """Test using mysql server."""
        conn = MySQLdb.connect(user='root', unix_socket=mysql_socket, database=mysql_database_name)


Contact
-------

If you have questions, bug reports, suggestions, etc. please create an issue on
the `GitHub project page <https://github.com/pytest-dev/pytest-services>`_.


License
-------

This software is licensed under the `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/pytest-dev/pytest-services/blob/main/LICENSE.txt>`_


© 2014 Anatoly Bubenkov, Paylogic International and others.
