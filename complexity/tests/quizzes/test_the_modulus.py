#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/quizzes/the_modulus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import json

def quiz_new(test_client, quiz_module):
    return test_client.get('/quiz/{}/_new'.format(quiz_module))

def quiz_next(test_client, quiz_module, data=None):
    if data is None:
        return test_client.get('/quiz/{}/_next'.format(quiz_module))

    url = '/quiz/{}/_next'.format(quiz_module)
    data = json.dumps(data)
    return test_client.post(
        url,
        data=data,
        content_type='application/json'
    )

def quiz_answer(test_client, quiz_module, answer):
    resp = quiz_next(test_client, quiz_module)
    q = json.loads(resp.data)
    question = q['question']
    answer = [
        (selector(question), response_time)
        for selector, response_time in answer
    ]
    return json.loads(quiz_next(
        test_client,
        quiz_module,
        dict(answer=answer)
    ).data)

def test_two_correct(test_client, quiz_module="the_modulus"):

    answer_selector = lambda i: (lambda question: question[i][2])

    quiz_new(test_client, quiz_module)

    score = quiz_answer(test_client, quiz_module, [
        (answer_selector(0), 10),
        (answer_selector(1), 9),
        (answer_selector(2), 3)
    ])['score']
    assert score == 3*5

    resp = quiz_answer(test_client, quiz_module, [
        (answer_selector(0), 5),
        (answer_selector(1), 3),
        (answer_selector(2), 1)
    ])
    assert resp['score'] == 3*5*2

    return resp

