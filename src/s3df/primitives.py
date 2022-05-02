from .utils import to_vec


class Shape:
    """Base class for all primitives"""


class Cube(Shape):
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdBox(p - {to_vec(self.position)}, {to_vec(self.size, size=3)})"

    def __str__(self):
        return f"Cube(position=({self.position}), size={self.size})"
