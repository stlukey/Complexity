#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: maths/expression.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Class used to represent maths expressions.

"""

import collections

from . import DEFAULT_FORMAT, operators
from .operands import MathsOperand


class MathsExpression(MathsOperand):
    """
    Represent maths expressions.

    :ivar operator: The expressions MathsOperator.
    :ivar operands: A list of (or children of) MathsOperand objects.


    :param operands: Either an iterable type (e.g. a list)
                     containing, or a single, MathOperand
                     (or child class of MathOperand) object(s).

    :param operator: A Maths Operator Object.
    """

    def __init__(self, operands, operator=operators.multiply):
        # If its a single instance turn it into a list.
        if isinstance(operands, MathsOperand):
            operands = [operands]

        # If it's not a list it must at least be iterable.
        if not isinstance(operands, list):
            if not isinstance(operands, collections.Iterable):
                raise ValueError
            # Turn into list.
            operands = list(operands)

        # There needs to be at least one operator.
        if len(operands) < 1:
            raise ValueError

        self.operands = operands
        self.operator = operator

        super(MathsExpression, self).__init__(
            order=operator.order
        )

    def render(self, **kwargs):
        """
        Render the MathExpression object into the `DEFAULT_FORMAT`.

        :param kwargs: Any options to be passed for other,
                        MathsOperands. (e.g. seeds for
                        MathsRandomConstant)
        :return: `DEFAULT_FORMAT` representation of the expression.
        """
        # Recursion can occur here as the `render` method is called
        # for each operand which may contain another
        # `MathsExpression`.
        return self.operator[DEFAULT_FORMAT](
            *self.operands, **kwargs
        ).render(**kwargs)
