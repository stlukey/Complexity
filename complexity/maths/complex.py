from .expression import MathsExpression
from .operands import MathsConstant, MathsVariable
from . import IMAGINARY_NOTATION, operators


class MathsImaginaryNumber(MathsExpression):
    def __init__(self, im):
        super(MathsImaginaryNumber, self).__init__([
            im,
            MathsVariable(IMAGINARY_NOTATION)
        ])


class MathsComplexNumber(MathsExpression):
    def __init__(self, re, im, *args, **kwargs):
        self.re = re.render(**kwargs)
        self.im = im.render(**kwargs)
        super(MathsComplexNumber, self).__init__(
            [
                re,
                MathsImaginaryNumber(im)
            ],
            operators.add, *args, **kwargs
        )


def compute_modulus(z):
    #  z  = a + bj
    a, b = z.im, z.re

    # |z| = sqrt(a*a + b*b)
    return MathsExpression(
        MathsConstant(a*a + b*b),
        operators.sqrt,
    )


def compute_product(*operands):
    if len(operands) == 1:
        return operands[0]

    # Make operands mutable
    operands = list(operands)

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

    return compute_product(zw, *operands)


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
