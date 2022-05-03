from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from modularyze import ConfBuilder

from . import operations, primitives, snippets


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


def compile_file(path, template_path="template.glsl", save_as=None):
    builder = ConfBuilder()
    builder.register_multi_constructors(
        **{"!primitives": primitives, "!operations": operations}
    )
    path = Path(path)
    shader = builder.build(str(path))

    if isinstance(shader, list):
        shader = shader[0] if len(shader) == 1 else operations.Union(*shader)
    elif isinstance(shader, dict) and "scene" in shader:
        shader = shader["scene"][0] if len(shader["scene"]) == 1 else operations.Union(*shader["scene"])
    else:
        raise ValueError("Format not understood!")

    snips = [
        getattr(snippets, f"{t.upper()}_SNIPPET") for t in sorted(get_types(shader))
    ]

    env = Environment(
        loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
        autoescape=select_autoescape(),
    )
    template = env.get_template(str(template_path))
    code = template.render(
        snippets="\n\n".join(snips),
        main_shader=repr(shader),
    )

    save_as = save_as or str(path.parent / f"{path.stem}.glsl")
    with open(save_as, "w") as f:
        f.write(code)

    return code
