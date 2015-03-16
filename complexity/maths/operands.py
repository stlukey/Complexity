#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: maths/operands.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Class used to represent maths operands.

"""


from random import Random

from . import make_brackets


class BODMAS(object):
    """
    Simple enum like object for representing the order of operations.
    """
    (
        brackets, order, division, multiplication,
        addition, subtraction
    ) = range(6)


class MathsOperand(object):
    """
    Represents operands in MathExpressions.

    :param value: The value of the operand.
    :param order: The order of operations for the operand.
    """

    def __init__(self, value=None, order=None):
        self._value = value
        self._order = order

    @property
    def enclosed(self):
        """
        :returns: True if enclosed in brackets.
        """
        return self._order == BODMAS.brackets

    def requires_brackets(self, order, explicit=True):
        """
        Detect if operand needs brackets when used in an expression
        with `order`.

        :param order: The order (BODMAS value) used by the
                       expression.

        :param explicit: Used in the case of multiplication to
                          distinguish between '5x' and '5 * x'.

        :returns: Boolean of if the operand needs brackets when used
                  in an expression of `order`.
        """
        # If it already has brackets it does not need more.
        if self.enclosed:
            return False

        # If it's a constant it needs brackets if used explicitly.
        # e.g. '(3)(3)' not '33'
        if self._order is None:
            return not explicit

        # Else it just depends if the new order is less.
        return self._order > order

    def render(self, **kwargs):
        """
        :param kwargs: for inheritance.
        :returns: `value`
        """
        return self._value

    def render_auto_brackets(self, order, **kwargs):
        """
        Combines `render` and `requires_brackets for convenience
        but does not allow for implicit operations as they require
        irregular rules.
        """
        rendered = self.render(**kwargs)

        # Add brackets if needed.
        if self.requires_brackets(order):
            rendered = make_brackets(rendered)

        return str(rendered)


class MathsConstant(MathsOperand):
    """
    Represents constants.
    """
    def __init__(self, value):
        super(MathsConstant, self).__init__(
            value=value,
            order=None
        )


class MathsRandomConstant(MathsConstant):
    """
    Represents constants that are required to be random.
    """
    def __init__(self, start, end, step=1):
        self._start = start
        self._end = end
        self._step = step
        self._render = None

        super(MathsRandomConstant, self).__init__(
            value=None
        )

    def reset(self):
        self._render = None

    def render(self, **kwargs):
        if hasattr(self, '_render') and self._render is not None:
            return self._render

        random = kwargs.get('random')

        if random is None:
            random = Random()

        self._render = random.randrange(
            self._start, self._end, self._step
        )
        return self._render


class MathsVariable(MathsOperand):
    """
    Represents varibles.
    """
    def __init__(self, value):
        super(MathsVariable, self).__init__(
            value,
            order=BODMAS.brackets
        )
