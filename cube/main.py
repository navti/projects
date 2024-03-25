import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *
from specs import *
import numpy as np
import ctypes
import sys

# add to path variable so module can be found
cube_dir = '/'.join(__file__.split('/')[:-1])
shaders_dir = cube_dir+"/shaders"
# sys.path.append(cube_dir)
# sys.path.append(shaders_dir)

from shaders.shaders import *


class App:
    def __init__(self, vs_filepath, fs_filepath):
        self.vertex_shader_filepath = vs_filepath
        self.fragment_shader_filepath = fs_filepath
        self._g_quit = False
        self._shader_program = None
        self.vertex_array = None
        self._glfw_init()
    
    def _gl_clear(self):
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT)
        # glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    def _glfw_init(self):
        glfw.init()
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        glfwSetWindowCloseCallback(self.window, self._quit)
        self._gl_clear()
        glfw.swap_buffers(self.window)

    def _quit(self, window):
        glfw.destroy_window(window)
        glfw.terminate()

    def _poll_input(self):
        if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            self._g_quit = True
        glfw.poll_events()

    def _draw(self):
        glBindVertexArray(self.vertex_array)
        glDrawArrays(GL_LINE_LOOP, 0, 8)

    def _vertex_specification(self):
        positions, colors = get_cube_spec()

        self.vertex_array = glGenVertexArrays(1)
        glBindVertexArray(self.vertex_array)

        # Attribute 0 - position buffer
        attribute_index_0 = 0
        size = 4
        stride = 0 # or 4*4 = 16
        offset = 0
        
        position_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
        glBufferData(GL_ARRAY_BUFFER,
                     positions.nbytes,
                     positions,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(attribute_index_0,
                              size,
                              GL_FLOAT,
                              GL_FALSE,
                              stride,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(attribute_index_0)

        # Attribute 1 - color buffer
        attribute_index_1 = 1
        size = 4
        stride = 0 # or 4*4 = 16
        offset = 0
        
        color_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
        glBufferData(GL_ARRAY_BUFFER,
                     colors.nbytes,
                     colors,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(attribute_index_1,
                              size,
                              GL_FLOAT,
                              GL_FALSE,
                              stride,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(attribute_index_1)
        
        # cleanup
        glBindVertexArray(0)
        glDisableVertexAttribArray(attribute_index_0)
        glDisableVertexAttribArray(attribute_index_1)

    def _create_graphics_pipeline(self):
        self._shader_program = create_shader_program(self.vertex_shader_filepath,
                                                     self.fragment_shader_filepath)
        glUseProgram(self._shader_program)

    def run(self):
        self._vertex_specification()
        self._create_graphics_pipeline()
        """ main loop """
        while not self._g_quit:
            self._poll_input()
            self._gl_clear()
            self._draw()
            glfw.swap_buffers(self.window)
        self._quit(self.window)

if __name__ == "__main__":
    vertex_shader_filepath = shaders_dir+"/vertex_shader.txt"
    fragment_shader_filepath = shaders_dir+"/fragment_shader.txt"
    app = App(vertex_shader_filepath, fragment_shader_filepath)
    app.run()