import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *
from specs import *
from texture import Texture
import numpy as np
import ctypes
from camera import Camera
import pyrr
import math

cube_dir = '/'.join(__file__.split('/')[:-1])
shaders_dir = cube_dir+"/shaders"
textures_dir = cube_dir+"/textures"

from shaders.shaders import *

class App:
    """
    main app class
    :param vs_filepath: vertex shader filepath
    :param fs_filepath: fragment shader filepath
    """
    def __init__(self, vs_filepath, fs_filepath, tex_path):
        """
        App constructor, initialize flags and glfw
        """
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
        self.cubetex = Texture('cubetex', tex_path)
    
    def _init_flags(self):
        """
        initialize control flags
        """
        self._g_quit = False
        self._clear_mouse_data()

    def _gl_init(self):
        """
        openGL initialization
        """
        self._gl_clear()
        # glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def _glfw_init(self):
        """
        initialize glfw, set hints, window, callbacks
        """
        glfw.init()
        self._set_glfw_hints()
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        self._set_glfw_callbacks()
        self._gl_init()
        glfw.swap_buffers(self.window)

    def _set_glfw_hints(self):
        """
        set glfw window hints
        """
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)

    def _set_glfw_callbacks(self):
        """
        set glfw callbacks
        """
        glfwSetWindowCloseCallback(self.window, self._quit)
        glfwSetScrollCallback(self.window, self._scroll_callback)
        glfwSetMouseButtonCallback(self.window, self._mouse_button_callback)
        glfwSetCursorEnterCallback(self.window, self._cursor_enter_callback)
        glfwSetCursorPosCallback(self.window, self._cursor_pos_callback)

    def _gl_clear(self):
        """
        set viewport, clear depth and color buffers
        """
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    def _quit(self, window):
        """
        terminate app
        :param window: glfw window in context
        :returns: None
        """
        glfw.destroy_window(window)
        glfw.terminate()

    def _poll_input(self):
        """
        poll events for controls
        """
        if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            self._g_quit = True
        glfw.poll_events()

    def _draw(self):
        """
        opengGL bind vertex array, draw elements
        """
        glBindVertexArray(self.vertex_array)
        # glDrawArrays(GL_TRIANGLES, 0, 8)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.idx_buffer)
        glDrawElements(GL_TRIANGLE_STRIP,
                       self.indices.size,
                       GL_UNSIGNED_INT,
                       ctypes.c_void_p())

    def _vertex_specification(self):
        """
        set vertex specifications
        """
        # read cube specification
        positions, colors, texture_coords = get_cube_spec()
        self.attrib_buffer[0] = positions
        self.attrib_buffer[1] = colors
        self.attrib_buffer[2] = texture_coords
        # generate vertex array object
        self.vertex_array = glGenVertexArrays(1)
        # bind vertex array object
        glBindVertexArray(self.vertex_array)

        for attrib_id, buffer_data in self.attrib_buffer.items():
            self._set_buffer(attrib_id, buffer_data)
        
        # index buffer
        self.indices = np.array([0,1,4,5,6,1,2,0,3,4,7,6,3,2], dtype=np.uint32)
        # generate index buffer
        self.idx_buffer = glGenBuffers(1)
        # bind index buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.idx_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     self.indices.nbytes,
                     self.indices,
                     GL_STATIC_DRAW)
        # cleanup
        glBindVertexArray(0)

    def _set_buffer(self, attrib_idx, data):
        """
        set attribute buffers
        generate buffers, bind and enable vertex attrib array
        :param attrib_idx: attribute index
        :param data: attribute data, like vertex positions, colors etc.
        :returns: None
        """
        size = 4 if attrib_idx < 2 else 2
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
        """
        create shader program and set GL to use it.
        """
        self._shader_program = create_shader_program(self.vertex_shader_filepath,
                                                     self.fragment_shader_filepath)
        glUseProgram(self._shader_program)
        self._set_texture()

    def _set_texture(self):
        self.cubetex.load_texture()
        # using GL_TEXTURE0, hence that 0 as last param
        glUniform1i(glGetUniformLocation(self._shader_program, "imageTexture"), 0)

    # mouse events related callbacks
    def _mouse_button_callback(self, window, button, action, mods):
        """
        mouse button press callback function
        The params are passed to the callback funcion from the os
        :param window: glfw window in context
        :param button: mouse button on which an event occurs
        :param action: the action, press or release
        :param mods: any modifier keys pressed with mouse button
        """
        if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
            self._mouse_left_press = True
        elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
            self._mouse_left_press = False
        # cache cursor positions for using with camera controls
        self._cursor_x, self._cursor_y = glfwGetCursorPos(window)

    def _cursor_pos_callback(self, window, xpos, ypos):
        """
        callback function when cursor position changes
        :param window: glfw window in context
        :param xpos: current x position of cursor
        :param ypos: current y position of cursor
        :returns: None
        """
        if self._mouse_left_press:
            # calculate offsets
            x_offset = self._cursor_x - xpos
            y_offset = self._cursor_y - ypos
            # store new positions
            self._cursor_x = xpos
            self._cursor_y = ypos
            # update rotate transforms
            self.camera.rotate(x_offset, y_offset)
            # print(f"xpos: {x_offset}, ypos: {y_offset}")

    def _clear_mouse_data(self):
        """
        utility function to clear mouse related data
        """
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
        """
        set model, view and projection transforms for the shader program to read
        """
        # populate 'model' variable with model transform data used by shader program
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "model"),
            1,
            GL_FALSE,
            self.model_transform
        )

        # populate 'view' variable with view transform data used by shader program
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "view"),
            1,
            GL_FALSE,
            self.view_transform
        )

        # populate 'projection' variable with projection transform data used by shader program
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, "projection"),
            1,
            GL_FALSE,
            self.projection_transform
        )

    def run(self):
        """
        run app
        """
        self._vertex_specification()
        self._create_graphics_pipeline()
        self.camera = Camera()
        angle = 0
        """ main loop """
        while not self._g_quit:
            self._poll_input()
            self._gl_clear()
            # set translate and scale
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
    tex_path = textures_dir+"/cubemaps.png"
    # tex_path = textures_dir+"/tex.jpg"
    app = App(vertex_shader_filepath, fragment_shader_filepath, tex_path)
    app.run()