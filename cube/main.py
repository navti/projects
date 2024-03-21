import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from settings import *


class App:
    def __init__(self):
        glfw.init()
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "The Cube", None, None)
        glfw.make_context_current(self.window)
        glClearColor(1,1,1,1)

    def run(self):
        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
                break
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.window)

    def terminate(self):
        glfw.destroy_window(self.window)
        glfw.terminate()

if __name__ == "__main__":
    app = App()
    app.run()
    app.terminate()