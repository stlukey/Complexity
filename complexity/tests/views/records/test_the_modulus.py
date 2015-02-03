#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    complexity: tests/views/records/test_the_modulus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from ..quizzes import Quiz

quiz = Quiz("the_modulus")

records_url = "/records/{}".format("the_modulus")

NAMES = ["Jack", "Harry", "Emma", "Hannah", "Tom"]

def test_added(test_client):
    """
    Test that a record is saved once a quiz is complete.
    """
    assert NAMES[0] not in test_client.get(records_url).data
    
    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[0]) 

    assert NAMES[0] in test_client.get(records_url).data

def test_order(test_client):
    """
    Test that records are stored in order.
    """
    
    for name in NAMES:
        assert name not in test_client.get(records_url).data

    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_incorrect(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[1]) 

    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[0]) 

    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_incorrect(test_client, *([2]*3))
    quiz.answer_incorrect(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[2]) 

    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_correct(test_client, *([3]*3))
    quiz.answer_incorrect(test_client, *([1]*3))
    quiz.answer_incorrect(test_client, *([2]*3))
    quiz.answer_incorrect(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[3]) 

    quiz.new(test_client)
    quiz.answer_correct(test_client, *([1]*3))
    quiz.answer_correct(test_client, *([2]*3))
    quiz.answer_incorrect(test_client, *([3]*3))
    quiz.answer_incorrect(test_client, *([1]*3))
    quiz.answer_incorrect(test_client, *([2]*3))
    quiz.answer_incorrect(test_client, *([3]*3))
    resp = quiz.finish(test_client, NAMES[4]) 

    last = 0

    records = test_client.get(records_url).data

    for name in NAMES:
        next = records[last:].find(name)
        assert next != -1
        last += next

