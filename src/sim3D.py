from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#from OpenGL.GLUT import glutLeaveMainLoop  # export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
import sys, math
from PIL import Image
import numpy as np
import imageio.v2 as imageio
from mpl_toolkits.mplot3d import Axes3D
import os
import sys, math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

# Constants which will never be varied between test cases
k_l = 0.25   # Magnus coefficient
m = 0.156    # mass of ball (kg)
#The ball, when new, shall weigh not less than 5.5 ounces/155.9 g, nor more than 5.75 ounces/163 g, 
#and shall measure not less than 8.81 in/22.4 cm, nor more than 9 in/22.9 cm in circumference.
circumference_of_ball = 0.225  # meters
diameter_of_ball = circumference_of_ball / (2*math.pi)  # meters OR diameter_of_ball = circumference_of_ball / (2*math.pi)  # meters
radius_of_ball = diameter_of_ball / 2
A = math.pi * radius_of_ball**2  # cross-sectional area of ball (m^2)

# Field and Pitch dimensions
ground_size = 140  # diameter
pitch_width = 3.05
pitch_length = 22.56  # TODO: pitch length is double what is should be - see calculations = -pitch_length instead of -pitch_length/2
pitchstart_to_bowlingcrease = 1.22
bowlingcrease_to_poppingcrease = 1.22
poppingcrease_to_otherpoppingcrease = 17.68
pitchstart_to_poppingcrease = pitchstart_to_bowlingcrease + bowlingcrease_to_poppingcrease
height_of_stumps = 0.72
diameter_of_stumps = 0.04
bowler_stumps_distance = -pitch_length/2 + pitchstart_to_bowlingcrease
batter_stumps_distance = pitch_length/2 - pitchstart_to_bowlingcrease

# Bowler dimensions
bowler_height = 1.8  # Get reference for average height of a male spin bowler = approx 1.8 metres
release_height_above_bowler_head = 0.5  # approximate height of arm above head at release
bowler_release_height = bowler_height + release_height_above_bowler_head
half_bowler_stride = 0.3  # approximate half stride length to find distance between popping crease and x position of bowler's hand
bowler_release_distance = -pitch_length/2 + pitchstart_to_poppingcrease - half_bowler_stride
bowler_preferred_distance_from_centerline = 0.3 
bowler_release_x = 0.0 + bowler_preferred_distance_from_centerline  # for right-handed bowler and batsman

# Storing positions for flight of ball
past_x_values = []
past_y_values = []
past_z_values = []

# Initial velocity
#vx, vy, vz = 0, 5, 15

# Spin vector (backspin = spin around x-axis, pointing left-right)
# assume clockwise round x (top spin rate), clockwise round y (), clockwise round z

# Physics parameters
g = 9.81
dt = 0.01
t = 0.0
max_time = 5  # seconds

# Initial position
initial_x = 0 # TODO: future possible offset in display: initial_x = -bowler_release_x  # due to display requirements
x, y, z = initial_x, bowler_release_height, bowler_release_distance  # start above ground, back from origin at popping crease
# x = along pitch, y = height, z = across pitch

completed_bounce = False  # there will be one bounce

# Window size
width, height = 800, 600
stop_simulation = False

