from invoke import task

from s3df import compile_file


@task
def render(c, path):
    code = compile_file(path)
    print(code)
