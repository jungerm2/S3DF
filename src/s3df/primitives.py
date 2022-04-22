class Shape:
    """Base class for all primitives"""
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Subclass should implement this!")


class Cube(Shape):
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def __call__(self, p):
        return f"sdBox(p, {float(self.size)});"

    def __str__(self):
        return f"Cube(position=({self.position}), size={self.size})"