def flight(omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z):

    # Physics update
    v = [vx, vy, vz]
    speed = math.sqrt(vx**2 + vy**2 + vz**2)

    angular_velocity = (omega[0]**2 + omega[1]**2)**0.5
    spin_rate = radius_of_ball * angular_velocity / (speed + 1e-6)  # to avoid division by zero
    c_l = k_l * spin_rate * 8 # cheat additional factor to increase visibility of curved path
    c_d = k_d  # constant depending on ball properties

    # Drag
    Fd = 0.5 * rho * speed**2 * A * c_d  # in Paper 2 & 3

    # Lift
    #Fl = 0.5 * rho * speed**2 * A * c_l  # in Paper 2 & 3
    Fl = (4/3) * 4 * math.pi * radius_of_ball**3 * rho * c_l * spin_rate*speed  # from NASA page on lift - Kutta-Joukowski theorem

    angle_of_lift_force_x = np.arccos(np.dot(np.cross(omega, v), [1,0,0]) / (np.linalg.norm(np.cross(omega, v)) * np.linalg.norm([1,0,0]) + 1e-8))  # avoid division by zero
    angle_of_lift_force_y = np.arccos(np.dot(np.cross(omega, v), [0,1,0]) / (np.linalg.norm(np.cross(omega, v)) * np.linalg.norm([0,1,0]) + 1e-8))  # avoid division by zero

    # Accelerations
    #ax = (Fl[0] * math.sin(angle_with_pos_x) - Fd[0] * math.cos(angle_with_pos_x)) / m
    #ay = (-m*g + Fl[1] * math.cos(angle_with_pos_x) - Fd[1] * math.sin(angle_with_pos_x)) / m
    #az = Fd[2] + Fl[2]  # TODO: wrong!

    # note angle on which lift acts is different
    ax = (-Fd * math.cos(angle_with_pos_x) * math.cos(angle_with_pos_z) - Fl * math.sin(angle_of_lift_force_x) * math.cos(angle_of_lift_force_y)) / m
    ay = (-m*g - Fd * math.sin(angle_with_pos_z) + Fl * math.sin(angle_of_lift_force_y)) / m
    az = (-Fd * math.sin(angle_with_pos_x) * math.cos(angle_with_pos_z) - Fl * math.cos(angle_of_lift_force_x) * math.cos(angle_of_lift_force_y)) / m


    #ax = (-Fd * math.cos(angle_with_pos_x) * math.cos(angle_with_pos_z) - Fl * math.sin(angle_with_pos_x) * math.cos(angle_with_pos_z)) / m
    #ay = (-m*g - Fd * math.sin(angle_with_pos_z) + Fl * math.sin(angle_with_pos_z)) / m
    #az = (-Fd * math.sin(angle_with_pos_x) * math.cos(angle_with_pos_z) - Fl * math.cos(angle_with_pos_x) * math.cos(angle_with_pos_z)) / m

    '''#2D model
    ax = 0
    ay = (-m*g - Fd * math.sin(angle_with_pos_z) + Fl * math.cos(angle_with_pos_z)) / m
    az = (-Fd * math.cos(angle_with_pos_z) - Fl * math.sin(angle_with_pos_z)) / m
    '''
    # only need one angle for projection onto y axis

    # Write accelerations and forces to a new file
    with open(directory_test_case_results+"/sim3D_forces.txt", "a") as f_forces:
        f_forces.write(f"{t:.3f},{ax:.5f},{ay:.5f},{az:.5f},{Fd:.5f},{Fl:.5f}\n")

    # Integrate
    vx += ax * dt
    vy += ay * dt
    vz += az * dt

    # Update angle_with_pos_x
    angle_with_pos_x = math.atan2(vz, vx) 
    angle_with_pos_z = math.atan2(vy, vz)

    return omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z

def bounce(omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z):

    friction_coefficient = 0.35  # from average in https://www.researchgate.net/publication/225873716_Predicting_the_playing_character_of_cricket_pitches
    dh = 0.1  # TODO : some small distance tbd
    k = 0.55  # TODO : find coefficient of restitution between ball and ground

    print("Bouncing...")
    
    '''bounce_dt = dt # TODO: function
    # Note this is 2D
    vx_new = vx
    vy_new = k**0.5 * vy *-1
    vz_new = np.sign(omega[0])*(friction_coefficient * (vy + vy_new) + friction_coefficient*g*bounce_dt) + (vz + radius_of_ball*omega[0])
    angle_with_pos_x = angle_with_pos_x #math.atan2(vz, vx) 
    angle_with_pos_z = math.atan2(vy, vz)'''

    e_number = 1  # perfectly_elastic
    bounce_dt = 2*e_number*math.sqrt(2*dh/g)
    # This is 3D
    omega_old = omega.copy()
    #omega = np.array(omega)*(2/7)+np.array([vz, vx])*(5/(7*radius_of_ball))  #assuming ball is solid sphere
    omega = np.array(omega)*(2/7)+np.array([vz, vy, vx])*(5/(7*radius_of_ball))  #assuming ball is solid sphere

    # TODO: is there a change in spin axis angle upon bounce? - yes compute from mag of components

    # TODO : make use of third component of spin

    vy_new = k**0.5 * vy *-1
    vx_new = abs(radius_of_ball*omega[2])
    vz_new = radius_of_ball*omega[0] #+ abs(radius_of_ball*omega[1])
    # abs for now

    angle_x_old = angle_with_pos_x
    angle_z_old = angle_with_pos_z

    angle_with_pos_x = math.atan2(vz_new, vx_new)#-math.radians(90)  # fudge factor
    angle_with_pos_z = math.atan2(vy_new, vz_new)

    print(angle_with_pos_x - angle_x_old, angle_with_pos_z - angle_z_old)

    print(omega[0] - omega_old[0], omega[1] - omega_old[1])

    return omega, vx_new, vy_new, vz_new, angle_with_pos_x, angle_with_pos_z, bounce_dt


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.7, 0.8, 0.9, 0.2)  # select blue background colour for sky

    # Lighting
    '''glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])'''
    
