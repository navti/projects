import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *
from specs import *
import numpy as np
import ctypes

class App:
    def __init__(self):
        self._glfw_init()
        self._gl_init()
        self._g_quit = False

    def _gl_init(self):
        glClearColor(0,0,0,1)

    def _glfw_init(self):
        glfw.init()
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        glfwSetWindowCloseCallback(self.window, self._quit)
    
    def _quit(self, window):
        glfw.destroy_window(window)
        glfw.terminate()

    def _poll_input(self):
        if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            self._g_quit = True
        glfw.poll_events()

    def _pre_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def _draw(self):
        pass

    def _vertex_specification(self):
        positions, colors = get_cube_spec()

        vertex_array = glGenVertexArrays(1)
        glBindVertexArray(vertex_array)

        # Attribute 0 - position buffer
        attribute_index = 0
        size = 4
        stride = 0 # or 4*4 = 16
        offset = 0
        
        position_buffer = glGenBuffers(1)
        glBindBuffer(position_buffer)
        glBufferData(GL_ARRAY_BUFFER,
                     positions.nbytes,
                     positions,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(attribute_index,
                              size,
                              GL_FLOAT,
                              GL_FALSE,
                              stride,
                              ctypes.c_void_p(offset))
        glEnableVertexArrayAttrib(attribute_index)

        # Attribute 1 - color buffer
        attribute_index = 1
        size = 4
        stride = 0 # or 4*4 = 16
        offset = 0
        
        color_buffer = glGenBuffers(1)
        glBindBuffer(color_buffer)
        glBufferData(GL_ARRAY_BUFFER,
                     colors.nbytes,
                     colors,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(attribute_index,
                              size,
                              GL_FLOAT,
                              GL_FALSE,
                              stride,
                              ctypes.c_void_p(offset))
        glEnableVertexArrayAttrib(attribute_index)
        

    def run(self):
        """ main loop """
        while not self._g_quit:
            self._poll_input()
            self._pre_draw()
            self._draw()
            glfw.swap_buffers(self.window)
        self._quit(self.window)

if __name__ == "__main__":
    app = App()
    app.run()