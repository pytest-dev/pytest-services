"""Services plugin for pytest.

Provides an easy way of running service processes for your tests.
"""

from .folders import *  # NOQA
from .log import *  # NOQA
from .locks import *  # NOQA
from .xvfb import *  # NOQA
from .memcached import *  # NOQA
from .mysql import *  # NOQA
from .service import *  # NOQA


def pytest_addoption(parser):
    """Add options for services plugin."""
    group = parser.getgroup("services", "service processes for tests")
    group._addoption(
        '--run-services',
        action="store_true", dest="run_services",
        default=False,
        help="Run services automatically by pytest")
    group._addoption(
        '--xvfb-display',
        action="store", dest="display",
        default=None,
        help="X display to use")
