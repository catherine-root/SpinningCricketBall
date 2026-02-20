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

### Constants from plots3D.py
# Ball
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
batter_stumps_distance = pitch_length/2 + 5 - pitchstart_to_bowlingcrease
# Bowler dimensions
bowler_height = 1.8  # Get reference for average height of a male spin bowler = approx 1.8 metres
release_height_above_bowler_head = 0.5  # approximate height of arm above head at release
bowler_release_height = bowler_height + release_height_above_bowler_head
half_bowler_stride = 0.3  # approximate half stride length to find distance between popping crease and x position of bowler's hand
bowler_release_distance = -pitch_length/2 + pitchstart_to_poppingcrease - half_bowler_stride
bowler_preferred_distance_from_centerline = 0.3 
bowler_release_x = 0.0 + bowler_preferred_distance_from_centerline  # for right-handed bowler and batsman

# Storing positions for flight trail of ball
past_x_values = []
past_y_values = []
past_z_values = []

# Window size
width, height = 800, 600
images = []
stop_simulation = False

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
    
def display():  # I think the display is reflected in x axis (down line of bowler's view is +x)
    global data, data_line_index
    global past_x_values, past_y_values, past_z_values
    global radius_of_ball

    scaled_radius_of_ball = 5 * radius_of_ball

    # Repeating here: inefficient
    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        data = f.readlines()

    # Read data from file
    if data_line_index >= len(data):
        glutLeaveMainLoop()
        return
    t, x, y, z, vx, vy, vz, horizontal_angle, elevation_angle = data[data_line_index].split(",")
    with open(directory_test_case_results+"/sim3D_debug.txt", "a") as f:
        #f.write(f"data[{data_line_index}]: {t:.3f},{x:.3f},{y:.3f},{z:.3f},{vx:.3f},{vy:.3f},{vz:.3f},{horizontal_angle:.3f},{elevation_angle:.3f}\n")
        f.write(f"data\n")
    data_line_index += 1

    x = float(x)
    y = float(y)
    z = float(z)

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
        gluLookAt(20, 2, 0, 0, 0, 0, 0, 1, 0)
    

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

    '''for i in range(40):
        try:
            glPushMatrix()
            glPopMatrix()
        except:
            print("Overflow at push", i)
            break
    err = glGetError()
    print("GL error before push:", err)'''
    # Draw stumps as a cylinder
    for x_offset in [-0.05, 0, 0.05]:
        glPushMatrix()
        #glBegin(GL_CYLINDER)
        glColor3f(1,1,1)
        glTranslatef(x_offset, 0, bowler_stumps_distance)
        quadric = gluNewQuadric()
        gluCylinder(quadric, diameter_of_stumps / 2, diameter_of_stumps / 2, height_of_stumps, 32, 1)
        gluDeleteQuadric(quadric)
        #glEnd()
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

    '''# TODO : fix angle of seam lines on ball
    # Draw two thin lines around the circumference of the ball, rotated by elevation_angle
    glColor3f(1.0, 0.75, 0.75)  # Red lines
    seam_offset = diameter_of_ball * 0.05
    glLineWidth(seam_offset/3) # two lines with a line-widht gap between them
    for z_offset in [-seam_offset, seam_offset]:  # Two lines, slightly above and below center
        # Rotate the seam lines by elevation_angle about the z-axis
        glRotatef(math.degrees(elevation_angle), 0, 0, 1)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2 * math.pi * i / 100
            x_circ = 0.5 * math.cos(theta)
            y_circ = 0.5 * math.sin(theta)
            glVertex3f(x_circ, y_circ, z_offset)
        glEnd()
    '''
    glPopMatrix()


    # Ball shadow on ground - assuming sun directly overhead
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

    # For rendering display
    glutSwapBuffers()

    # Store images for video
    global images
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)  # image
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # flip vertically
    images.append(np.array(image))
    print("Appended image to array.")


def timer(value):
    glutPostRedisplay()
    glutTimerFunc(int(dt*1000), timer, 0)


'''def timer(value):
    global t
    if data_line_index < len(data)-1:
        glutPostRedisplay()
        glutTimerFunc(int(dt*10), timer, 0)
    else:
        print("Simulation finished.")
        imageio.mimsave(directory_test_case_results+"/sim_"+viewpoint+".gif", images, fps=10*int(len(images)/max_time))
        print("Simulation saved.")
        
        #from OpenGL.GLUT import glutLeaveMainLoop
        #glutLeaveMainLoop()
        print("After glutLeaveMainLoop attempt.")'''

def main_start():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"3D Cricket Ball Motion - OpenGL")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()
    print("end main")

    
