#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Complexity: tests/views/quizzes/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import json

class Quiz(object):
    """
    A class to manage common operations to quizzes.

    Each instance represents the operations for a specific
    'quiz_module'. Hence, a new instance is requied for each module
    and NOT for each quiz attempt.
    """
    def __init__(self, module):
        self.module = module

    def new(self, test_client):
        """
        Makes a request to the application to create a new quiz.
        """
        return test_client.get('/quiz/{}/_new'.format(self.module))

    def next(self, test_client, data=None):
        """
        Makes a reuest for the nest part of the quiz.#
        
        This is a POST request if `data` is provided.
        """
        if data is None:
            return test_client.get(
                '/quiz/{}/_next'.format(self.module)
            )

        url = '/quiz/{}/_next'.format(self.module)
        data = json.dumps(data)
        return test_client.post(
            url,
            data=data,
            content_type='application/json'
        )

    def answer(self, test_client, answer):
        """
        Answer next question to the quiz.
        """
        # Load question.
        resp = self.next(test_client)
        q = json.loads(resp.data)
        question = q['question']

        # Build the answer using the selector function (or optionally
        # answer value) and response time from the `answer` list.
        answer = [
            (
                ans(question) if hasattr(ans, '__call__') else ans,
                response_time
            )
            for ans, response_time in answer
        ]

        # Return dictionary representing the returned JSON.
        return json.loads(self.next(
            test_client,
            dict(answer=answer)
        ).data)

    def get_patterns(self, test_client):
        """
        Return possible patterns for question.
        The server must have first responded with spotted=True.
        """
        return json.loads(
            self.next(test_client, dict(spotted=True)).data
        )['patterns']

    def answer_correct(self, test_client, *response_times):
        """
        Answer question with correct answers and with the given
        response times.
        """
        # Select the correct answer.
        answer_selector = lambda i: (lambda question: question[i][2])

        return self.answer(test_client, [
            (answer_selector(i), response_times[i])
            for i in xrange(3)
        ])

    def answer_incorrect(self, test_client, *response_times):
        """
        Answer question with incorrect answers and with the given
        response times.
        """
        # Select the first incorrect answer.
        def answer_selector(i):
            def func(question):
                correct = question[i][2]
                return (correct + 1) % 3

        return self.answer(test_client, [
            (answer_selector(i), response_times[i])
            for i in xrange(3)
        ])

    def finish(self, test_client, name):
        self.next(test_client)
        url = "/quiz/{}/finish".format(self.module)
        return test_client.post(
            url,
            data=dict(name=name),
        )

