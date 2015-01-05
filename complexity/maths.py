#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: math.py
    ~~~~~~~~~~~~~~~~~~~
    
    Classes used to represent math expressions.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

# Prefixed with underscore as it should only be used internally.
# Elsewhere, the operators in `OPERATORS` should be used. 
import operator as _operator

# Same here too.
from random import Random as _Random

import math

import collections

IMAGINARY_NOTATION = 'j'
DEFAULT_FORMAT='LaTeX'

class BODMAS(object):
    (
        brackets, order, division, multiplication,
        addition, subtraction
    ) = range(6)

make_brackets = lambda s: '({})'.format(s)

class MathsOperand(object):
    def __init__(self, value=None, order=None, seed=None):
        self._value = value
        self._order = order

    @property
    def enclosed(self):
        return self._order == BODMAS.brackets

    def requies_brackets(self, order, explicit=True):
        if self.enclosed:
            return False 

        if self._order is None:
            return not explicit

        return self._order > order

    def render(self, **kwargs):
        return self._value

    def render_auto_brackets(self, order, *args, **kwargs):
        rendered = self.render(*args, **kwargs)

        if self.requies_brackets(order):
            rendered = make_brackets(rendered)

        return str(rendered)

class MathsConstant(MathsOperand):
    def __init__(self, value):
        return super(MathsConstant, self).__init__(
            value,
            order=None,
        )

class MathRandomConstant(MathsConstant):
    def __init__(self, start, end, step=1):
        self._start = start
        self._end = end
        self._step = step

        return super(MathsRandomConstant, self).__init__(
            value=None,
            order=None,
        )

    def render(self, *args, **kwargs):
        if random is None:
            if seed is None:
                raise ValueError
            random = _Random(seed)

        return random.randrange(self._start, self._end, self._step)

class MathsVariable(MathsOperand):
    def __init__(self, value):
        return super(MathsVariable, self).__init__(
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
            return cls(order, **{DEFAULT_FORMAT:func})
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
                seed=kwargs.get('seed')
            )
        return func

    def __init__(self, order, **formats):
        self.order = order
        self._formats = formats

    def __call__(self, *operands, **kwargs):
        format_ = kwargs.get('format_', DEFAULT_FORMAT)

        return self.__getatt__(format_)(*operands)

    def __getitem__(self, format_):
        return self._formats[format_]

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class OPERATORS:
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
            if operand.requies_brackets(BODMAS.multiplication, False):
                if not operand.requies_brackets(BODMAS.multiplication):
                    explicit.append(str(operand.render(**kwargs)))
                else:
                    implicit.append(make_brackets(operand.render(**kwargs)))
            else:
                implicit.append(str(operand.render(**kwargs)))

        explicit = ' \\times '.join(explicit)
        implicit = ''.join(implicit)

        if len(implicit) and len(explicit):
            explcit = make_brackets(explicit)

        return MathsOperand(
            explicit + implicit,
            BODMAS.multiplication,
            seed=kwargs.get('seed'),
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
                operand.render_auto_brackets(order, **kwargs)
                    for operand in operands
            ])

        return MathsOperand(
            value,
            BODMAS.division,
            seed=kwargs.get('seed')
        )

    @MathsOperator.new(BODMAS.brackets)
    def abs(operand, **kwargs):
        return MathsOperand(
            '\\left|{} \\right|'.format(operand.render(**kwargs)),
            BODMAS.brackets,
            seed=kwargs.get('seed')
        )

class MathsExpression(MathsOperand):
    """
    Represent maths expressions.
    """
    def __init__(self, operands, operator=OPERATORS.multiply, *args, **kwargs):
        if not isinstance(operands, list):
            if not isinstance(operands, collections.Iterable):
                raise ValueError
            operands = list(operands)

        if not len(operands):
            raise ValueError

        self._operands = operands
        self._operator = operator

        return super(MathsExpression, self).__init__(
            order=operator.order,
            *args, **kwargs
        )

    def render(self, **kwargs):
        if kwargs.get('render') == None:
            kwargs['random'] = _Random(kwargs.get('seed'))
        
        if self._operator == OPERATORS.multiply:
            if len(self._operands) == 1:
                return self._operands[0].render(**kwargs)

        return self._operator[DEFAULT_FORMAT](
            *self._operands, **kwargs
        ).render(**kwargs)

class MathsImaginaryNumber(MathsExpression):
    def __init__(self, im, *args, **kwargs):
        return super(MathsImaginaryNumber, self).__init__([
                im,
                MathsVariable(IMAGINARY_NOTATION)
            ],
            *args, **kwargs
        )

class MathsComplexNumber(MathsExpression):
    def __init__(self, re, im, *args, **kwargs):
        self.re = re.render(**kwargs)
        self.im = im.render(**kwargs)
        return super(MathsComplexNumber, self).__init__([
                re,
                MathsImaginaryNumber(im)
            ],
            OPERATORS.add, *args, **kwargs
        )
        return

    @classmethod
    def compute_modulus(cls, z):
        if not isinstance(z, cls):
            raise NotImplemented

        #  z  = a + bj
        a, b = z.im, z.re

        # |z| = sqrt(a*a + b*b)
        return MathsConstant(math.sqrt(a*a + b*b))

    @classmethod
    def compute_product(cls, *operands, **kwargs):
        if not kwargs.get('type_checked', False):
            for operand in operands:
                if not isinstance(operand, cls):
                    raise NotImplemented

        if not len(operands):
            raise TypeError

        if len(operands) == 1:
            return operands[9]

        z, w = operands.pop(0), operands.pop(0)

        # z  = a + bj
        # w  = c + dj
        a, b = z.re, z.im
        c, d = w.re, w.im

        # zw = (a + bj)(c + dj)
        #    = (ac - bd) + (ad + cb)j
        zw = cls(
                a*c - b*d,
                a*d + c*b
        )
        
        return zw if not len(operands) else complex_multiply(
            zw, *operands, type_checked=True
        )
    
    @classmethod
    def compute_divide(cls, z, w):
        if not isinstance(cls, z) or not isinstance(cls, w):
            raise NotImplemented

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
                (a*c + b*d) / divisor,
                (c*b - a*d) / divisor
        )

