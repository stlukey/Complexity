#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests
    ~~~~~~~~~~~~~~~~~
    
    Test suite for complexity.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""
import os
import unittest
import tempfile

from complexity import app
from complexity.quizes import quiz_modules
from complexity.quiz import COOKIE_QUIZ

class ComplexityTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SHELVE_FILENAME'] = 'test_' + app.config['SHELVE_FILENAME']
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.unlink(app.config['SHELVE_FILENAME'])

    def test_quiz_cookies(self):
        resp = self.app.get('/quiz/{}/next'.format(quiz_modules[0]))
        self.assertNotEqual(resp.status, '200 OK')
        
        self.app.get('/quiz/{}/new'.format(quiz_modules[0]))
        
        quiz_id = None
        for cookie in self.app.cookie_jar:
            if cookie.name == COOKIE_QUIZ:
                quiz_id = cookie.value
        self.assertIsNotNone(quiz_id)

        resp = self.app.get('/quiz/{}/next'.format(quiz_modules[0]))
        self.assertEqual(resp.status, '200 OK')

if __name__ == '__main__':
    unittest.main()

