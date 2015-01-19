"""Configuration for pytest runner."""

pytest_plugins = 'pytester'

import pytest


@pytest.fixture(scope='session')
def run_services():
    """Run services for tests."""
    return True
