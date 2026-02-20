from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, math

# Constants
g = 9.81
dt = 0.02
k_d = 0.05   # drag coefficient
k_m = 0.02   # Magnus coefficient

# Initial velocity
vx, vy, vz = 15, 15, 5

# Spin vector (backspin = spin around x-axis, pointing left-right)
omega = (0, 0, 50)  # rad/s

# Physics parameters
g = 9.81
dt = 0.02
t = 0.0

# Initial position
x, y, z = 0.0, 1.0, 0.0

# Initial velocity (shoot at 45° in x-y plane, with z component too)
speed = 15.0
angle_xy = math.radians(45)   # horizontal angle
angle_up = math.radians(30)   # elevation angle

vx = speed * math.cos(angle_up) * math.cos(angle_xy)
vy = speed * math.sin(angle_up)
vz = speed * math.cos(angle_up) * math.sin(angle_xy)

# Window size
width, height = 800, 600

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.9, 0.9, 0.9, 1.0)

    # Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

def display():
    global x, y, z, vx, vy, vz, t

    # Physics update
    v = [vx, vy, vz]
    speed = math.sqrt(vx**2 + vy**2 + vz**2)

    # Drag
    Fd = [-k_d * speed * vx,
          -k_d * speed * vy,
          -k_d * speed * vz]

    # Magnus (backspin)
    Fm = [k_m * (omega[1]*vz - omega[2]*vy),
          k_m * (omega[2]*vx - omega[0]*vz),
          k_m * (omega[0]*vy - omega[1]*vx)]

    # Accelerations
    ax = Fd[0] + Fm[0]
    ay = Fd[1] + Fm[1] - g
    az = Fd[2] + Fm[2]

    # Integrate
    vx += ax * dt
    vy += ay * dt
    vz += az * dt
    x += vx * dt
    y += vy * dt
    z += vz * dt

    if y < 0:  # stop at ground
        y = 0

    # --- OpenGL draw ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width/height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(15, 10, 25, 0, 0, 0, 0, 1, 0)

    # Ground
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    glNormal3f(0,1,0)
    glVertex3f(-50, 0, -50)
    glVertex3f( 50, 0, -50)
    glVertex3f( 50, 0,  50)
    glVertex3f(-50, 0,  50)
    glEnd()

    # Ball
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.6, 0.1, 0.1)
    glutSolidSphere(0.5, 30, 30)

    # Draw two thin lines around the circumference of the ball
    glColor3f(1.0, 0.0, 0.0)  # Red lines
    glLineWidth(0.7)
    for z_offset in [-0.05, 0.05]:  # Two lines, slightly above and below center
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2 * math.pi * i / 100
            x_circ = 0.5 * math.cos(theta)
            y_circ = 0.5 * math.sin(theta)
            glVertex3f(x_circ, y_circ, z_offset)
        glEnd()

    glPopMatrix()

    glutSwapBuffers()


def timer(value):
    glutPostRedisplay()
    glutTimerFunc(int(dt*1000), timer, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"3D Projectile Motion - OpenGL")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
