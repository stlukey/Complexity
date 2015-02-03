#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: tests/test_maths.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from complexity.maths import *
from complexity.maths.complex import (compute_modulus,
                                      compute_product,
                                      compute_divide)

def test_operand_constant():
    """
    Test MathsConstant object.
    """
    for i in xrange(100):
        a = MathsConstant(i)
        assert a.render() == i

def test_operand_random_constant():
    """
    Test MathsRandomConstant object.
    """
    a = MathsRandomConstant(0, 9)
    assert a.render() in xrange(9)

def test_operand_variable():
    """
    Test MathsVariable object.
    """
    a = MathsVariable('a')
    assert a.render() == 'a'

def test_operator_multiply():
    """
    Test the multiply operator.
    """
    a = MathsRandomConstant(1, 10)
    b = MathsRandomConstant(1, 10)
    
    x = MathsVariable('x')
    y = MathsVariable('y')
    
    # Explicit multiplication.
    ab = MathsExpression([a, b]).render()
    ab_expected = '{} \\times {}'.format(a.render(), b.render())
    assert ab == ab_expected

    # Implicit multiplication.
    xy = MathsExpression([x, y]).render()
    assert xy == 'xy' 

    # Implicit multiplication, with a single constant.
    for n in [a, b]:
        nxy = MathsExpression([n, x, y]).render()
        nxy_expected = '{}xy'.format(n.render())
        assert nxy == nxy_expected

    # Implicit and explicit muliplication.
    abxy = MathsExpression([a, b, x, y]).render()
    abxy_expected = '({} \\times {})xy'.format(
        a.render(),
        b.render()
    )
    assert abxy == abxy_expected

def test_operator_divide():
    """
    Test the divide operator.
    """
    a = MathsRandomConstant(1, 10)
    b = MathsRandomConstant(1, 10)
    
    x = MathsVariable('x')
    y = MathsVariable('y')
    
    # Constant divided by constant.
    a_div_b = MathsExpression([a, b], operators.divide).render()
    a_div_b_expected =\
            '\\frac{{ {} }}{{ {} }}'.format(a.render(), b.render())
    assert a_div_b == a_div_b_expected
    
    # Constant divided by variable.
    a_div_x = MathsExpression([a, x], operators.divide).render()
    a_div_x_expected = '\\frac{{ {} }}{{ x }}'.format(a.render())
    assert a_div_x == a_div_x_expected

    # Variable divided by variable.
    x_div_y = MathsExpression([x, y], operators.divide).render()
    x_div_y_expected = r'\frac{ x }{ y }'
    assert x_div_y == x_div_y_expected

    # Variable divided by constant.
    y_div_b = MathsExpression([y, b], operators.divide).render()
    y_div_b_expected = '\\frac{{ y }}{{ {} }}'.format(b.render())
    assert y_div_b == y_div_b_expected

    # Multiple Operands.
    abxy_div = MathsExpression([a, b, x, y], operators.divide).render()
    abxy_div_expected = r' \div '.join(
        map(lambda n: str(n.render()), [a, b, x, y])
    )
    assert abxy_div == abxy_div_expected

def test_operator_abs():
    """
    Test the absolute value operator.
    """
    for i in xrange(100):
        a = MathsExpression(MathsConstant(i), operators.abs)
        assert a.render() == '\\left|{} \\right|'.format(i)

def test_operator_sqrt():
    """
    Test the square root operator.
    """
    for i in xrange(100):
        a = MathsExpression(MathsConstant(i), operators.sqrt)
        assert a.render() == '\\sqrt{{ {} }}'.format(i)

def test_operator_add():
    """
    Test the add operator.
    """
    nums = map(str, xrange(50))
    nums_maths_constant = map(MathsConstant, nums)
    exp = MathsExpression(nums_maths_constant, operators.add)
    assert exp.render() == ' + '.join(nums)

def test_operator_subtract():
    """
    Test the substract operator.
    """
    nums = map(str, xrange(50))
    nums_maths_constant = map(MathsConstant, nums)
    exp = MathsExpression(nums_maths_constant, operators.subtract)
    assert exp.render() == ' - '.join(nums)

def test_imaginary_number():
    """
    Test MathsImaginaryNumber object.
    """
    for i in xrange(100):
        a = MathsImaginaryNumber(
            MathsConstant(i)
        )

        assert a.render() == '{}j'.format(i)

def test_complex_number(a=None, b=None):
    """
    Test MathsComplexNumber object.
    """
    if a is None or b is None:
        for a in xrange(100):
            for b in xrange(100):
                test_complex_number(a, b)
        return

    z = MathsComplexNumber(
        MathsConstant(a),
        MathsConstant(b)
    )

    assert z.render() == '{} + {}j'.format(a, b)

def test_compute_modulus(a=None, b=None):
    """
    Test the compute_modulus function.
    """
    if a is None or b is None:
        for a in xrange(100):
            for b in xrange(100):
                test_compute_modulus(a, b)
        return

    z = MathsComplexNumber(
        MathsConstant(a),
        MathsConstant(b)
    )
    
    modulus = compute_modulus(z).render()
    expected = '\\sqrt{{ {} }}'.format(z.im**2 + z.re**2)
    assert modulus == expected 

def test_compute_product():
    """
    Test the compute_product function.
    """

    a = MathsConstant(3)
    b = MathsConstant(3)
    c = MathsConstant(2)
    d = MathsConstant(1)

    z = MathsComplexNumber(a, b)
    w = MathsComplexNumber(c, d)

    zw = compute_product(z, w).render()
    assert zw ==  '3 + 9j'

def test_compute_divide():
    """
    Test the compute_divide function.
    """

    a = MathsConstant(3)
    b = MathsConstant(2)
    c = MathsConstant(1)
    d = MathsConstant(-2)

    z = MathsComplexNumber(a, b)
    w = MathsComplexNumber(c, d)

    z_div_w = compute_divide(z, w).render()
    assert z_div_w ==  '-0.2 + 1.6j'
    


