"""Fixtures for memcache."""
import os
import pytest

from .log import dont_capture
from .process import check_output


@pytest.fixture(scope='session')
def memcached_socket(run_dir, run_services):
    """The memcached socket location."""
    if run_services:
        return os.path.join(run_dir, 'memcached.sock')


@pytest.fixture(scope='session')
def memcached(run_services, memcached_socket, watcher_getter):
    """The memcached instance which is ready to be used by the tests."""
    if run_services:
        return watcher_getter(
            name='memcached',
            arguments=['-s', memcached_socket],
            checker=lambda: os.path.exists(memcached_socket))


@pytest.fixture(scope='session')
def memcached_connection(run_services, memcached_socket):
    """The connection string to the local memcached instance."""
    if run_services:
        return 'unix:{0}'.format(memcached_socket)


@pytest.fixture
def do_memcached_clean(run_services):
    """Determine whether memcached should be clean on the start of every test."""
    return run_services


@pytest.fixture
def memcached_clean(request, memcached, memcached_socket, do_memcached_clean):
    """Clean memcached instance."""
    if do_memcached_clean:
        with dont_capture(request):
            check_output([
                "echo 'flush_all' | nc -U {memcached_socket}".format(memcached_socket=memcached_socket)
            ], shell=True)
