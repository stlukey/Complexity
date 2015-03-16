#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: maths/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Represent maths expressions.

"""


IMAGINARY_NOTATION = 'j'
DEFAULT_FORMAT = 'LaTeX'

make_brackets = lambda s: '({})'.format(s)

from .operators import MathsOperator
from .expression import MathsExpression
from .operands import (MathsOperand, MathsConstant,
                       MathsRandomConstant, MathsVariable, BODMAS)
from . import operators
from .complex import MathsImaginaryNumber, MathsComplexNumber

# __all__ is what gets imported when selecting '*' with:
#     from __name__ import *

__all__ = ['MathsOperand', 'MathsOperator', 'MathsExpression',
           'MathsConstant', 'MathsRandomConstant', 'MathsVariable',
           'operators', 'MathsImaginaryNumber', 'MathsComplexNumber',
           'BODMAS']
