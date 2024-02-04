import math
import pyglet
from pyglet.gl import *
from pyglet.window import key
from primitives import *

# Create a window object
window = pyglet.window.Window(800, 600, "Snake3D")
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

glClearColor(0,0,0,1)
glEnable(GL_DEPTH_TEST)

helv_font=pyglet.font.load("Helvetica", 14)
fps_display = pyglet.clock.ClockDisplay(helv_font, color=(1, 0, 0, 0.3))

fov = 40
INCREMENT = 5
x_rot = 5
y_rot = 5

# Register on_draw function
@window.event
def on_draw():
    # Clear the current GL Window
    window.clear()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    for c in cubes:
        glPushMatrix()
        glTranslatef(*c.i3)
        glBegin(GL_QUADS)
        c.draw()
        glEnd()
        glPopMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(1,1,1)
    glLineWidth(2)
    glBegin(GL_QUADS)
    world_box.draw()
    glEnd()

    glPointSize(2)
    glColor3f(1,1,1)
    glBegin(GL_POINTS)
    for l in points:
        glVertex3f(*l)
    glEnd()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect_ratio = width / height
    gluPerspective(fov, aspect_ratio, 1, 2000)

    return pyglet.event.EVENT_HANDLED


@window.event
def on_text_motion(motion):
    global x_rot,y_rot

    if motion == key.UP:
        x_rot -= INCREMENT
    elif motion == key.DOWN:
        x_rot += INCREMENT
    elif motion == key.LEFT:
        y_rot -= INCREMENT
    elif motion == key.RIGHT:
        y_rot += INCREMENT


## Register a function for the on_text event
pos = [0,0,-400]
rot = [0,0,0]
MOVE = 5

def do_view_state():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rot[0], 1, 0, 0)
    glRotatef(rot[1], 0, 1, 0)
    glTranslatef(*pos)


def move_facing(dist):
    horiz_ang = math.radians(-rot[1])
    xh = math.sin(horiz_ang) * dist
    zh = math.cos(horiz_ang) * dist

    vert_ang = math.radians(rot[0])
    yv = math.sin(vert_ang) * dist

    pos[0] += xh
    pos[1] += yv
    pos[2] += zh

    do_view_state()


def main_update(dt):
    global fov
    if keyboard[key.Y]:
        fov += 1
        on_resize(window.width, window.height)
    if keyboard[key.U]:
        fov -= fov > 1
        on_resize(window.width, window.height)

    if keyboard[key.SPACE]:
        move_facing(5)

    if keyboard[key.B]:
        move_facing(-5)

    if keyboard[key.W]:
        rot[0] -= 1
        do_view_state()

    if keyboard[key.S]:
        rot[0] += 1
        do_view_state()

    if keyboard[key.A]:
        rot[1] -= 1
        do_view_state()

    if keyboard[key.D]:
        rot[1] += 1
        do_view_state()



cubes = []
size = 10
numx = 6
numy = numx
xbounds = size*numx*2
ybounds = size*numy*2
spacing = size*2

for x in range(0, xbounds, spacing):
    for y in range(0, ybounds, spacing):
        cubes.append(Cube((x,y,0), size))

for z in range(0, numx*size*2, spacing):
    for y in range(0, ybounds, spacing):
        cubes.append(Cube((xbounds, y, z), size))

world_box = Cube((0,0,0), 800)
world_box.colors = ((0.7,0.7,0.7), (0.4, 0.4, 0.4))*6

points = []
world_grid_size = 800
step = 100
for x in range(-world_grid_size, world_grid_size, step):
    for z in range(-world_grid_size, world_grid_size, step):
        for y in range(-world_grid_size, world_grid_size, step):
            points.append((x,y,z))



pyglet.clock.schedule_interval(main_update, 1/60.0)
do_view_state()
pyglet.app.run()