def display():
    global x, y, z, vx, vy, vz, angle_with_pos_x, angle_with_pos_z, omega, t
    global completed_bounce
    global past_x_values, past_y_values, past_z_values
    global radius_of_ball

    #print("In plots3D.py in main()")
    # --- Store position and time for plots ---
    with open(directory_test_case_results+"/sim3D_output.txt", "a") as f:
        f.write(f"{t:.3f},{x:.3f},{y:.3f},{z:.3f},{vx:.3f},{vy:.3f},{vz:.3f},{angle_with_pos_x:.3f},{angle_with_pos_z:.3f}\n")

    t += dt

    # TODO : bounce or not
    # TODO : bounce equations
    # TODO: how much does the ball squish? How close to ground before we apply the bounce equations?
    if z > batter_stumps_distance:
        print("Ball is in line with the batter's stumps. Stopping simulation.")
        stop_simulation = True
        plot_main()

    elif y < 0 and completed_bounce:  # stop after one bounce when it hits ground again
        print("Ball is hitting ground a second time. Stopping simulation.")
        stop_simulation = True
        plot_main() 
    
    elif t > 8 or abs(x) > pitch_width:
        print("Ball has gone too wide or taken too long to complete motion. Stopping simulation.")
        stop_simulation = True
        plot_main()

    elif y < 0+radius_of_ball and not completed_bounce:  # stop at ground - scaled up ball will look as if it is in the ground a bit more
        #y = 0+scaled_radius_of_ball

        # "Instant" bounce
        # x,y,z remain the same
        # only update directions and speeds (of spin + of ball trajectory)
        omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z, bounce_dt = bounce(omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z)
        completed_bounce = True
        t = t - dt + bounce_dt  # to correct for different dt for bounce step

        x += vx * dt
        y += vy * dt
        z += vz * dt

        display_slide(x, y, z)
        display()
    
    else:
        omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z = flight(omega, vx, vy, vz, angle_with_pos_x, angle_with_pos_z)

        x += vx * dt
        y += vy * dt
        z += vz * dt

        display_slide(x, y, z)
        display()



