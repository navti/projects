from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Simple window!")
    glClearColor(1,1,1,1)
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()