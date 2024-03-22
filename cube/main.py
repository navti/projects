import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *


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
        glfwSetWindowCloseCallback(self.window, self.quit)

    def run(self):
        """ main loop """
        while not self._g_quit:
            self.poll_input()
            self.pre_draw()
            self.draw()
            glfw.swap_buffers(self.window)
        self.quit(self.window)

    def quit(self, window):
        glfw.destroy_window(window)
        glfw.terminate()

    def poll_input(self):
        if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            self._g_quit = True
        glfw.poll_events()

    def pre_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self):
        pass

if __name__ == "__main__":
    app = App()
    app.run()