def display_slide(x, y, z):  # I think the display is reflected in x axis (down line of bowler's view is +x)

    scaled_radius_of_ball = 5 * radius_of_ball

    # --- OpenGL draw ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width/height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##KEY
    '''gluLookAt(0, 10, -40,   # eye position
        0, 0, 0,     # look at origin
        0, 1, 0)     # up vector'''
    if viewpoint == "diagonal":
        # Diagonal angle
        gluLookAt(15, 10, 25, 0, 0, 0, 0, 1, 0) 
    elif viewpoint == "bowler":
        # Bowler view angle
        gluLookAt(bowler_release_x, bowler_height, bowler_release_distance, 0, 0, 0, 0, 1, 0)
    elif viewpoint == "top-down":
        # From-the-sky angle
        gluLookAt(0, 50, 0, 0, 0, 0, 0, 0, -1)
    else:  #viewpoint == "sideon"
        # Side-on angle
        gluLookAt(30, 2, 0, 0, 0, 0, 0, 1, 0)
    

    # Ground
    # TODO: make this a circle
    glColor3f(0.0, 0.2, 0.0)  # select dark green colour for ground
    glBegin(GL_QUADS)
    glNormal3f(0,1,0) # normal vector pointing up - indicates orientation of ground
    glVertex3f(-ground_size, -0.01, -ground_size)
    glVertex3f( ground_size, -0.01, -ground_size)
    glVertex3f( ground_size, -0.01,  ground_size)
    glVertex3f(-ground_size, -0.01,  ground_size)
    glEnd()

    # Pitch
    # TODO: add gridlines
    glColor3f(0.667, 0.831, 0.561)  # select dark green colour for ground
    glBegin(GL_QUADS)
    glNormal3f(0,1,0) # normal vector pointing up - indicates orientation of ground
    glVertex3f(-pitch_width/2, 0, -pitch_length/2)
    glVertex3f( pitch_width/2, 0, -pitch_length/2)
    glVertex3f( pitch_width/2, 0,  pitch_length/2)
    glVertex3f(-pitch_width/2, 0,  pitch_length/2)
    glEnd()

    # Draw stumps as a cylinder
    for x_offset in [-0.05, 0, 0.05]:
        glPushMatrix()
        glColor3f(1,1,1)
        glTranslatef(x_offset, 0, bowler_stumps_distance)
        quadric = gluNewQuadric()
        gluCylinder(quadric, diameter_of_stumps / 2, diameter_of_stumps / 2, height_of_stumps, 32, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    '''# Ball coordinate finder - get bearings
    glPushMatrix()
    glTranslatef(-5, 10, 20)
    glColor3f(0,0,0)
    glutSolidSphere(scaled_radius_of_ball, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(5, 10, -20)
    glColor3f(1,1,1)
    glutSolidSphere(scaled_radius_of_ball, 10, 10)
    glPopMatrix()'''

    display_x = -x  # due to coordinate system in the simulation

    # Ball
    glPushMatrix()
    glTranslatef(display_x, y, z)
    glColor3f(0.6, 0.1, 0.1)
    glutSolidSphere(scaled_radius_of_ball, 30, 30)

    #glPopMatrix()

    # TODO : fix angle of seam lines on ball
    # Draw two thin lines around the circumference of the ball, rotated by angle_with_pos_z
    glColor3f(1.0, 0.75, 0.75)  # Red lines
    seam_offset = diameter_of_ball * 0.05
    glLineWidth(seam_offset/3) # two lines with a line-widht gap between them
    for z_offset in [-seam_offset, seam_offset]:  # Two lines, slightly above and below center
        glPushMatrix()
        # Rotate the seam lines by angle_with_pos_z about the z-axis
        glRotatef(math.degrees(angle_with_pos_z), 0, 0, 1)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2 * math.pi * i / 100
            x_circ = 0.5 * math.cos(theta)
            y_circ = 0.5 * math.sin(theta)
            glVertex3f(x_circ, y_circ, z_offset)
        glEnd()
        glPopMatrix()


    # Ball shadow on ground - assuming sun directly overhead
    glPopMatrix()
    glPushMatrix()
    glTranslatef(display_x, 0.015, z)  # slightly above ground to display over Ground and Pitch
    glColor3f(0.251, 0.322, 0.243)   # darker color for shadow
    # Draw a flat disc as the shadow
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, 0.0)  # center of disc
    num_segments = 40
    shadow_radius = scaled_radius_of_ball * 1.01  # little bit larger than ball radius
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments
        x_disc = shadow_radius * math.cos(theta)
        z_disc = shadow_radius * math.sin(theta)
        glVertex3f(x_disc, 0.0, z_disc)
    glEnd()

    glPopMatrix()

    # Flight trail
    for i, past_x in enumerate(past_x_values):
        past_y = past_y_values[i]
        past_z = past_z_values[i]
        glPushMatrix()
        glTranslatef(-past_x, past_y, past_z)
        glColor3f(0.969, 0.655, 0.792)
        glutSolidSphere(scaled_radius_of_ball*0.2, 10, 10)  # smaller spheres for trail
        glPopMatrix()

    # Store x,y,z positions for flight trail
    past_x_values.append(x)
    past_y_values.append(y)
    past_z_values.append(z)

    '''# Store images for video
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)  # image
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # flip vertically
    images.append(np.array(image))'''

    # For rendering display
    glutSwapBuffers()

