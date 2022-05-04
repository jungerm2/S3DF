import textwrap
from functools import reduce

import numpy as np
from scipy.spatial.transform import Rotation as R

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

    def __repr__(self):
        if len(self.shapes) == 2:
            return super().__repr__()
        multi_union = reduce(Union, reversed(self.shapes))
        return repr(multi_union)


class Subtraction(Operation):
    GLSL_NAME = "opSubtraction"


class Intersection(Operation):
    GLSL_NAME = "opIntersection"


class Translate(Operation):
    def __init__(self, direction, *shapes):
        self.direction = direction
        super().__init__(*shapes)
        self.modify = self.shapes[0].modify

    def __str__(self):
        return f"{self.__class__.__name__}(direction={self.direction}, shape={self.shapes[0]})"

    def __repr__(self):
        self.modify(f"%(p)s - {to_vec(self.direction)}")
        # self.shapes[0].modify(f"invert({t})*%(p)s")
        return repr(self.shapes[0])


class Repeat(Operation):
    GLSL_NAME = "opRep"

    def __init__(self, direction, *shapes):
        self.direction = direction
        super().__init__(*shapes)
        self.modify = self.shapes[0].modify

    def __str__(self):
        return f"{self.__class__.__name__}(direction={self.direction}, shape={self.shapes[0]})"

    def __repr__(self):
        self.modify(f"{self.GLSL_NAME}(%(p)s, {to_vec(self.direction)})")
        return repr(self.shapes[0])


class Rotate(Operation):
    def __init__(self, matrix, *shapes):
        self.matrix = matrix
        super().__init__(*shapes)
        self.modify = self.shapes[0].modify

    def __str__(self):
        return f"{self.__class__.__name__}(matrix={self.matrix}, shape={self.shapes[0]})"

    def __repr__(self):
        row_major = "mat3(" + ",\n".join(to_vec(row, size=3) for row in self.matrix) + ")"
        column_major = f"transpose({row_major})"
        self.modify(f"inverse({column_major})*(%(p)s)")
        return repr(self.shapes[0])


class RotateVec(Rotate):
    def __init__(self, vec, angle, *shapes):
        vec = np.array(vec) / np.linalg.norm(vec)
        angle = np.deg2rad(angle)
        matrix = R.from_rotvec(angle * vec).as_matrix().tolist()
        super().__init__(matrix, *shapes)


class RotateX(RotateVec):
    def __init__(self, angle, *shapes):
        super().__init__([1, 0, 0], angle, *shapes)


class RotateY(RotateVec):
    def __init__(self, angle, *shapes):
        super().__init__([0, 1, 0], angle, *shapes)


class RotateZ(RotateVec):
    def __init__(self, angle, *shapes):
        super().__init__([0, 0, 1], angle, *shapes)
