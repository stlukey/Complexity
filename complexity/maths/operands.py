
from random import Random

from . import make_brackets


class BODMAS(object):
    (
        brackets, order, division, multiplication,
        addition, subtraction
    ) = range(6)


class MathsOperand(object):
    def __init__(self, value=None, order=None):
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
            value=value,
            order=None
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
