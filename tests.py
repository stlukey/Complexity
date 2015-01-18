#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests
    ~~~~~~~~~~~~~~~~~
 m+
    Test suite for complexity.

    Copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""
import os
import unittest

from complexity import app
from complexity.quizzes import quiz_modules

import json


class ComplexityTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SHELVE_FILENAME'] = 'test.bin'
        app.config['TESTING'] = True
        self.test_client = app.test_client()

    def tearDown(self):
        os.unlink(app.config['SHELVE_FILENAME'])

    def quiz_new(self, quiz_module):
        return self.test_client.get('/quiz/{}/_new'.format(quiz_module))

    def quiz_next(self, quiz_module):
        return self.test_client.get('/quiz/{}/_next'.format(quiz_module))

    def quiz_choose(self):
        return self.test_client.get('/quiz/choose')

    def quiz_next_post(self, quiz_module, data):
        url = '/quiz/{}/_next'.format(quiz_module)
        data = json.dumps(data)
        return self.test_client.post(url, data=data, content_type='application/json')


    def test_quiz_cookies(self):
        resp = self.quiz_next(quiz_modules[0])
        self.assertNotEqual(resp.status, '200 OK')

        self.quiz_new(quiz_modules[0])

        resp = self.quiz_next(quiz_modules[0])
        self.assertEqual(resp.status, '200 OK')

        self.test_client.cookie_jar = None


        resp = self.quiz_next(quiz_modules[0])
        self.assertEqual(resp.status, '400 BAD REQUEST')

    def the_modulus_two_correct(self, module="the_modulus"):
        # Answer first question perfectly.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        question = q['question']
        answer = [
            (question[0][2], 10),
            (question[1][2], 9),
            (question[2][2], 3)
        ]
        resp = self.quiz_next_post(module, dict(answer=answer))
        score = json.loads(resp.data)['score']
        self.assertEqual(score, 3 * 5)

        # Answer second question perfectly, but faster.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        question = q['question']
        answer = [
            (question[0][2], 5),
            (question[1][2], 3),
            (question[2][2], 1)
        ]
        resp = self.quiz_next_post(module, dict(answer=answer)).data
        resp = json.loads(resp)
        self.assertEqual(resp['score'], 3 * 5 * 2)

        return resp

    def test_the_modulus_all_correct(self):
        module = 'the_modulus'

        self.quiz_new(module)
        
        resp = self.the_modulus_two_correct(module)

        # Server detect pattern may have been spotted and user says
        # they've spotted it.
        self.assert_(resp['spotted'])
        patterns = json.loads(
            self.quiz_next_post(module, dict(spotted=True)).data
        )['patterns']


        CORRECT_PATTERN = r'\left|zw \right| = \left|z \right|\left|w \right|'

        self.assertIn(CORRECT_PATTERN, patterns)

        # User shows they've correctly spotted the pattern and scores
        # marks for next question.
        resp = self.quiz_next_post(module, dict(answer=CORRECT_PATTERN))
        score = json.loads(resp.data)['score']
        self.assertEquals(score, 5*3*5 + 5)

        self.quiz_choose()

    def test_the_modulus_all_correct_not_spotted(self):
        module = 'the_modulus'

        self.quiz_new(module)

        resp = self.the_modulus_two_correct(module)

        # Server detect pattern may have been spotted and user says
        # they've spotted it.
        self.assert_(resp['spotted'])
        patterns = json.loads(
            self.quiz_next_post(module, dict(spotted=True)).data
        )['patterns']


        CORRECT_PATTERN = r'\left|zw \right| = \left|z \right|\left|w \right|'

        self.assertIn(CORRECT_PATTERN, patterns)

        # User shows they've correctly spotted the pattern and scores
        # marks for next question.
        del patterns[patterns.index(CORRECT_PATTERN)]
        resp = self.quiz_next_post(module, dict(answer=patterns.pop()))
        score = json.loads(resp.data)['score']
        self.assertEquals(score, 2*3*5)

        self.quiz_choose()

if __name__ == '__main__':
    unittest.main()

