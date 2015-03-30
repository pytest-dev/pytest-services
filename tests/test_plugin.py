"""Tests for pytest-services plugin."""
import os.path
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


def test_mysql(mysql, mysql_connection):
    """Test mysql service."""
    conn = MySQLdb.connect(user='root')
    assert conn


def test_xvfb(xvfb, xvfb_display):
    """Test xvfb service."""
    socket.create_connection(('127.0.0.1', 6000 + xvfb_display))


def test_port_getter(port_getter):
    """Test port getter utility."""
    port1 = port_getter()
    sock1 = socket.socket(socket.AF_INET)
    sock1.bind(('127.0.0.1', port1))
    assert port1
    port2 = port_getter()
    sock2 = socket.socket(socket.AF_INET)
    sock2.bind(('127.0.0.1', port2))
    assert port2
    assert port1 != port2


def test_display_getter(display_getter):
    """Test display getter utility."""
    display1 = display_getter()
    assert display1
    display2 = display_getter()
    assert display2
    assert display1 != display2


def test_temp_dir(temp_dir):
    """Test temp dir directory."""
    assert os.path.isdir(temp_dir)
