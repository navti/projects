import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *
from specs import *
import numpy as np
import ctypes
import sys
import pyrr
import math

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
        self.attrib_buffer = {}
        self.model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self.view_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._glfw_init()
    
    def _gl_init(self):
        self._gl_clear()
        glEnable(GL_DEPTH_TEST)

    def _glfw_init(self):
        glfw.init()
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        glfwSetWindowCloseCallback(self.window, self._quit)
        self._gl_init()
        glfw.swap_buffers(self.window)

    def _gl_clear(self):
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    def _quit(self, window):
        glfw.destroy_window(window)
        glfw.terminate()

    def _poll_input(self):
        if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            self._g_quit = True
        glfw.poll_events()

    def _draw(self):
        glBindVertexArray(self.vertex_array)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # glDrawArrays(GL_TRIANGLES, 0, 8)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.idx_buffer)
        glDrawElements(GL_TRIANGLE_STRIP,
                       self.indices.size,
                       GL_UNSIGNED_INT,
                       ctypes.c_void_p())

    def _vertex_specification(self):
        positions, colors = get_cube_spec()
        self.attrib_buffer[0] = positions
        self.attrib_buffer[1] = colors

        self.vertex_array = glGenVertexArrays(1)
        glBindVertexArray(self.vertex_array)

        for attrib_id, buffer_data in self.attrib_buffer.items():
            self._set_buffer(attrib_id, buffer_data)
        
        # index buffer
        self.indices = np.array([0,1,4,5,6,1,2,0,3,4,7,6,3,2], dtype=np.uint32)
        self.idx_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.idx_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     self.indices.nbytes,
                     self.indices,
                     GL_STATIC_DRAW)
        # cleanup
        glBindVertexArray(0)

    def _set_buffer(self, attrib_idx, data):
        size = 4
        stride = 0 # or 4*4 = 16
        offset = 0
        
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER,
                     data.nbytes,
                     data,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(attrib_idx,
                              size,
                              GL_FLOAT,
                              GL_FALSE,
                              stride,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(attrib_idx)

    def _create_graphics_pipeline(self):
        self._shader_program = create_shader_program(self.vertex_shader_filepath,
                                                     self.fragment_shader_filepath)
        glUseProgram(self._shader_program)
        self.set_transforms()

    def set_transforms(self):
        glUseProgram(self._shader_program)

        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "model"),
            1,
            GL_FALSE,
            self.model_transform
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "view"),
            1,
            GL_FALSE,
            self.view_transform
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "projection"),
            1,
            GL_FALSE,
            self.projection_transform
        )

    def run(self):
        self._vertex_specification()
        self._create_graphics_pipeline()
        angle = 0
        """ main loop """
        while not self._g_quit:
            self._poll_input()
            self._gl_clear()
            # translate to origin
            # translate_origin = pyrr.matrix44.create_from_translation(np.array([-0.5,-0.5, 0]), dtype=np.float32)
            scale = pyrr.matrix44.create_from_scale(np.array([0.5,0.5,0.5]), dtype=np.float32)
            rotate_x_45 = pyrr.matrix44.create_from_x_rotation(math.radians(45), dtype=np.float32)
            rotate_y = pyrr.matrix44.create_from_y_rotation(math.radians(angle), dtype=np.float32)
            view_transform = pyrr.matrix44.create_look_at(np.array([0,0,0.5],dtype=np.float32),
                                                          np.array([0,0,0], dtype=np.float32),
                                                          np.array([0,1,0],dtype=np.float32),
                                                          dtype=np.float32)
            self.model_transform = rotate_y @ rotate_x_45 @ scale
            self.set_transforms()
            self._draw()
            glfw.swap_buffers(self.window)
            angle += 1
        self._quit(self.window)

if __name__ == "__main__":
    vertex_shader_filepath = shaders_dir+"/vertex_shader.txt"
    fragment_shader_filepath = shaders_dir+"/fragment_shader.txt"
    app = App(vertex_shader_filepath, fragment_shader_filepath)
    app.run()