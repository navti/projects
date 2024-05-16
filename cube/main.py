import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *
from specs import *
import numpy as np
import ctypes
from camera import Camera
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
        self._shader_program = None
        self.vertex_array = None
        self.attrib_buffer = {}
        self.model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self.view_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._init_flags()
        self._glfw_init()
    
    def _init_flags(self):
        self._g_quit = False
        self._clear_mouse_data()

    def _gl_init(self):
        self._gl_clear()
        # glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def _glfw_init(self):
        glfw.init()
        self._set_glfw_hints()
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        self._set_glfw_callbacks()
        self._gl_init()
        glfw.swap_buffers(self.window)

    def _set_glfw_hints(self):
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)

    def _set_glfw_callbacks(self):
        glfwSetWindowCloseCallback(self.window, self._quit)
        glfwSetScrollCallback(self.window, self._scroll_callback)
        glfwSetMouseButtonCallback(self.window, self._mouse_button_callback)
        glfwSetCursorEnterCallback(self.window, self._cursor_enter_callback)
        glfwSetCursorPosCallback(self.window, self._cursor_pos_callback)

    def _gl_clear(self):
        glClearColor(0, 0, 0, 1)
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
        # self.set_transforms()

    # mouse events related callbacks
    def _mouse_button_callback(self, window, button, action, mods):
        if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
            self._mouse_left_press = True
        elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
            self._mouse_left_press = False
        self._cursor_x, self._cursor_y = glfwGetCursorPos(window)
        # print(f"x: {self._cursor_x}, y: {self._cursor_y}")

    def _cursor_pos_callback(self, window, xpos, ypos):
        if self._mouse_left_press:
            x_offset = self._cursor_x - xpos
            y_offset = self._cursor_y - ypos
            self._cursor_x = xpos
            self._cursor_y = ypos
            self.camera.rotate(x_offset, y_offset)
            print(f"xpos: {x_offset}, ypos: {y_offset}")

    def _clear_mouse_data(self):
        self._cursor_x = 0
        self._cursor_y = 0
        self._mouse_left_press = False
        self._mouse_active = False

    def _scroll_callback(self, window, x_offset, y_offset):
        """
        callback function to detect when mouse scroll wheel is activated and perform camera
        back and forward motion.
        :param window: the window object associated with the event
        :param x_offset: x offset of the scroll
        :param y_offset: y offset of the scroll
        :return: None
        """
        if self._mouse_active:
            if y_offset > 0:
                self.camera.step_forward()
            elif y_offset < 0:
                self.camera.step_back()

    def _cursor_enter_callback(self, window, entered):
        """
        detect when cursor enters or exits the window area
        :param window: window in context
        :param entered: signal True if cursor entered, False if cursor not entered
        :return: None
        """
        if entered:
            self._mouse_active = True
        else:
            self._clear_mouse_data()
            self._mouse_active = False

    def set_transforms(self):
        # glUseProgram(self._shader_program)

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
        self.camera = Camera()
        angle = 0
        """ main loop """
        while not self._g_quit:
            self._poll_input()
            self._gl_clear()
            translate_vector = [0, 0, 0]
            scale_vector = [0.5, 0.5, 0.5]
            scale = pyrr.matrix44.create_from_scale(np.array(scale_vector), dtype=np.float32)
            translate = pyrr.matrix44.create_from_translation(np.array(translate_vector), dtype=np.float32)
            rotate_y = pyrr.matrix44.create_from_y_rotation(math.radians(angle), dtype=np.float32)
            # pyrr gives matrix that should be post multiplied
            self.model_transform = scale @ translate
            # camera transform: world space -> camera space
            eye = [0, 1, 1]
            target = [0, 0, 0]
            up = [0, 1, 0]
            self.view_transform = self.camera.view_transform
            # self.view_transform = pyrr.matrix44.create_look_at(np.array(eye),
            #                                np.array(target),
            #                                np.array(up),
            #                                dtype=np.float32)
            # orthogonal projection: defines viewing prism, camera space -> NDC
            left = -1
            right = 1
            bottom = -1
            top = 1
            near = 0.5
            far = 20
            # self.projection_transform = pyrr.matrix44.create_orthogonal_projection(left, right, bottom, top, near, far, dtype=np.float32)
            # perspective projection
            fovy = 60
            aspect_ratio = 1.0
            self.projection_transform = pyrr.matrix44.create_perspective_projection(fovy, aspect_ratio, near, far, dtype=np.float32)
            # set pointers to transforms for vertex shader
            self.set_transforms()
            self._draw()
            glfw.swap_buffers(self.window)
            angle -= 1
        self._quit(self.window)

if __name__ == "__main__":
    vertex_shader_filepath = shaders_dir+"/vertex_shader.txt"
    fragment_shader_filepath = shaders_dir+"/fragment_shader.txt"
    app = App(vertex_shader_filepath, fragment_shader_filepath)
    app.run()