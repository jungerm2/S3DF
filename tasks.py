import sys
from pathlib import Path

from invoke import task

from s3df import compile_file, render_from_path


@task
def compile_yaml(
    c, path, template_path="template_with_camera.glsl", save_as=None, show=True
):
    path = str(Path(path).resolve())
    code = compile_file(path, template_path=template_path, save_as=save_as)
    if show:
        print(code)


@task
def render_glsl(c, path):
    sys.argv = sys.argv[:1]
    path = str(Path(path).resolve())
    render_from_path(path)


@task
def compile_and_render(
    c, path, template_path="template_with_camera.glsl", save_as="tmp.glsl"
):
    compile_yaml(c, path, template_path=template_path, save_as=save_as)
    render_glsl(c, save_as)
