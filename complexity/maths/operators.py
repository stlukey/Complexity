from . import DEFAULT_FORMAT, make_brackets
from .operands import MathsOperand, BODMAS


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

    explicit_out = ' \\times '.join(explicit)
    implicit_out = ''.join(implicit)

    if len(implicit) and len(explicit) > 1:
        explicit_out = make_brackets(explicit_out)

    return MathsOperand(
        explicit_out + implicit_out,
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

add = MathsOperator.auto_new(BODMAS.addition, ' + ')
subtract = MathsOperator.auto_new(BODMAS.subtraction, ' - ')
