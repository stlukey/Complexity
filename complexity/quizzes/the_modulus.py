#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quizzes/the_modulus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import random

from flask import request

from . import BaseQuiz
from ..maths import *


class MultipleChoiceQuestion(object):
    def __init__(self):
        self.answered = False
        self.score = 0

    @staticmethod
    def _make_part(part):
        question, answers = part

        question = question.render()
        answers = map(lambda expr: str(expr.render()), answers)
        correct_answer = answers.pop(0)

        correct_answer_index = random.randrange(0, 3)
        answers.insert(correct_answer_index, correct_answer)

        return question, answers, correct_answer_index

    @property
    def question(self):
        if not hasattr(self, '_question'):
            self._question = map(self._make_part, self.parts)

        return self._question

    def ask(self):
        return dict(
            data=self.data,
            question=self.question
        )

    def answer(self, req_data):
        if self.answered:
            raise ValueError

        answers = req_data['answers']

        for i in xrange(len(self.parts)):
            if answers[i][0] == self._question[i][2]:
                self.score += 5

        self.answered = True
        return self.score


class MultiplyQuestion(MultipleChoiceQuestion):
    def __init__(self, *args, **kwargs):
        # Variables used to represent questions.
        self.z_var = MathsVariable('z')
        self.w_var = MathsVariable('w')
        self.zw_var = MathsExpression([
                self.z_var,
                self.w_var
            ],
            OPERATORS.multiply
        )

        # Per-Question random variable definitions.
        self.z = MathsComplexNumber(
            MathsRandomConstant(1, 11),
            MathsRandomConstant(1, 11)
        )
        self.w = MathsComplexNumber(
            MathsRandomConstant(1, 11),
            MathsRandomConstant(1, 11)
        )
        self.zw = self.z.compute_product(self.w)

        self.data = dict(z=self.z.render(), w=self.w.render())
        self.parts = [self.part_one, self.part_two, self.part_three]
        super(MultiplyQuestion, self).__init__(*args, **kwargs)

    @property
    def part_one(self):
        if not hasattr(self, '_part_one'):
            question = self.zw_var
            answers = self.zw, MathsConstant(1), MathsConstant(2)

            self._part_one = question, answers
        
        return self._part_one

    @property
    def part_two(self):
        def answers():
            zw_mod = self.zw.compute_modulus()

            zw_mod_squared = zw_mod.operands[0]

            step = int(zw_mod_squared.render() * 0.1)
            start = int(zw_mod_squared.render() - step*10)
            end = int(zw_mod_squared.render() + step*10)

            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    OPERATORS.sqrt
                ) for _ in xrange(2)
            ]

            return [zw_mod] + wrong_answers


        if not hasattr(self, '_part_two'):
            question = MathsExpression(
                self.zw_var,
                OPERATORS.abs
            )

            self._part_two = question, answers()

        return self._part_two

    @property
    def part_three(self):
        def question():
            # |z|
            z_mod_var = MathsExpression([
                    MathsVariable('z'),
                ], OPERATORS.abs
            )
            # |w|
            w_mod_var = MathsExpression([
                    MathsVariable('w'),
                ], OPERATORS.abs
            )
            # |z||w|
            return MathsExpression([
                    z_mod_var, w_mod_var
                ], OPERATORS.multiply
            )

        def answers():
            # |a + bj| = sqrt(a*a + b*b)
            z_mod = self.z.compute_modulus()
            w_mod = self.w.compute_modulus()
            # |a + bj|^2 = a*a + b*b.
            z_mod_squared = z_mod.operands[0]
            w_mod_squared = w_mod.operands[0]
            # |a + bj|^2 |c + dj|^2 = (a*a + b*b)(c*c + d*d)
            z_mod_squared_w_mod_squared = MathsConstant(
                z_mod_squared.render() * w_mod_squared.render()
            )
            # |a + bj||c + dj| = sqrt[ (a*a + b*b) (c*c + d*d) ]
            z_mod_w_mod = MathsExpression(
                z_mod_squared_w_mod_squared,
                OPERATORS.sqrt
            )

            step = int(z_mod_squared_w_mod_squared.render() * 0.1)
            start = int(z_mod_squared_w_mod_squared.render() - step*10)
            end = int(z_mod_squared_w_mod_squared.render() + step*10)

            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    OPERATORS.sqrt
                ) for _ in xrange(2)
            ]

            return [z_mod_w_mod] + wrong_answers

        if not hasattr(self, '_part_three'):
            self._part_three = question(), answers()

        return self._part_three

    def pattern(self, user_answer=None):
        equal = lambda exp1, exp2: '{} = {}'.format(exp1.render(),
                                                    exp2.render())

        z_mod_var = MathsExpression(self.z_var, OPERATORS.abs)
        w_mod_var = MathsExpression(self.w_var, OPERATORS.abs)
        z_mod_w_mod_var = MathsExpression([
            z_mod_var,
            w_mod_var
        ])

        zw_mod_var = MathsExpression(self.zw_var, OPERATORS.abs)

        correct_answer = equal(zw_mod_var, z_mod_w_mod_var)
        incorrect_answer_one = equal(z_mod_var, w_mod_var)
        incorrect_answer_two = equal(z_mod_var, zw_mod_var)

        if user_answer is not None:
            return correct_answer == user_answer

        answers = [
            correct_answer,
            incorrect_answer_one,
            incorrect_answer_two
        ]
        random.shuffle(answers)

        return answers


class Quiz(BaseQuiz):
    def __init__(self, *args, **kwargs):
        self.questions = [(MultiplyQuestion, 5)]
        self.repeat_limit = 0
        self.repeat_count = 0
        self.score = 0
        self.prev_resp_time = None
        self.ask_spotted = False

    @property
    def question(self):
        if hasattr(self, '_question'):
            if not self._question.answered:
                return self._question

        if not hasattr(self, '_Question') or self.repeat_count >= self.repeat_limit:
            self.repeat_count = 0
            self.prev_resp_time = None
            self.ask_spotted = 0
            self._Question, self.repeat_limit = self.questions.pop(0)

        self.repeat_count += 1
        self._question = self._Question()
        return self._question

    def next(self, json=None):
        if self.ask_spotted in (1, 2):
            if self.ask_spotted == 2:
                score =  5 + (self.repeat_limit - self.repeat_count) * len(self.question.parts) * 5
                if self._question.pattern(json.data['answer']):
                    self.score += score
                self.ask_spotted = 0
                self.repeat_count = self.repeat_limit
                return dict(score=self.score)

            if json.get('spotted', False):
                self.ask_spotted = 2
                return dict(patterns=self.question.pattern())
            
            self.ask_spotted = 0

        if self.question is None:
            return self.finish()

        return {
            'GET': self.get_question,
            'POST': self.answer_question,
        }[request.method](json)


    def get_question(self, json=None):
        """Get current question."""
        return self.question.ask()

    def answer_question(self, json):
        """Answer current question."""

        self.score += self.question.answer(json)
        
        resp_time = json['answers'][-1][1]
        if self.prev_resp_time is not None:
            self.ask_spotted = int(resp_time < self.prev_resp_time)
        self.prev_resp_time = resp_time
        
        return dict(
            score=self.score,
            ask_spotted=self.ask_spotted
        )

    def finish_quiz(self):
        """Finish quiz, save scores"""
        pass



