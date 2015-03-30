"""Configuration for pytest runner."""

import pytest

pytest_plugins = 'pytester'


@pytest.fixture(scope='session')
def run_services():
    """Run services for tests."""
    return True
