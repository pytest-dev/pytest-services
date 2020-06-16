"""Logging fixtures and functions."""
import contextlib
import logging
import logging.handlers
import socket

import pytest


@pytest.fixture(scope='session')
def services_log(worker_id):
    """A services_logger with the worker id."""
    handler = None
    for kwargs in (dict(socktype=socket.SOCK_RAW), dict(socktype=socket.SOCK_STREAM), dict()):
        try:
            handler = logging.handlers.SysLogHandler(
                facility=logging.handlers.SysLogHandler.LOG_LOCAL7, address='/dev/log', **kwargs)
            break
        except (IOError, TypeError):
            pass
    logger = logging.getLogger('[{worker_id}] {name}'.format(name=__name__, worker_id=worker_id))
    logger.setLevel(logging.DEBUG)
    if handler and workaround_issue_20(handler):
        logger.propagate = 0
        logger.addHandler(handler)
    return logger


def workaround_issue_20(handler):
    """
    Workaround for
    https://github.com/pytest-dev/pytest-services/issues/20,
    disabling installation of a broken handler.
    """
    return hasattr(handler, 'socket')


@contextlib.contextmanager
def dont_capture(request):
    """Suspend capturing of stdout by pytest."""
    capman = request.config.pluginmanager.getplugin("capturemanager")
    capman.suspendcapture()
    try:
        yield
    finally:
        capman.resumecapture()


def remove_handlers():
    """Remove root services_logging handlers."""
    handlers = []
    for handler in logging.root.handlers:
        if not isinstance(handler, logging.StreamHandler):
            handlers.append(handler)
    logging.root.handlers = handlers
