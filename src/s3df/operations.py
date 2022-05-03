import textwrap

from .primitives import Shape
from .snippets import INDENT
from .utils import to_vec


class Operation:
    """Base class for all operations"""

    GLSL_NAME = None

    def __init__(self, *shapes: Shape):
        self.shapes = shapes

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(str(s) for s in self.shapes)})"

    def __repr__(self):
        if self.GLSL_NAME:
            shapes = [textwrap.indent(repr(s), INDENT) for s in self.shapes]
            shapes = ", \n".join(shapes)
            return f"{self.GLSL_NAME}(\n{shapes}\n)"
        return NotImplementedError(
            f"Method __repr__ not implemented or `GLSL_NAME` not set."
        )


class Union(Operation):
    GLSL_NAME = "opUnion"


class Subtraction(Operation):
    GLSL_NAME = "opSubtraction"


class Intersection(Operation):
    GLSL_NAME = "opIntersection"


class Translate(Operation):
    def __init__(self, direction, *shapes):
        self.direction = direction
        super().__init__(*shapes)

    def __str__(self):
        return f"{self.__class__.__name__}(direction={self.direction}, shape={self.shapes[0]})"

    def __repr__(self):
        self.shapes[0].modify(f"%(p)s - {to_vec(self.direction)}")
        return repr(self.shapes[0])


class Repeat(Operation):
    GLSL_NAME = "opRep"

    def __init__(self, direction, *shapes):
        self.direction = direction
        super().__init__(*shapes)

    def __str__(self):
        return f"{self.__class__.__name__}(direction={self.direction}, shape={self.shapes[0]})"

    def __repr__(self):
        self.shapes[0].modify(f"{self.GLSL_NAME}(%(p)s, {to_vec(self.direction)})")
        return repr(self.shapes[0])


class Tx(Operation):
    GLSL_NAME = "opTx"
