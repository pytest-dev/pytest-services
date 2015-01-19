"""Fixtures for mysql."""
import os
import shutil

from distutils.spawn import find_executable
import pytest

from .process import (
    CalledProcessWithOutputError,
    check_output,
)


@pytest.fixture(scope='session')
def mysql_system_database(run_services, mysql_data_dir, memory_temp_dir, lock_dir, log):
    """Install database to given path."""
    if run_services:
        mysql_install_db = find_executable('mysql_install_db')
        assert mysql_install_db, 'You have to install mysql_install_db script.'

        my_print_defaults = find_executable('my_print_defaults')
        assert my_print_defaults, 'You have to install my_print_defaults script.'

        mysql_basedir = os.path.dirname(os.path.dirname(my_print_defaults))

        defaults_path = os.path.join(mysql_data_dir, 'defaults.cnf')

        with open(defaults_path, 'w+') as fd:
            fd.write("""
    [mysqld]
    user = {user}
    tmpdir = {tmpdir}
    """.format(user=os.environ['USER'], tmpdir=memory_temp_dir))

        try:
            log.debug('Starting mysql_install_db.')
            check_output([
                mysql_install_db,
                '--defaults-file={0}'.format(defaults_path),
                '--datadir={0}'.format(mysql_data_dir),
                '--basedir={0}'.format(mysql_basedir),
                '--user={0}'.format(os.environ['USER'])],
            )
        except CalledProcessWithOutputError as e:
            log.error(
                '{e.cmd} failed with output:\n{e.output}\nand erorr:\n{e.err}. '
                'Please ensure you disabled apparmor for /run/shm/** or for whole mysql'.format(e=e))
            raise
        finally:
            log.debug('mysql_install_db was executed.')


@pytest.fixture(scope='session')
def mysql_data_dir(
        request, memory_base_dir, memory_temp_dir, lock_dir, session_id, log, run_services):
    """The root directory for the mysql instance.

    `mysql_install_db` is run in that directory.

    """
    if run_services:
        path = os.path.join(memory_base_dir, 'mysql')
        log.debug('Making mysql base dir in {path}'.format(path=path))

        def finalizer():
            shutil.rmtree(path, ignore_errors=True)

        finalizer()
        request.addfinalizer(finalizer)
        os.mkdir(path)
        return path


@pytest.fixture(scope='session')
def mysql_socket(run_dir):
    """The mysqld socket location."""
    return os.path.join(run_dir, 'mysql.sock')


@pytest.fixture(scope='session')
def mysql_pid(run_dir):
    """The pid file of the mysqld."""
    return os.path.join(run_dir, 'mysql.pid')


@pytest.fixture(scope='session')
def mysql_connection(run_services, mysql_socket):
    """The connection string to the local mysql instance."""
    if run_services:
        return 'mysql://root@localhost/?unix_socket={0}&charset=utf8'.format(mysql_socket)


@pytest.fixture(scope='session')
def mysql_watcher(
        request, run_services, watcher_getter, mysql_system_database, mysql_pid, mysql_socket, mysql_data_dir):
    """The mysqld process watcher."""
    if run_services:
        return watcher_getter('mysqld', [
            '--datadir={mysql_data_dir}'.format(mysql_data_dir=mysql_data_dir),
            '--pid-file={mysql_pid}'.format(mysql_pid=mysql_pid),
            '--socket={mysql_socket}'.format(mysql_socket=mysql_socket),
            '--skip-networking',
            '--general-log=true',
            '--log-error={mysql_data_dir}/error.log'.format(mysql_data_dir=mysql_data_dir)
        ], checker=lambda: os.path.exists(mysql_socket))


@pytest.fixture(scope='session')
def mysq_database_name():
    """Name of test database to be created."""
    return 'test'


@pytest.fixture(scope='session')
def mysql_database_getter(run_services, mysql_watcher, mysql_socket):
    """Prepare new test database creation function."""
    if run_services:
        def getter(database_name):
            check_output(
                [
                    'mysql',
                    '--user=root',
                    '--socket={0}'.format(mysql_socket),
                    '--execute=create database {0};'.format(database_name),
                ],
            )
        return getter


@pytest.fixture(scope='session')
def mysql_database(run_services, mysql_database_getter, mysq_database_name):
    """Prepare new test database creation function."""
    if run_services:
        return mysql_database_getter(mysq_database_name)


@pytest.fixture(scope='session')
def mysql(request, run_services, mysql_watcher, mysql_database):
    """The mysql instance which is ready to be used by the tests."""
    if run_services:
        return mysql_watcher
