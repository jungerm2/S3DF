from .utils import to_vec


class Shape:
    """Base class for all primitives"""
    def __init__(self):
        self.p = "p"

    def modify(self, func):
        self.p = func % dict(p=self.p)


class Cube(Shape):
    def __init__(self, position, size):
        super().__init__()
        self.modify(f"%(p)s - {to_vec(position)}")
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdBox({self.p}, {to_vec(self.size, size=3)})"

    def __str__(self):
        return f"Cube(position=({self.position}), size={self.size})"


class Sphere(Shape):
    def __init__(self, position, size):
        super().__init__()
        self.modify(f"%(p)s - {to_vec(position)}")
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdSphere({self.p}, {self.size})"

    def __str__(self):
        return f"Sphere(position=({self.position}), size={self.size})"


class Torus(Shape):
    def __init__(self, position, size):
        super().__init__()
        self.modify(f"%(p)s - {to_vec(position)}")
        self.position = position
        self.size = size

    def __repr__(self):
        return f"sdTorus({self.p}, {to_vec(self.size, size=2)})"

    def __str__(self):
        return f"Torus(position=({self.position}), size={self.size})"


class CappedCylinder(Shape):
    def __init__(self, position, height, radius):
        super().__init__()
        self.modify(f"%(p)s - {to_vec(position)}")
        self.position = position
        self.height = height
        self.radius = radius

    def __repr__(self):
        return f"sdCappedCylinder({self.p}, {self.height}, {self.radius})"

    def __str__(self):
        return f"CappedCylinder(position=({self.position}), height={self.height}, radius={self.radius})"
