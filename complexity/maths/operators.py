#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: maths/operators.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Class used to represent maths operators.

"""

from . import DEFAULT_FORMAT, make_brackets
from .operands import MathsOperand, BODMAS


class MathsOperator(object):
    """
    Class for math operators.

    :param order: The order (BODMAS value).
    :param formats: functions named by format for rendering.
    """

    @classmethod
    def new(cls, order):
        """
        Creates a decorator to be used on functions for operands with
        only the `DEFAULT_FORMAT`.

        :param order: The order (BODMAS value).
        :return: The decorator.
        """
        def dec(func):
            """
            Created MathsOperator instance with only
            `DEFAULT_FORMAT`.

            :param func: The function for `DEFAULT_FORMAT`.
            :return: MathsOperator instance.
            """
            return cls(order, **{DEFAULT_FORMAT: func})
        return dec

    @classmethod
    def auto_new(cls, order, delimiter):
        """
        Automatically creates function for operators which simply has
        a delimiter (e.g. + and -). Not for operators with additional
        rules like multiplication which can be implicit or explicit
        etc.

        :param order: The order (BODMAS value).
        :param delimiter: The delimiter (e.g. ' + ', or ' - ').
        :return: Instance of MathsOperator.
        """
        @cls.new(order)
        def func(*operands, **kwargs):
            return MathsOperand(
                delimiter.join([
                    operand.render_auto_brackets(order, **kwargs)
                    for operand in operands
                ]),
                order,
                **kwargs
            )
        return func

    def __init__(self, order, **formats):
        self.order = order
        self._formats = formats

    def __call__(self, *operands, **kwargs):
        """
        When called as a function the `DEFAULT_FORMAT` is used.

        :param operands: MathOperands to be operated on.
        :param kwargs: any options for rendering.
        :return: A representation of the expression in the
                  `DEFAULT_FORMAT`.
        """
        format_ = kwargs.get('format_', DEFAULT_FORMAT)

        return self.__getitem__(format_)(*operands)

    def __getitem__(self, format_):
        """
        When the instance is accessed by: instance_name[format]
        it runs this function. This function returns the operators
        function for `format_`.

        :param format_: Chosen format.
        :return: Function for this operator that given the operands
                 renders the expression.
        """
        return self._formats[format_]


@MathsOperator.new(BODMAS.multiplication)
def multiply(*operands, **kwargs):
    """
    Renders multiplication expressions into the `DEFAULT_FORMAT`.

    :param operands: The operands.
    :param kwargs: Render options.
    :return: Rendered expression in MathsOperand to keep order data.
    """
    explicit = []
    implicit = []
    for operand in operands:
        # Does it need a bracket if multiplied implicitly?
        if operand.requires_brackets(
            BODMAS.multiplication, False
        ):
            # What about explicitly?
            if not operand.requires_brackets(
                BODMAS.multiplication
            ):
                # Add it to `explicit` then.
                explicit.append(
                    str(operand.render(**kwargs))
                )
            else:
                # Only add brackets when we have to.
                # Unfortunately we have to here.
                implicit.append(
                    make_brackets(operand.render(**kwargs))
                )
        else:
            # Add it to `implicit` then.
            implicit.append(str(operand.render(**kwargs)))

    # Join explicit list into string delimited by multiplication.
    explicit_out = r' \times '.join(explicit)
    # If it is implicit, no delimiters are needed.
    implicit_out = ''.join(implicit)

    # Only add brackets if implicit values exist (e.g. for
    # '(2 * 3 * 4)a' but not for '2 * 3 * 4') and only when there's
    # more than one explict value (e.g. for '(2*3)a' but not '2a').
    if len(implicit) and len(explicit) > 1:
        explicit_out = make_brackets(explicit_out)

    return MathsOperand(
        explicit_out + implicit_out,
        BODMAS.multiplication
    )

@MathsOperator.new(BODMAS.division)
def divide(*operands, **kwargs):
    """
    Renders division expressions into the `DEFAULT_FORMAT`.

    :param operands: The operands.
    :param kwargs: Render options.
    :return: Rendered expression in MathsOperand to keep order data.
    """
    # If there are only two operands, treat them as a fraction.
    if len(operands) == 2:
        value = '\\frac{{ {} }}{{ {} }}'.format(*[
            str(operand.render(**kwargs))
            for operand in operands
        ])
    # Else just join them with a delimiter
    else:
        value = r' \div '.join([
            operand.render_auto_brackets(
                BODMAS.division, **kwargs
            )
            for operand in operands
        ])

    return MathsOperand(
        value,
        BODMAS.division,
    )

@MathsOperator.new(BODMAS.brackets)
def abs(operand, **kwargs):
    """
    Renders absolute value expressions into the `DEFAULT_FORMAT`.

    :param operand: The operand.
    :param kwargs: Render options.
    :return: Rendered expression in MathsOperand to keep order data.
    """
    # Simply add | either side and treat as brackets.
    return MathsOperand(
        '\\left|{} \\right|'.format(operand.render(**kwargs)),
        BODMAS.brackets,
    )

@MathsOperator.new(BODMAS.brackets)
def sqrt(operand, **kwargs):
    """
    Renders square root expressions into the `DEFAULT_FORMAT`.

    :param operand: The operand.
    :param kwargs: Render options.
    :return: Rendered expression in MathsOperand to keep order data.
    """
    # Simply add square root symbol and treat as brackets.
    return MathsOperand(
        '\\sqrt{{ {} }}'.format(operand.render(**kwargs)),
        BODMAS.brackets,
    )

# Simple operator definitions. They equate to the same as above but
# can be generated automatically as there rules are simpler.
add = MathsOperator.auto_new(BODMAS.addition, ' + ')
subtract = MathsOperator.auto_new(BODMAS.subtraction, ' - ')
