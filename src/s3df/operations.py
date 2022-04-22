import typing
from primitives import Shape


class Operation:
    """Base class for all operations"""
    def __init__(self, *shapes: typing.List[Shape]):
        self.shapes = shapes

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Subclass should implement this!")

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(self.shapes)})"


class Union(Operation):
    def __repr__(self):
        return f"opUnion({self.shapes})"


class Intersection(Operation):
    def __call__(self, *args, **kwargs):
        pass
