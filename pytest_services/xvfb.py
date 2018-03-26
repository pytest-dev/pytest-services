"""Fixtures for the GUI environment."""
import os
import fcntl
import socket
import re
try:
    import subprocess32 as subprocess
except ImportError:  # pragma: no cover
    import subprocess

import pytest

from .locks import (
    file_lock,
)


def xvfb_supports_listen():
    """Determine whether the '-listen' option is supported by Xvfb."""
    p = subprocess.Popen(
        ['Xvfb', '-listen', 'TCP', '-__sentinel_parameter__'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    _, stderr = p.communicate()

    match = re.search(
        br'^Unrecognized option: (?P<option>.*)$',
        stderr,
        flags=re.MULTILINE,
    ).groupdict()
    unrecognized_option = match['option']
    return unrecognized_option != b'-listen'


@pytest.fixture(scope='session')
def xvfb_display(request, run_services, lock_dir, services_log, display_getter):
    """The DISPLAY environment variable used in this test run.

    In case it is not a local run, a random value will be picked up and set,
    otherwise it will be taken from the environment.

    """
    if run_services:
        if request.config.option.display:
            display = request.config.option.display
        else:
            display = display_getter()
        os.environ['DISPLAY'] = ':{0}'.format(display) if ':' not in str(display) else display

        return display


@pytest.fixture(scope='session')
def xvfb_resolution():
    """xvfb display resolution."""
    return (1366, 768, 8)


@pytest.fixture(scope='session')
def xvfb(request, run_services, xvfb_display, lock_dir, xvfb_resolution, watcher_getter):
    """The Xvfb process."""
    if request.config.option.display or not run_services:
        # display is passed, no action required
        return

    if xvfb_supports_listen():
        listen_args = ['-listen', 'TCP']
    else:
        listen_args = []

    with file_lock(os.path.join(lock_dir, 'xvfb_{0}.lock'.format(xvfb_display)),
                   operation=fcntl.LOCK_EX | fcntl.LOCK_NB):

        def checker():
            try:
                socket.create_connection(('127.0.0.1', 6000 + xvfb_display))
                return True
            except socket.error:
                pass

        return watcher_getter(
            'Xvfb', [
                ':{display}'.format(display=xvfb_display),
                '-screen',
                '0',
                'x'.join(str(value) for value in xvfb_resolution),
                '-ac',
                '-nolock',
                '+extension', 'RANDR'
            ] + listen_args,
            checker=checker,
            request=request,
        )
