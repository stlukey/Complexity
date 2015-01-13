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
from complexity.quizzes import quiz_modules
from complexity.quiz import COOKIE_QUIZ

import json


class ComplexityTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SHELVE_FILENAME'] = 'test_' + app.config['SHELVE_FILENAME']
        app.config['TESTING'] = True
        self.test_client = app.test_client()

    def tearDown(self):
        # os.unlink(app.config['SHELVE_FILENAME'])
        pass

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

        self.quiz_choose()

        resp = self.quiz_next(quiz_modules[0])
        self.assertNotEqual(resp.status, '200 OK')


    def test_the_modulus_all_correct(self):
        module = 'the_modulus'

        self.quiz_new(module)
        
        # Answer first question perfectly.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        answers = [
            (q['question'][0][2], 10),
            (q['question'][1][2], 9),
            (q['question'][2][2], 3)
        ]
        resp = self.quiz_next_post(module, dict(answers=answers))
        score = json.loads(resp.data)['score']
        assert score == 3 * 5

        # Answer second question perfectly, but faster.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        answers = [
            (q['question'][0][2], 5),
            (q['question'][1][2], 3),
            (q['question'][2][2], 1)
        ]
        resp = self.quiz_next_post(module, dict(answers=answers))
        score = json.loads(resp.data)['score']
        assert score == 3 * 5 * 2

        # Server detect pattern may have been spotted and user says
        # they've spotted it.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        assert q['ask_spotted']
        # Resend `q` again to mimic spotted request.
        patterns = self.quiz_next_post(module, dict(spotted=True))


        # User shows they've correctly spotted the pattern and scores
        # marks for next question.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        resp = self.quiz_next_post(module, dict(pattern=r'\left|zw \right| = \left|z \right|\left|w \right|'))
        score = json.loads(resp.data)['score']
        assert score == 3 * 5 * 5 + 5

        self.quiz_choose()

    def test_the_modulus_incorrect_pattern_spotted(self):
        module = 'the_modulus'

        self.quiz_new(module)
        
        # Answer first question perfectly.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        answers = [
            (q['question'][0][1][q['question'][0][2]], 10),
            (q['question'][1][1][q['question'][1][2]], 9),
            (q['question'][2][1][q['question'][2][2]], 3)
        ]
        resp = self.quiz_next_post(module, answers)
        score = json.loads(resp.data)['score']
        assert score == 3 * 5

        # Answer second question perfectly, but faster.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        answers = [
            (q['question'][0][1][q['question'][0][2]], 5),
            (q['question'][1][1][q['question'][1][2]], 3),
            (q['question'][2][1][q['question'][2][2]], 1)
        ]
        resp = self.quiz_next_post(module, answers)
        score = json.loads(resp.data)['score']
        assert score == 3 * 5 * 2

        # Server detect pattern may have been spotted and user says
        # they've spotted it.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        assert q['ask_spotted']
        # Resend `q` again to mimic spotted request.
        resp = self.quiz_next_post(module, q)
        score = json.loads(resp.data)['score']
        assert score == 3 * 5

        # User shows they've incorrectly spotted the pattern and
        # scores marks for next 2 questions are lost.
        resp = self.quiz_next(module)
        q = json.loads(resp.data)
        answers = [
            (q['question'][0][1][q['question'][0][2]-1], 10),
        ]
        resp = self.quiz_next_post(module, answers)
        score = json.loads(resp.data)['score']
        assert score == 3 * 5

        self.quiz_choose()

if __name__ == '__main__':
    unittest.main()