def timer(value):
    global t, max_time
    if t < max_time:
        glutPostRedisplay()
        glutTimerFunc(int(dt*10), timer, 0)
    else:
        print("Simulation finished.")
        imageio.mimsave(directory_test_case_results+"/sim_"+viewpoint+".gif", images, fps=10*int(len(images)/max_time))
        print("Simulation saved.")
        plot_main()
        print("Run plot_main complete.")
        
        #from OpenGL.GLUT import glutLeaveMainLoop
        glutLeaveMainLoop()
        #sys.exit(0)
        print("After glutLeaveMainLoop attempt.")
        #next_sim(case, viewpoint)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"3D Cricket Ball Motion - OpenGL")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()
    print("end main")

def plot_main():
    # remember to get/store plot data from directory_test_case_results
    import matplotlib.pyplot as plt

    with open(directory_test_case_results+"/sim3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))  # t, x, y, z, vx, vy, vz, angle_with_pos_x, angle_with_pos_z
        for i, line in enumerate(lines):
            #print(line.strip().split(','))
            data_matrix[i] = np.array(line.strip().split(','), dtype=float)

    time_values = data_matrix[:, 0]
    x_values = data_matrix[:, 1]
    y_values = data_matrix[:, 2]
    z_values = data_matrix[:, 3]
    vx_values = data_matrix[:, 4]
    vy_values = data_matrix[:, 5]
    vz_values = data_matrix[:, 6]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_values, z_values, np.ones(len(y_values))*(0), color='grey')
    ax.plot(x_values, np.ones(len(z_values))*(30), y_values, color='grey')
    ax.plot(np.zeros(len(x_values))*(-0.3), z_values, y_values, color='grey')
    ax.plot(x_values, z_values, y_values, color='red')  # y_values represent height
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length, pitch_length) # TODO: pitch length is double what it should be - see calculations
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("3D Ball Trajectory")
    plt.savefig(directory_test_case_results+"/sim3D_trajectory_line.png")

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values, z_values, np.zeros(len(y_values)), color='grey', s=1)
    #ax.scatter(x_values, np.zeros(len(z_values)), y_values, color='grey', s=1)
    #ax.scatter(np.zeros(len(x_values)), z_values, y_values, color='grey', s=1)
    ax.scatter(x_values, z_values, y_values, color='red', s=10)  # y_values represent height, bigger dots
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("3D Ball Trajectory")
    # Set equal scale for x and z axes
    x_range = x_values.max() - x_values.min()
    z_range = z_values.max() - z_values.min()
    max_range = max(x_range, z_range)
    x_mid = (x_values.max() + x_values.min()) / 2
    z_mid = (z_values.max() + z_values.min()) / 2
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length, pitch_length) # TODO: pitch length is double what it should be - see calculations
    plt.savefig(directory_test_case_results+"/sim3D_trajectory_dots.png")

    modulo_dots = 10
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values[::modulo_dots], z_values[::modulo_dots], np.zeros(len(y_values[::modulo_dots])), color='grey', s=1)
    #ax.scatter(x_values[::modulo_dots], np.zeros(len(z_values[::modulo_dots])), y_values[::modulo_dots], color='grey', s=1)
    #ax.scatter(np.zeros(len(x_values[::modulo_dots])), z_values[::modulo_dots], y_values[::modulo_dots], color='grey', s=1)
    ax.scatter(x_values[::modulo_dots], z_values[::modulo_dots], y_values[::modulo_dots], color='red', s=10)  # y_values represent height, bigger dots
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length, pitch_length) # TODO: pitch length is double what it should be - see calculations
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_title("3D Ball Trajectory")
    ax.set_box_aspect([1, 1, 1])
    plt.savefig(directory_test_case_results+"/sim3D_trajectory_fewer_dots.png")

    print("Plots saved.")
    return
    # Fix plots and set boundaries - check with output numbers
    #sys.exit()
    
