#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    complexity: tests/views/quizzes/test_the_modulus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import json

from . import Quiz

CORRECT_PRODUCT_PATTERN =\
        r'\left|zw \right| = \left|z \right|\left|w \right|'

quiz = Quiz("the_modulus")

def test_first_two_correct(test_client):
    """
    Tests if the server returns the correct score and detects a
    pattern may have been spotted when the correct answers and
    response times are given for the first two questions.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Answer first question correctly.
    time = 3
    score = quiz.answer_correct(test_client, *([time]*3))['score']
    assert score == 5*3

    # Answer second question correctly, but faster.
    time -= 2
    resp = quiz.answer_correct(test_client, *([time]*3))
    assert resp['score'] == 5*3*2

    # The server should detect a pattern may have been spotted.
    assert resp['spotted']

def test_product_pattern(test_client):
    """
    Tests when first two answers are correct and the user says
    they've spotted a pattern if the correct pattern exists in the
    possible patterns.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Answer first two correct.
    quiz.answer_correct(test_client, *([3]*3))
    resp = quiz.answer_correct(test_client, *([1]*3))

    # Get possible answers.
    patterns = quiz.get_patterns(test_client)

    # The answers must contain the correct pattern.
    assert CORRECT_PRODUCT_PATTERN in patterns


def test_product_all_correct(test_client):
    """
    Test for when a user answers the modulus's product questions
    perfectly.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Answer first two correct.
    quiz.answer_correct(test_client, *([3]*3))
    resp = quiz.answer_correct(test_client, *([1]*3))

    # Get possible answers.
    patterns = quiz.get_patterns(test_client)

    # Show correct pattern has been spotted.
    score = json.loads(quiz.next(
        test_client,
        dict(answer=CORRECT_PRODUCT_PATTERN)
    ).data)['score']

    # Each question has three parts and each part has 5 points.
    # Each type of question gets repeated 3 times with random content
    # each time. If the pattern gets spotted all the points are given
    # (5*3*4) plus 5 extra.
    assert score == 5*3*3 +5

def test_product_not_spotted(test_client):
    """
    Test for when a user answers first two questions correct but
    fails to spot the pattern correctly.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Answer first two correct.
    quiz.answer_correct(test_client, *([3]*3))
    resp = quiz.answer_correct(test_client, *([1]*3))

    # Get possible answers.
    patterns = quiz.get_patterns(test_client)

    # Remove correct answer from the answers.
    correct = patterns.index(CORRECT_PRODUCT_PATTERN)
    del patterns[correct]

    # Answer with the wrong pattern.
    score = json.loads(quiz.next(
        test_client,
        dict(answer=patterns[0])
    ).data)['score']

    # The user should not be awarded the points.
    assert score != 5*3*3 +5

def test_erroneous_answers(test_client):
    """
    Test for when a erroneous index is provided in an answer.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Answer question with erroneous index for the answers.
    quiz.next(test_client)
    answer = [(99, 99)] * 3
    resp = quiz.next(test_client, dict(answer=answer))

    # The server should process the answer as normal but not
    # award any points.
    assert resp.status == '200 OK'


def test_extreme_answers(test_client):
    """
    Test for when the extreme answer index are provided.
    """
    # Create a new quiz instance.
    quiz.new(test_client)

    # Test for 0 index.
    quiz.next(test_client)
    answer = [(0, 9)] * 3
    resp = quiz.next(test_client, dict(answer=answer))
    assert resp.status == '200 OK'

    # Test for 2 index.
    quiz.next(test_client)
    answer = [(2, 9)] * 3
    resp = quiz.next(test_client, dict(answer=answer))
    assert resp.status == '200 OK'

