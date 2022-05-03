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


class Sphere(Shape):
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdSphere(p - {to_vec(self.position)}, {self.size})"

    def __str__(self):
        return f"Sphere(position=({self.position}), size={self.size})"


class Torus(Shape):
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdTorus(p - {to_vec(self.position)}, {to_vec(self.size, size=2)})"

    def __str__(self):
        return f"Cube(position=({self.position}), size={self.size})"


class CappedCylinder(Shape):
    def __init__(self, position, height, radius):
        self.position = position
        self.height = height
        self.radius = radius

    def __repr__(self):
        return f"sdCappedCylinder(p - {to_vec(self.position)}, {self.height}, {self.radius})"

    def __str__(self):
        return f"CappedCylinder(position=({self.position}), height={self.height}, radius={self.radius})"
