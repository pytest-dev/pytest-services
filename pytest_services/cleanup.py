"""Cleanup after test run."""
import os.path
import glob
import shutil
import fcntl
import errno

import pytest

from .process import (
    check_output,
    CalledProcessWithOutputError,
)
from .locks import (
    lock_file,
    unlock_file,
    file_lock,
)


def clean_stale_locks(lock_dir, session_id, log):
    """Clean stale lock of previous test runs."""
    for lock in glob.iglob(os.path.join(lock_dir, 'pl-*.lock')):
        log.debug('found lock: {0}'.format(lock))
        try:
            handle = lock_file(lock, session_id, operation=fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            if e.errno in (errno.EACCES, errno.EAGAIN):
                with open(lock, 'r') as fd:
                    locked_id = fd.read()
                log.debug('found session lock: {0}'.format(locked_id))
                yield 'sr-{0}'.format(locked_id)
        else:
            log.debug('removing stale lock: {0}'.format(lock))
            unlock_file(lock, handle)


def get_session_id(filename):
    """Get session id from given filename. Used to defer session id from artifact paths."""
    return os.path.splitext(os.path.basename(filename))[0]


def clean_disk_artifacts(root_dir, locked_ids, log):
    """Clean disk-based artifacts from previous test runs."""
    for proc in glob.iglob(os.path.join(root_dir, 'pl-*')):
        proc_id = get_session_id(proc)
        if proc_id in locked_ids:
            # not remove current session's folder
            log.debug('skipping removal: {0}'.format(proc))
            continue
        try:
            args = ['pkill', '-u', os.environ['USER'], '-f', proc_id]
            log.debug('killing: {0}'.format(['pkill', '-u', os.environ['USER'], '-f', proc_id]))
            check_output(args)
        except CalledProcessWithOutputError:
            pass
        log.debug('removing: {0}'.format(proc))
        shutil.rmtree(proc, ignore_errors=True)


def clean_memory_artifacts(memory_root_dir, locked_ids, log):
    """Clean memory-based artifacts from previous test runs."""
    for proc in glob.iglob(os.path.join(memory_root_dir, 'pl-*')):
        proc_id = get_session_id(proc)
        if proc_id in locked_ids:
            # not remove current session's folder
            log.debug('skipping removal: {0}'.format(proc))
            continue
        log.debug('removing: {0}'.format(proc))
        shutil.rmtree(proc, ignore_errors=True)


@pytest.fixture(scope='session')
def test_cleanup(run_services, session_id, root_dir, lock_dir, memory_root_dir, log):
    """Clean up stale files from other test runs."""
    if run_services:
        with file_lock(os.path.join(lock_dir, 'test_cleanup')):
            log.debug('starting cleaning up, session_id: {0}'.format(session_id))

            locked_ids = ['sr-{0}'.format(session_id)]

            # clean stale locks
            locked_ids.extend(clean_stale_locks(lock_dir, session_id, log))

            # clean disk-based artifacts
            clean_disk_artifacts(root_dir, locked_ids, log)

            # clean memory-based artifacts
            clean_memory_artifacts(root_dir, locked_ids, log)

        log.debug('cleaning up done, session_id: {0}'.format(session_id))