if __name__ == "__main__":
    global case
    case = int(sys.argv[1])

    if case == 0:
        print("0 is an invalid case number. Running case 1 instead.")
        case = 1

    #print("In plots3D.py running case", case)

    global viewpoint
    viewpoint = "bowler"  # Options: "bowler", "diagonal", "top-down", "sideon"

    global directory_test_case_results
    stop_simulation = False
    # Iterate over all test cases
    with open("../test/test_cases.txt", "r") as test_cases_file:
        lines = test_cases_file.readlines()[case:case+1]  # Skip header line OR CHANGE TO ACCESS OTHER TEST CASES FOR NOW
        for line in lines:
            params = line.strip().split(';')
            dt = float(params[0])
            g = float(params[1])
            rho = float(params[2])
            k_d = float(params[3])
            initial_speed = float(params[4])
            elevation_angle = float(params[5])
            horizontal_angle = float(params[6])
            #seam_facing_angle = float(params[7])  # currently unused
            spin_rate = float(params[7])
            spin_axis_angle = np.array(params[8].strip("(").strip(")").split(":"), dtype=float)  # TODO: check the angles are the right way around below
            initial_omega = [spin_rate*math.sin(spin_axis_angle[0]), spin_rate*math.cos(spin_axis_angle[1])*math.cos(spin_axis_angle[0]), spin_rate*math.cos(spin_axis_angle[2])*math.sin(spin_axis_angle[0])]
            # use spherical coordinates to get 3 components of spin from the 2 angles and magnitude
            omega = initial_omega

            description = params[9]
            print("Testing case:", description)
            if int(sys.argv[2]) == 1:
                print("Simulation Parameters:")
                print(f"  Time step (dt): {dt}")
                print(f"  Gravity (g): {g}")
                print(f"  Air density (rho): {rho}")
                print(f"  Drag coefficient (k_d): {k_d}")
                print(f"  Initial speed: {initial_speed}")
                print(f"  Elevation angle: {elevation_angle}")
                print(f"  Horizontal angle: {horizontal_angle}")
                print(f"  Initial angular velocity (spin rate): {spin_rate}")
                print(f"  Initial angular velocity (omega): {omega}")
                print(f"  Description: {description}")

            # Set recursion depth limit to be greater than default
            n = int(100 * 1/dt)
            sys.setrecursionlimit(n)

            # Set initial conditions based on test case
            speed = initial_speed
            angle_with_pos_x = horizontal_angle
            angle_with_pos_z = elevation_angle

            vx = speed * math.cos(angle_with_pos_z) * math.cos(angle_with_pos_x)
            vy = speed * math.sin(angle_with_pos_z)
            vz = speed * math.cos(angle_with_pos_z) * math.sin(angle_with_pos_x)

            x, y, z = initial_x, bowler_release_height, bowler_release_distance
            t = 0.0
            completed_bounce = False
            past_x_values = []
            past_y_values = []
            past_z_values = []


            directory_name_for_test_case = description.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")
            directory_test_case_results = "../test/test_results/" + directory_name_for_test_case
            
            os.makedirs(directory_test_case_results, exist_ok=True)

            # Set up output files
            if os.path.exists(directory_test_case_results+"/sim3D_output.txt"):
                os.remove(directory_test_case_results+"/sim3D_output.txt")
            with open(directory_test_case_results+"/sim3D_output.txt", "w") as f:
                f.write(f"t,x,y,z,vx,vy,vz\n")
            if os.path.exists(directory_test_case_results+"/sim3D_forces.txt"):
                os.remove(directory_test_case_results+"/sim3D_forces.txt")
            with open(directory_test_case_results+"/sim3D_forces.txt", "w") as f:
                f.write(f"t,ax,ay,az,Fd,Fl\n")

            main() # Run the simulation - stop at pitch boundaries not time
            plot_main()

