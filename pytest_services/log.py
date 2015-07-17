"""Logging fixtures and functions."""
import contextlib
import logging
import logging.handlers
import socket

import pytest


@pytest.fixture(scope='session')
def services_log(slave_id):
    """A services_logger with the slave id."""
    handler = None
    for kwargs in (dict(socktype=socket.SOCK_RAW), dict(socktype=socket.SOCK_STREAM), dict()):
        try:
            handler = logging.handlers.SysLogHandler(
                facility=logging.handlers.SysLogHandler.LOG_LOCAL7, address='/dev/log', **kwargs)
            break
        except (IOError, TypeError):
            pass
    logger = logging.getLogger('[{slave_id}] {name}'.format(name=__name__, slave_id=slave_id))
    logger.setLevel(logging.DEBUG)
    if handler:
        logger.propagate = 0
        logger.addHandler(handler)
    return logger


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
