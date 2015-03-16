#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: maths/complex.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Classes and functions used to represent and operate on
    complex numbers.

"""

from .expression import MathsExpression
from .operands import MathsConstant, MathsVariable
from . import IMAGINARY_NOTATION, operators


class MathsImaginaryNumber(MathsExpression):
    """
    Represents an imaginary number.

    It inherits from `MathsExpression` because for the imaginary
    number "8j" it represents the expression:

        MathsConstant(8) * MathsVariable('j')


    :param im: A `MathsOperator` (or child class) object for the
               imaginary part.
    """
    def __init__(self, im):
        super(MathsImaginaryNumber, self).__init__([
            im,
            MathsVariable(IMAGINARY_NOTATION)
        ])


class MathsComplexNumber(MathsExpression):
    """
    Represents a Complex number.

    It inherits from `MathsExpression` because for the complex
    number "2 + 8j" it represents the expression:

        MathsConstant(2) + (MathsConstant(8) * MathsVariable('j'))


    :param re: A `MathsOperator` (or child class) object for the
               real part.

    :param im: A `MathsOperator` (or child class) object for the
               imaginary part.

    :param kwargs: Options for rendering.
    """
    def __init__(self, re, im, **kwargs):
        self.re = re.render(**kwargs)
        self.im = im.render(**kwargs)
        super(MathsComplexNumber, self).__init__(
            [
                re,
                MathsImaginaryNumber(im)
            ],
            operators.add
        )


def compute_modulus(z):
    """
    Compute modulus of `z`.

    :param z: A MathsComplexNumber object.
    :return: |z| in terms of MathsExpression square root.
    """
    #  z  = a + bj
    a, b = z.re, z.im

    # |z| = sqrt(a*a + b*b)
    return MathsExpression(
        MathsConstant(a*a + b*b),
        operators.sqrt,
    )


def compute_product(*operands):
    """
    Compute product of complex numbers in `operands`.

    :param operands: MathComplexNumber objects to be multiplied.
    :return: MathsComplexNumber object of `operands` product.
    """

    # If there's only one operand, all have been multiplied so
    # return.
    if len(operands) == 1:
        return operands[0]

    # Make operands mutable. Before it was a tuple.
    operands = list(operands)

    # Pop `z` and `w` out the beginning of the list.
    z, w = operands.pop(0), operands.pop(0)

    # z  = a + bj
    # w  = c + dj
    a, b = z.re, z.im
    c, d = w.re, w.im

    # zw = (a + bj)(c + dj)
    #    = (ac - bd) + (ad + cb)j
    zw = MathsComplexNumber(
        MathsConstant(a*c - b*d),
        MathsConstant(a*d + c*b)
    )

    # Recursion occurs here.
    return compute_product(zw, *operands)


def compute_divide(z, w):
    """
    Compute `z` divided by `w`.

    :param z: MathsComplexNumber object to be divided.
    :param w: MathsComplexNumber object to divide by.
    :return: MathsComplexNumber object of `z` divided by `w`.
    """
    # z  = a + bj
    # w  = c + dj
    a, b = z.re, z.im
    c, d = w.re, w.im

    # z   a + bj   c - dj
    # - = ------ * ------
    # w   c + dj   c - dj
    #
    #     (ac + bd) + (cb - ad)j
    #   = ----------------------
    #         c*c + d*d

    divisor = c*c + d*d
    return MathsComplexNumber(
        MathsConstant((a*c + b*d) / divisor),
        MathsConstant((c*b - a*d) / divisor)
    )
