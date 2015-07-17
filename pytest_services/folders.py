"""Fixtures for supporting a distributed test run."""
import os
import psutil
import shutil

import pytest


@pytest.fixture(scope='session')
def root_dir():
    """The parent directory of the test base artifact directory."""
    return '/tmp'


@pytest.yield_fixture(scope='session')
def base_dir(request, session_id, root_dir, services_log):
    """The directory where test run artifacts should be stored.

    It is responsibility of fixtures and tests that depend on it to clean up
    after themselves.

    """
    path = os.path.join(root_dir, 'sr-{0}'.format(session_id))
    services_log.debug('creating base dir: {0}'.format(path))
    if not os.path.exists(path):
        os.mkdir(path)

    yield path

    services_log.debug('finalizing base dir: {0}'.format(path))
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(scope='session')
def temp_dir(request, base_dir, services_log):
    """The temporary dir."""
    path = os.path.join(base_dir, 'tmp')

    services_log.debug('creating temp dir: {0}'.format(path))
    if not os.path.exists(path):
        os.mkdir(path)

    return path


@pytest.fixture(scope='session')
def memory_root_dir(root_dir):
    """The parent directory of the test artifact directory in memory."""
    # check for a free space for at least 8 parallel processes
    if os.path.exists('/dev/shm') and psutil.disk_usage('/dev/shm').free > 1024 * 1024 * 64 * 10:
        return '/dev/shm'
    else:
        return root_dir


@pytest.yield_fixture(scope='session')
def memory_base_dir(request, session_id, memory_root_dir, services_log):
    """The directory where memory test run artifacts should be stored.

    It is responsibility of fixtures and tests that depend on it to clean up
    after themselves.

    """
    path = os.path.join(memory_root_dir, 'sr-{0}'.format(session_id))

    services_log.debug('creating memory base dir: {0}'.format(path))
    if not os.path.exists(path):
        os.mkdir(path)

    yield path

    services_log.debug('finalizing memory base dir: {0}'.format(path))
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(scope='session')
def memory_temp_dir(request, memory_base_dir, services_log):
    """The memory temporary dir."""
    path = os.path.join(memory_base_dir, 'tmp')

    services_log.debug('creating memory temp dir: {0}'.format(path))
    if not os.path.exists(path):
        os.mkdir(path)

    return path


@pytest.fixture(scope='session')
def lock_dir(memory_root_dir, services_log):
    """The lock dir."""
    path = os.path.join(memory_root_dir, 'service-locks')
    services_log.debug('ensuring lock dir: {0}'.format(path))
    if not os.path.exists(path):
        try:
            os.mkdir(path, 0o777)
        except OSError:
            # concurrent already created this path
            pass
    try:
        os.chmod(path, 0o777)  # permissions on previous line can be ignored
    except OSError:
        # could happen, but we'll continue as it's just a folder permissions
        pass

    return path


@pytest.fixture(scope='session')
def run_dir(memory_temp_dir, services_log):
    """The run dir (like local /var/run)."""
    path = os.path.join(memory_temp_dir, 'run')
    services_log.debug('creating run dir: {0}'.format(path))
    os.mkdir(path)

    return path
