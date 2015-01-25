#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/conftest.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
import pytest

from complexity import create_app

@pytest.fixture
def app(tmpfile):
    return create_app(SHELVE_FILENAME=tmpfile)

@pytest.fixture
def client(app):
    return app.test_client()

def test_foo(client):
    print client.get('/')

