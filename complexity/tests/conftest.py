#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/conftest.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
import os
import pytest

from complexity import create_app

@pytest.fixture
def app(request, tmpdir):
    shelve = str(tmpdir.join('test_complexity.bin'))
    def clean_up():
        os.unlink(shelve)
        tmpdir.remove()
    request.addfinalizer(clean_up)
    return create_app(SHELVE_FILENAME=shelve)

@pytest.fixture
def test_client(app):
    return app.test_client()

