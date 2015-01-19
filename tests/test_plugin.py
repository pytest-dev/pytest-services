"""Tests for pytest-services plugin."""
import socket

import pylibmc
import MySQLdb


def test_memcached(request, memcached, memcached_socket):
    """Test memcached service."""
    mc = pylibmc.Client([memcached_socket])
    mc.set('some', 1)
    assert mc.get('some') == 1

    # check memcached cleaner
    request.getfuncargvalue('memcached_clean')
    assert mc.get('some') is None


def test_mysql(request, mysql, mysql_connection):
    """Test mysql service."""
    conn = MySQLdb.connect(user='root')
    assert conn


def test_xvfb(request, xvfb, xvfb_display):
    """Test xvfb service."""
    socket.create_connection(('127.0.0.1', 6000 + xvfb_display))
