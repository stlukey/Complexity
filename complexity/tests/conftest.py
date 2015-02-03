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

# NOTE: Fixtures are used to setup and clean up an environment for
#       each test to run. When a test has a parameter with the same
#       name as a fixture, the return value of the fixture is passed
#       to the test.

@pytest.fixture
def app(request, tmpdir):
    """
    Setup Flask app instance.

    :param request: Fixture request object passed by pytest.
    :param tmpdir: Builtin fixture for a temporary directory.
    """

    # Create path to shelve file.
    shelve = str(tmpdir.join('test_complexity.bin'))

    def clean_up():
        # Remove shelve file and temp directory.
        os.unlink(shelve)
        tmpdir.remove()
    request.addfinalizer(clean_up)

    return create_app(SHELVE_FILENAME=shelve)

@pytest.fixture
def test_client(app):
    """
    Create test client for flask app.

    :param app: Custom app fixture.
    """
    return app.test_client()

