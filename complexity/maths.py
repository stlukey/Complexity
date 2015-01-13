#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: math.py
    ~~~~~~~~~~~~~~~~~~~
    
    Classes used to represent math expressions.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from random import Random

import collections

IMAGINARY_NOTATION = 'j'
DEFAULT_FORMAT = 'LaTeX'


class BODMAS(object):
    (
        brackets, order, division, multiplication,
        addition, subtraction
    ) = range(6)

make_brackets = lambda s: '({})'.format(s)


class MathsOperand(object):
    def __init__(self, value=None, order=None, **kwargs):
        self._value = value
        self._order = order

    @property
    def enclosed(self):
        return self._order == BODMAS.brackets

    def requires_brackets(self, order, explicit=True):
        if self.enclosed:
            return False 

        if self._order is None:
            return not explicit

        return self._order > order

    def render(self, **kwargs):
        return self._value

    def render_auto_brackets(self, order, **kwargs):
        rendered = self.render(**kwargs)

        if self.requires_brackets(order):
            rendered = make_brackets(rendered)

        return str(rendered)


class MathsConstant(MathsOperand):
    def __init__(self, value):
        super(MathsConstant, self).__init__(
            value,
            order=None,
        )


class MathsRandomConstant(MathsConstant):
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
    def __init__(self, value):
        super(MathsVariable, self).__init__(
            value,
            order=BODMAS.brackets
        )


class MathsOperator(object):
    """
    Class for math operators.
    """

    @classmethod
    def new(cls, order):
        def dec(func):
            return cls(order, **{DEFAULT_FORMAT: func})
        return dec
   
    @classmethod
    def auto_new(cls, order, delimiter):
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
        format_ = kwargs.get('format_', DEFAULT_FORMAT)

        return self.__getitem__(format_)(*operands)

    def __getitem__(self, format_):
        return self._formats[format_]

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__


class OPERATORS(object):
    """
    A collection of static MathsOperator instances.
    """

    add = MathsOperator.auto_new(BODMAS.addition, ' + ')
    subtract = MathsOperator.auto_new(BODMAS.addition, ' - ')

    @MathsOperator.new(BODMAS.multiplication)
    def multiply(*operands, **kwargs):
        explicit = []
        implicit = []
        for operand in operands:
            if operand.requires_brackets(
                BODMAS.multiplication, False
            ):
                if not operand.requires_brackets(
                    BODMAS.multiplication
                ):
                    explicit.append(
                        str(operand.render(**kwargs))
                    )
                else:
                    implicit.append(
                        make_brackets(operand.render(**kwargs))
                    )
            else:
                implicit.append(str(operand.render(**kwargs)))

        explicit = ' \\times '.join(explicit)
        implicit = ''.join(implicit)

        if len(implicit) and len(explicit):
            explicit = make_brackets(explicit)

        return MathsOperand(
            explicit + implicit,
            BODMAS.multiplication,
            **kwargs
        )

    @MathsOperator.new(BODMAS.division)
    def divide(*operands, **kwargs):
        if len(operands) == 2:
            value = '\\frac{{ {} }}{{ {} }}'.format(*[
                str(operand.render(**kwargs))
                for operand in operands
            ])
        else:
            value = ' \\ '.join([
                operand.render_auto_brackets(
                    BODMAS.division, **kwargs
                )
                for operand in operands
            ])

        return MathsOperand(
            value,
            BODMAS.division,
            **kwargs
        )

    @MathsOperator.new(BODMAS.brackets)
    def abs(operand, **kwargs):
        return MathsOperand(
            '\\left|{} \\right|'.format(operand.render(**kwargs)),
            BODMAS.brackets,
            **kwargs
        )

    @MathsOperator.new(BODMAS.brackets)
    def sqrt(operand, **kwargs):
        return MathsOperand(
            '\sqrt{{ {} }}'.format(operand.render(**kwargs)),
            BODMAS.brackets,
            **kwargs
        )

class MathsExpression(MathsOperand):
    """
    Represent maths expressions.
    """
    def __init__(self, operands, operator=OPERATORS.multiply, *args, **kwargs):
        if isinstance(operands, MathsOperand):
            operands = [operands]
        
        if not isinstance(operands, list):
            if not isinstance(operands, collections.Iterable):
                raise ValueError
            operands = list(operands)

        if not len(operands):
            raise ValueError

        self.operands = operands
        self.operator = operator

        super(MathsExpression, self).__init__(
            order=operator.order,
            *args, **kwargs
        )

    def render(self, **kwargs):
        if self.operator == OPERATORS.multiply:
            if len(self.operands) == 1:
                return self.operands[0].render(**kwargs)

        return self.operator[DEFAULT_FORMAT](
            *self.operands, **kwargs
        ).render(**kwargs)


class MathsImaginaryNumber(MathsExpression):
    def __init__(self, im, *args, **kwargs):
        super(MathsImaginaryNumber, self).__init__([
                im,
                MathsVariable(IMAGINARY_NOTATION)
            ],
            *args, **kwargs
        )


class MathsComplexNumber(MathsExpression):
    def __init__(self, re, im, *args, **kwargs):
        self.re = re.render(**kwargs)
        self.im = im.render(**kwargs)
        super(MathsComplexNumber, self).__init__([
                re,
                MathsImaginaryNumber(im)
            ],
            OPERATORS.add, *args, **kwargs
        )

    def compute_modulus(z):
        #  z  = a + bj
        a, b = z.im, z.re

        # |z| = sqrt(a*a + b*b)
        return MathsExpression(
            MathsConstant(a*a + b*b),
            OPERATORS.sqrt,
        )

    def compute_product(self, *others):
        if len(others) == 0:
            return self

        # Make others mutable 
        others = list(others)

        z, w = self, others.pop(0)

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
        
        return zw.compute_product(*others)
    
    def compute_divide(z, w):
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

