import logging
from pathlib import Path

import moderngl_window
from moderngl_window import WindowConfig, geometry, resources
from moderngl_window.finders.program import FilesystemFinder

# Register system resource directory in this package
resources.register_dir(Path(__file__).parent)


class ShaderToyWindow(WindowConfig):
    """
    Implement ShaderToy-like functionality in a GLSL window.
    Adapted from: https://github.com/einarf/shadertoy
    """

    title = "Python Shadertoy"
    resource_dir = Path(__file__).parent
    # Don't enforce a specific aspect ratio
    aspect_ratio = None
    main_program = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._error_state = False
        self._main_program_mtime = 0
        self._fallback_program = self.load_program("shaders/fallback.glsl")
        self._main_program_path = FilesystemFinder().find(Path(self.main_program))
        self._main_program = None
        self.load_main_program()
        self._quad_fs = geometry.quad_fs()
        self._mouse_pos = 0, 0
        self._mouse_scroll = 0

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)

    def render(self, time, frame_time):
        if self._error_state:
            self._quad_fs.render(self._fallback_program)
            return

        # Set standard shadertoy uniforms
        self.set_uniform("iTime", time)
        self.set_uniform("iMouse", self._mouse_pos)
        self.set_uniform("iResolution", self.wnd.buffer_size)
        self.set_uniform("iScroll", self._mouse_scroll)

        # Run the program
        self._quad_fs.render(self._main_program)

    def set_uniform(self, name, value):
        """Safely set uniform value"""
        try:
            self._main_program[name].value = value
        except (KeyError, NameError, TypeError):
            pass

    def load_main_program(self):
        try:
            new_program = self.load_program(self._main_program_path.parts[-1])
        except Exception as ex:
            self._error_state = True
            logging.error(ex)
            return

        if self._main_program:
            self._main_program.release()

        self._main_program = new_program
        self._error_state = False

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

    def mouse_drag_event(self, x, y, dx, dy):
        self._mouse_pos = x, y

    def mouse_scroll_event(self, x_offset, y_offset):
        self._mouse_scroll += y_offset


def render_from_path(path):
    class Renderer(ShaderToyWindow):
        resource_dir = Path(path).parent.resolve()
        main_program = Path(path).name

    Renderer.run()
