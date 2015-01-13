
import collections

from . import DEFAULT_FORMAT, operators
from .operands import MathsOperand


class MathsExpression(MathsOperand):
    """
    Represent maths expressions.
    """
    def __init__(self, operands, operator=operators.multiply, **kwargs):
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
            **kwargs
        )

    def render(self, **kwargs):
        return self.operator[DEFAULT_FORMAT](
            *self.operands, **kwargs
        ).render(**kwargs)