#if __name__ == "__main__":
if True:
    global case, viewpoint
    case = int(sys.argv[1])
    viewpoint = str(sys.argv[2])  # options: "sideon", "bowler", "diagonal", "top-down"

    if case == 0:
        print("0 is an invalid case number. Running case 1 instead.")
        case = 1

    global directory_test_case_results
    stop_simulation = False
    # Iterate over all test cases
    with open("../test/test_cases.txt", "r") as test_cases_file:
        lines = test_cases_file.readlines()[case:case+1]  # Skip header line OR CHANGE TO ACCESS OTHER TEST CASES FOR NOW
        for line in lines:
            params = line.strip().split(';')
            global t, dt, max_time
            dt = float(params[0])
            g = float(params[1])
            rho = float(params[2])
            k_d = float(params[3])
            initial_speed = float(params[4])
            elevation_angle = float(params[5])  # zy
            horizontal_angle = float(params[6])  #zx
            motion_angle_from_y = math.radians(90) - elevation_angle
            initial_speed_vector = [initial_speed*math.sin(motion_angle_from_y)*math.sin(horizontal_angle), initial_speed*math.cos(motion_angle_from_y), initial_speed*math.sin(motion_angle_from_y)*math.cos(horizontal_angle)] # v_x, v_y, v_z
            #seam_facing_angle = float(params[7])  # currently unused
            spin_rate = float(params[7])
            spin_axis_angle_up = float(params[8])
            spin_axis_angle_side = float(params[9])
            #spin_axis_angle = np.array(params[8].strip("(").strip(")").split(":"), dtype=float) # zy, zx # TODO: check the angles are the right way around below
            #OLD initial_omega = [spin_rate*math.sin(spin_axis_angle[0]), spin_rate*math.cos(spin_axis_angle[1])*math.cos(spin_axis_angle[0]), spin_rate*math.cos(spin_axis_angle[2])*math.sin(spin_axis_angle[0])]
            spin_axis_angle_from_y = math.radians(90) - spin_axis_angle_up
            spin_axis_angle = [spin_axis_angle_up, spin_axis_angle_side]
            initial_omega = [spin_rate*math.sin(spin_axis_angle_from_y)*math.sin(spin_axis_angle[1]), spin_rate*math.cos(spin_axis_angle_from_y), spin_rate*math.sin(spin_axis_angle_from_y)*math.cos(spin_axis_angle[1])] # w_x, w_y, w_z
            # using spherical coordinates to get 3 components of spin from the 2 angles and magnitude
            omega = initial_omega

            description = params[10]
            print("Testing case:", description)

            # Set recursion depth limit to be greater than default
            n = int(100 * 1/dt)
            sys.setrecursionlimit(n) # maybe don't need

            # Time
            t = 0.0
            max_time = 5  # seconds


            directory_name_for_test_case = description.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")
            directory_test_case_results = "../test/test_results/" + directory_name_for_test_case
            
            os.makedirs(directory_test_case_results, exist_ok=True)

            # Set up input/output files
            with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
                global data, data_line_index
                data = f.readlines()
                data_line_index = 1  # from 1 onwards to skip column headers t,x,y,z,vx,vy,vz,horizontal_angle,elevation_angle

            if os.path.exists(directory_test_case_results+"/sim3D_debug.txt"):
                os.remove(directory_test_case_results+"/sim3D_debug.txt")
            with open(directory_test_case_results+"/sim3D_debug.txt", "w") as f:
                f.write(f"DEBUG STARTED\n")
                f.write(f"Testing case: {description}\n")
                f.write("Simulation Parameters:\n")
                f.write(f"  Time step (dt): {dt}\n")
                f.write(f"  Gravity (g): {g}\n")
                f.write(f"  Air density (rho): {rho}\n")
                f.write(f"  Drag coefficient (k_d): {k_d}\n")
                f.write(f"  Initial speed: {initial_speed}\n")
                f.write(f"  Elevation angle: {elevation_angle}\n")
                f.write(f"  Horizontal angle: {horizontal_angle}\n")
                f.write(f"  Initial speed vector: {initial_speed_vector}\n")
                f.write(f"  Initial angular velocity (spin rate): {spin_rate}\n")
                f.write(f"  Spin axis angle up: {spin_axis_angle_up}\n")
                f.write(f"  Spin axis angle side: {spin_axis_angle_side}\n")
                f.write(f"  Initial angular velocity (omega): {omega}\n")
                f.write(f"  Description: {description}\n")

            main_start() # Run the simulation - stop at pitch boundaries not time
            imageio.mimsave(directory_test_case_results+"/sim_"+viewpoint+".gif", images, fps=10*int(len(images)/max_time))
            print("Simulation saved.")

