from modularyze import ConfBuilder

from . import primitives, operations, snippets


def get_types(shader, types=None):
    types = types or set()

    if type(shader) is list:
        for s in shader:
            types |= get_types(s, types)
    elif isinstance(shader, operations.Operation):
        for s in shader.shapes:
            types |= get_types(s, types)
        return types | {shader.__class__.__name__}
    elif isinstance(shader, primitives.Shape):
        return types | {shader.__class__.__name__}
    return types

def compile_file(path):
    builder = ConfBuilder()
    builder.register_multi_constructors(**{"!primitives": primitives, "!operations": operations})
    shader = builder.build(path)

    snips = [getattr(snippets, f"{t.upper()}_SNIPPET") for t in sorted(get_types(shader))]
    shader = shader[0] if len(shader) == 1 else operations.Union(*shader)

    return "\n\n".join(snips) + "\n\n" + repr(shader)
