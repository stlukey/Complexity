#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quizzes/the_modulus.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains a quiz implementation (`Quiz`) for the modulus topic.

"""

import random

from flask import request

from . import BaseQuiz
from ..maths import *
from ..maths.complex import (compute_modulus, compute_product,
                             compute_divide)
from ..errors import BadRequestError


class MultipleChoiceQuestion(object):
    """
    Inherited by questions with a multiple choice structure.

    Each question has three parts. For each part, a choice of
    three answers is provided; a correct one and two wrong ones.

    Once inherited the child class has to define the following
    instance varibles:

    :ivar data: Dictionary of variable definitions needed to answer
                the question.

    :ivar parts: A list of `tuple`s for each part of the question.
                 The first element being the `MathOperand`
                 representing the question and the second a list of
                 `MathOperand`s containing the correct answer
                 followed by two incorrect answers.
    """
    def __init__(self):
        self.answered = False
        self.score = 0
        self.results = []

    @staticmethod
    def _make_part(part):
        """
        Renders an randomises part and puts it into the correct
        format to be sent.

        :param part: A `tuple`, from `self.parts`.

        :returns: A `tuple` containing the rendered question, a
                   shuffled list of the answers rendered and
                   the index of the correct answer in that list.
        """
        question, answers = part

        # Render the question.
        question = question.render()
        # Render the possible answers.
        answers = map(lambda expr: str(expr.render()), answers)

        # Take out the correct answer.
        correct_answer = answers.pop(0)
        # Choose a random index.
        correct_answer_index = random.randrange(0, 3)
        # Place the correct answer in at that random index.
        answers.insert(correct_answer_index, correct_answer)

        return question, answers, correct_answer_index

    @property
    def question(self):
        """
        :returns: A `tuple` of all `self.parts` rendered and ready
                   to be sent.
        """

        # Only generate if they have not been generated before.
        if not hasattr(self, '_question'):
            self._question = map(self._make_part, self.parts)

        return self._question

    def ask(self):
        """
        :returns: The whole question to be asked with data.
        """
        return dict(
            data=self.data,
            question=self.question
        )

    def answer(self, request_data):
        """
        Answer the question.

        :param request_data: A dictionary containing the loaded
                             data from JSON inside the request.

        :returns: The total score and results for the question.
        """
        if self.answered:
            raise ValueError

        # Get the answer data.
        answer = request_data['answer']

        # Process each part.
        for i in xrange(len(self.parts)):

            correct = answer[i][0] == self._question[i][2]

            # Save result.
            self.results.append(correct)

            # If correct add 5 to the score.
            if correct:
                self.score += 5

        self.answered = True
        return self.score, self.results


class ModulusProductQuestion(MultipleChoiceQuestion):
    """
    Question for the modulus's product.
    """
    def __init__(self, *args, **kwargs):
        # Variables used to represent questions.
        self.z_var = MathsVariable('z')
        self.w_var = MathsVariable('w')
        self.zw_var = MathsExpression([
                self.z_var,
                self.w_var
            ],
            operators.multiply
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
        self.zw = compute_product(self.z, self.w)

        # Required `MultipleChoiceQuestion` instance varibles.
        self.data = dict(z=self.z.render(), w=self.w.render())
        self.parts = [self.part_one, self.part_two, self.part_three]

        # Call the inherited class's __init__
        super(ModulusProductQuestion, self).__init__(*args, **kwargs)

    @property
    def part_one(self):
        """
        Part one of the question. What is 'zw'?
        """

        # The answers are placed in a functions
        # to clearly separate the logic from the question.

        def answers():

            # Compute vars for random number generation.
            # For both the real part...
            step_re = int(self.zw.re * 0.1)
            if step_re < 1:
                step_re = 1
            start_re = int(self.zw.re - step_re*10)
            end_re = int(self.zw.re + step_re*10)

            # ....and imaginary part.
            step_im = int(self.zw.im * 0.1)
            if step_im < 1:
                step_im = 1
            start_im = int(self.zw.im - step_im*10)
            end_im = int(self.zw.im + step_im*10)

            # Generate wrong answers.
            wrong_answers = [
                MathsComplexNumber(
                    MathsRandomConstant(start_re, end_re, step_re),
                    MathsRandomConstant(start_im, end_im, step_im)
                ) for _ in xrange(2)
            ]

            return [self.zw] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_one'):
            # question = 'zw'
            question = self.zw_var

            self._part_one = question, answers()
        
        return self._part_one

    @property
    def part_two(self):
        """
        Part two of the question. What is '|zw|'?
        """

        # The question and answers are placed in different functions
        # to clearly separate the logic for each.

        def answers():
            zw_mod = compute_modulus(self.zw)

            # Remove the square root.
            zw_mod_squared = zw_mod.operands[0]

            # Compute vars for random number generation.
            step = int(zw_mod_squared.render() * 0.1)
            if step < 1:
                step = 1
            start = int(zw_mod_squared.render() - step*10)
            end = int(zw_mod_squared.render() + step*10)

            # Generate random numbers.
            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    operators.sqrt
                ) for _ in xrange(2)
            ]

            return [zw_mod] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_two'):
            # question = '|zw|'
            question = MathsExpression(
                self.zw_var,
                operators.abs
            )

            self._part_two = question, answers()

        return self._part_two

    @property
    def part_three(self):
        """
        Part three of the question. What is '|z||w|'?

        NOTE: There is a pattern here that the user might detect,
              and solve this question quicker. Basically the
              answer to this is the same as `self.part_two` because
              |zw| = |z||w|. It is down to the quiz object to
              detect this, then the `self.pattern` method can be
              used.
        """

        # The question and answers are placed in different functions
        # to clearly separate the logic for each.

        def question():
            # |z|
            z_mod_var = MathsExpression([
                    MathsVariable('z'),
                ], operators.abs
            )
            # |w|
            w_mod_var = MathsExpression([
                    MathsVariable('w'),
                ], operators.abs
            )

            # |z||w|
            return MathsExpression([
                    z_mod_var, w_mod_var
                ], operators.multiply
            )

        def answers():
            # |a + bj| = sqrt(a*a + b*b)
            z_mod = compute_modulus(self.z)
            w_mod = compute_modulus(self.w)

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
                operators.sqrt
            )

            # Compute vars for random numbers.
            step = int(z_mod_squared_w_mod_squared.render() * 0.1)
            if step < 1:
                step = 1
            start = int(z_mod_squared_w_mod_squared.render() - step*10)
            end = int(z_mod_squared_w_mod_squared.render() + step*10)

            # Generate wrong answers.
            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    operators.sqrt
                ) for _ in xrange(2)
            ]

            return [z_mod_w_mod] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_three'):
            self._part_three = question(), answers()

        return self._part_three

    def pattern(self, user_answer=None):
        """
        Ask about the pattern in the question.

        :param user_answer: The user's answer.

        :returns: Possible answers or, if `user_answer` is provided,
                   whether the user is correct.
        """
        # Helper function
        equal = lambda exp1, exp2: '{} = {}'.format(exp1.render(),
                                                    exp2.render())

        # A few algebraic expressions.
        z_mod_var = MathsExpression(self.z_var, operators.abs)
        w_mod_var = MathsExpression(self.w_var, operators.abs)
        z_mod_w_mod_var = MathsExpression([
            z_mod_var,
            w_mod_var
        ])
        zw_mod_var = MathsExpression(self.zw_var, operators.abs)

        # The possible answers
        correct_answer = equal(zw_mod_var, z_mod_w_mod_var)
        incorrect_answer_one = equal(z_mod_var, w_mod_var)
        incorrect_answer_two = equal(z_mod_var, zw_mod_var)

        # If answering the question return the result.
        if user_answer is not None:
            return correct_answer == user_answer

        # Shuffle answers.
        answers = [
            correct_answer,
            incorrect_answer_one,
            incorrect_answer_two
        ]
        random.shuffle(answers)

        return answers


class ModulusDivisionQuestion(MultipleChoiceQuestion):
    """
    Question for division with the modulus.
    """
    def __init__(self, *args, **kwargs):
        # Variables used to represent questions.
        self.z_var = MathsVariable('z')
        self.w_var = MathsVariable('w')
        self.z_div_w_var = MathsExpression([
                self.z_var,
                self.w_var
            ],
            operators.divide
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
        self.z_div_w = compute_divide(self.z, self.w)

        # Required `MultipleChoiceQuestion` instance varibles.
        self.data = dict(z=self.z.render(), w=self.w.render())
        self.parts = [self.part_one, self.part_two, self.part_three]

        # Call the inherited class's __init__
        super(ModulusDivisionQuestion, self).__init__(*args, **kwargs)

    @property
    def part_one(self):
        """
        Part one of the question. What is 'z / w'?
        """

        # The answers are placed in a functions
        # to clearly separate the logic from the question.

        def answers():

            # Compute vars for random number generation.
            # For both the real part...
            step_re = int(self.z_div_w.re)
            if step_re < 1:
                step_re = 1
            start_re = int(self.z_div_w.re - step_re*10)
            end_re = int(self.z_div_w.re + step_re*10)

            # ....and imaginary part.
            step_im = int(self.z_div_w.im)
            if step_im < 1:
                step_im = 1
            start_im = int(self.z_div_w.im - step_im*10)
            end_im = int(self.z_div_w.im + step_im*10)

            # Generate wrong answers.
            wrong_answers = [
                MathsComplexNumber(
                    MathsRandomConstant(start_re, end_re, step_re),
                    MathsRandomConstant(start_im, end_im, step_im)
                ) for _ in xrange(2)
            ]

            return [self.z_div_w] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_one'):
            # question = 'z / w'
            question = self.z_div_w_var

            self._part_one = question, answers()

        return self._part_one

    @property
    def part_two(self):
        """
        Part two of the question. What is '|z / w|'?
        """

        # The question and answers are placed in different functions
        # to clearly separate the logic for each.

        def answers():
            z_div_w_mod = compute_modulus(self.z_div_w)

            # Remove the square root.
            z_div_w_mod_squared = z_div_w_mod.operands[0]

            # Compute vars for random number generation.
            step = int(z_div_w_mod_squared.render())
            if step < 1:
                step = 1
            start = int(z_div_w_mod_squared.render() - step*10)
            end = int(z_div_w_mod_squared.render() + step*10)

            # Generate random numbers.
            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    operators.sqrt
                ) for _ in xrange(2)
            ]

            return [z_div_w_mod] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_two'):
            # question = '|zw|'
            question = MathsExpression(
                self.z_div_w_var,
                operators.abs
            )

            self._part_two = question, answers()

        return self._part_two

    @property
    def part_three(self):
        """
        Part three of the question. What is '|z| / |w|'?

        NOTE: There is a pattern here that the user might detect,
              and solve this question quicker. Basically the
              answer to this is the same as `self.part_two` because
              |z/w| = |z|/|w|. It is down to the quiz object to
              detect this, then the `self.pattern` method can be
              used.
        """

        # The question and answers are placed in different functions
        # to clearly separate the logic for each.

        def question():
            # |z|
            z_mod_var = MathsExpression([
                    MathsVariable('z'),
                ], operators.abs
            )
            # |w|
            w_mod_var = MathsExpression([
                    MathsVariable('w'),
                ], operators.abs
            )

            # |z| / |w|
            return MathsExpression([
                    z_mod_var, w_mod_var
                ], operators.divide
            )

        def answers():
            correct = self.part_two[1][0]
            correct_squared = correct.operands[0]

            # Compute vars for random numbers.
            step = int(correct_squared.render())
            if step < 1:
                step = 1
            start = int(correct_squared.render() - step*10)
            end = int(correct_squared.render() + step*10)

            # Generate wrong answers.
            wrong_answers = [
                MathsExpression(
                    MathsRandomConstant(start, end, step),
                    operators.sqrt
                ) for _ in xrange(2)
            ]

            return [correct] + wrong_answers

        # Only compute once as the same contents must be returned
        # for the same question instance.
        if not hasattr(self, '_part_three'):
            self._part_three = question(), answers()

        return self._part_three

    def pattern(self, user_answer=None):
        """
        Ask about the pattern in the question.

        :param user_answer: The user's answer.

        :returns: Possible answers or, if `user_answer` is provided,
                   whether the user is correct.
        """
        # Helper function
        equal = lambda exp1, exp2: '{} = {}'.format(exp1.render(),
                                                    exp2.render())

        # A few algebraic expressions.
        z_mod_var = MathsExpression(self.z_var, operators.abs)
        w_mod_var = MathsExpression(self.w_var, operators.abs)
        z_mod_div_w_mod_var = MathsExpression([
            z_mod_var,
            w_mod_var
        ], operators.divide)
        z_div_w_mod_var = MathsExpression(self.z_div_w_var, operators.abs)

        # The possible answers
        correct_answer = equal(z_div_w_mod_var, z_mod_div_w_mod_var)
        incorrect_answer_one = equal(z_mod_var, w_mod_var)
        incorrect_answer_two = equal(z_mod_var, z_div_w_mod_var)

        # If answering the question return the result.
        if user_answer is not None:
            return correct_answer == user_answer

        # Shuffle answers.
        answers = [
            correct_answer,
            incorrect_answer_one,
            incorrect_answer_two
        ]
        random.shuffle(answers)

        return answers


class PatternState(object):
    """
    Enum like object for representing the state of patterns being
    spotted.
    """

    not_spotted, spotted, confirmed = range(3)


class Quiz(BaseQuiz):
    """
    The Modulus Quiz.

    Contents:
        ModulusProductQuestion * 3,
        ModulusDivisionQuestion * 3

    """
    def __init__(self):
        self.questions = [
            (ModulusProductQuestion, 3),
            (ModulusDivisionQuestion, 3)
        ]
        self.repeat_limit = 0
        self.repeat_count = 0
        self.score = 0
        self.prev_resp_time = None
        self.pattern = PatternState.not_spotted
        super(Quiz, self).__init__()

    def next(self, json=None):
        """
        Handle request to '/the_modulus/_next'.
        """
        if self.pattern == PatternState.not_spotted and\
           self.question is None:
            return self.finish()

        # Separate GET and POST requests.
        return {
            'GET': self.get_question,
            'POST': self.answer_question,
        }[request.method](json)

    @property
    def question(self):
        # Check if there is still a question loaded that has not been
        # answered.
        if hasattr(self, '_question'):
            if not self._question.answered or self.pattern != PatternState.not_spotted:
                return self._question

        # Check if the current question type is finished or needs to
        # be repeated.
        if not hasattr(self, '_Question') or self.repeat_count >= self.repeat_limit:

            if len(self.questions) == 0:
                # Finished!
                return None

            # Go to next question type.
            self.repeat_count = 0
            self.prev_resp_time = None
            self.pattern = PatternState.not_spotted
            self._Question, self.repeat_limit = self.questions.pop(0)

        # Create new instance of `self._Question` at `self._question`
        self.repeat_count += 1
        self._question = self._Question()
        return self._question

    def get_question(self, _=None):
        """
        Handle: GET /the_modulus/_next
        """

        # As error message says below.
        if self.pattern != PatternState.not_spotted:
            raise BadRequestError(
                "Can't get more questions until the pattern has " +
                "been processed."
            )

        response = self.question.ask()
        response['finish'] = False
        return response

    def answer_question(self, json):
        """
        Handle: POST /the_modulus/_next
        """

        # Data is needed when answering a question.
        if json is None:
            BadRequestError("No data!")

        # When a pattern is spotted.
        if self.pattern != PatternState.not_spotted:

            # If the users says they know the pattern.
            if self.pattern == PatternState.confirmed:

                # If correct they get all the remaining points plus
                # an additional 5.
                score = 5 + (
                    (self.repeat_limit - self.repeat_count) *
                    len(self.question.parts) * 5
                )

                if 'answer' not in json:
                    raise BadRequestError('Expected answer.')

                # If correct they get the points.
                if self._question.pattern(json['answer']):
                    self.score += score

                # Else they loose all remaining points.

                # Either way, go to the next question.
                self.pattern = PatternState.not_spotted
                self.repeat_count = self.repeat_limit

                return dict(score=self.score)

            # Only other option is they are confirming whether or
            # not they know the pattern.
            if json.get('spotted', False):
                # If they say they know the pattern, return the
                # pattern question.
                self.pattern = PatternState.confirmed
                return dict(patterns=self.question.pattern())

            # So they don't yet know the pattern.
            self.pattern = PatternState.not_spotted
            return {}

        # A question must be being answered. If not, something has
        # gone wrong.
        if 'answer' not in json:
            raise BadRequestError('Expected answer.')

        # Answer question.
        score, results = self.question.answer(json)
        self.score += score

        # A pattern may have been spotted if the response time is
        # less than the previous.
        resp_time = json['answer'][-1][1]
        if self.prev_resp_time is not None and results[-1]:
            if resp_time < self.prev_resp_time:
                self.pattern = PatternState.spotted

        # Save previous response time to last question if correct.
        self.prev_resp_time = resp_time if results[-1] else None

        return dict(
            score=self.score,
            spotted=self.pattern
        )

    def finish(self, name=None):
        """
        Finish quiz, save scores
        """
        self.ended = True
        if name is None:
            return dict(finish=True)

        return (self.score, name)



