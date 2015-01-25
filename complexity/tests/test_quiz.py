#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/test_quiz.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

def test_root(test_client):
    assert 'Complexity' in test_client.get('/').data
