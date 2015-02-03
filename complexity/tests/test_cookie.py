#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/test_cookie.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from complexity.cookie import Cookie

DATA = 'somedata'
FAKE_SIGNATURE = 'fake-signature'

def test_creation():
    """
    Teat the creation of the Cookie object.
    """
    cookie = Cookie(DATA)

    # Cookie value should start with the data and the delimiter.
    assert cookie.value.startswith(DATA + '|')

    # All new cookies have there data accesable.
    assert cookie.data == DATA

def test_real_cookie():
    """
    Test cookie verification with a correct cookie.
    """
    cookie = Cookie(DATA)
    cookie_str = cookie.value

    cookie_with_check = Cookie(cookie_str, new=False)
    assert cookie_with_check.data == DATA

def test_fake_cookie():
    """
    Test cookie verification with a fake cookie.
    """
    cookie_str = '{}|{}'.format(DATA, FAKE_SIGNATURE)

    cookie_with_check = Cookie(cookie_str, new=False)
    assert cookie_with_check.data is None

