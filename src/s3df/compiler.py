import primitives
import operations
from modularyze import ConfBuilder

builder = ConfBuilder()
builder.register_constructors_from_modules(primitives, operations)
shader = builder.build("cube.yaml")

code = shader()
