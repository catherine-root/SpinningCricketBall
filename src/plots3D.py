import sys, math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

### START Retrieve constants from file (repeated in sim3D.py) ###
constants = {}
with open("../src/constants.txt", "r") as f:
    for line in f:
        key, value = line.strip().split("=")
        constants[key] = float(value)

k_l = constants['k_l']
m = constants['m']
circumference_of_ball = constants['circumference_of_ball']
diameter_of_ball = constants['diameter_of_ball']
radius_of_ball = constants['radius_of_ball']
A = constants['A']
ground_size = constants['ground_size']
pitch_width = constants['pitch_width']
pitch_length = constants['pitch_length']
pitchstart_to_bowlingcrease = constants['pitchstart_to_bowlingcrease']
bowlingcrease_to_poppingcrease = constants['bowlingcrease_to_poppingcrease']
poppingcrease_to_otherpoppingcrease = constants['poppingcrease_to_otherpoppingcrease']
pitchstart_to_poppingcrease = constants['pitchstart_to_poppingcrease']
height_of_stumps = constants['height_of_stumps']
diameter_of_stumps = constants['diameter_of_stumps']
bowler_stumps_distance = constants['bowler_stumps_distance']
batter_stumps_distance = constants['batter_stumps_distance']
bowler_release_height = constants['bowler_release_height']
half_bowler_stride = constants['half_bowler_stride']
bowler_release_distance = constants['bowler_release_distance']
bowler_preferred_distance_from_centerline = constants['bowler_preferred_distance_from_centerline']
bowler_release_x = constants['bowler_release_x']

g = constants['g']
dt = constants['dt']
t = constants['initial_t']
max_time = constants['max_time']
initial_x = constants['initial_x']
x = constants['x']
y = constants['y']
z = constants['z']
### END Retrieve constants from file ### (repeated in sim3D.py)


def flight(omega, vx, vy, vz, horizontal_angle, elevation_angle):
    
    # Velocity vector and speed
    v = [vx, vy, vz]
    speed = math.sqrt(vx**2 + vy**2 + vz**2)
    
    # Coefficients
    c_l = k_l * radius_of_ball * spin_rate / (speed + 1e-8)  # to avoid division by zero - this scaling is important
    c_d = k_d  # constant depending on ball properties

    # Drag
    Fd = 0.5 * rho * speed**2 * A * c_d  # in Paper 2 & 3

    # Lift
    Fl = (4/3) * 4 * math.pi * radius_of_ball**3 * rho * c_l * np.cross(omega, v)  # vector form of lift force
    Fl_magnitude = np.linalg.norm(Fl)

    # Accelerations
    ax = (-Fd * math.sin(horizontal_angle) * math.cos(elevation_angle) + Fl[0]) / m
    ay = (-m*g - Fd * math.sin(elevation_angle) + Fl[1]) / m
    az = (-Fd * math.cos(horizontal_angle) * math.cos(elevation_angle) + Fl[2]) / m

    # Debug
    with open(directory_test_case_results+"/plot3D_debug.txt", "a") as f_debug:
        f_debug.write("\n\nIn flight:\n")
        f_debug.write(f"t={t:.3f},horizontal_angle={horizontal_angle:.5f},elevation_angle={elevation_angle:.5f}\n")
        f_debug.write(f"t={t:.3f},horizontal_angle={math.degrees(horizontal_angle):.5f},elevation_angle={elevation_angle:.5f}\n")
        f_debug.write(f"ax={ax:.3f},sin(ha)={math.sin(horizontal_angle):.5f},cos(ea)={math.cos(elevation_angle):.5f},liftX={Fl[0]:.5f}\n")
        f_debug.write(f"ay={ay:.3f},sin(ea)={math.sin(elevation_angle):.5f},cos(ea)={math.cos(elevation_angle):.5f},liftY={Fl[1]:.5f}\n")
        f_debug.write(f"az={az:.3f},cos(ha)={math.cos(horizontal_angle):.5f},cos(ea)={math.cos(elevation_angle):.5f},liftZ={Fl[2]:.5f}\n")
        f_debug.write(f"omega={omega[0]:.5f},{omega[1]:.5f},{omega[2]:.5f},mag(omega)={np.linalg.norm(omega):.5f},spin_rate={spin_rate}\n")
        f_debug.write(f"v={vx:.3f},{vy:.3f},{vz:.3f},speed={speed:.3f},\n")
        f_debug.write(f"c_l={c_l}, c_d={c_d}, spin_rate={spin_rate}\n")


    # Write accelerations and forces to a new file
    with open(directory_test_case_results+"/plot3D_forces.txt", "a") as f_forces:
        f_forces.write(f"{t:.3f},{ax:.5f},{ay:.5f},{az:.5f},{Fd:.5f},{Fl_magnitude:.5f},{Fl[0]:.5f},{Fl[1]:.5f},{Fl[2]:.5f}\n")

    # Integrate
    vx += ax * dt
    vy += ay * dt
    vz += az * dt

    # Update horizontal_angle
    horizontal_angle = -math.atan2(vx, vz) 
    elevation_angle = math.atan2(vy, vz)

    return omega, vx, vy, vz, horizontal_angle, elevation_angle

def bounce(omega, vx, vy, vz, horizontal_angle, elevation_angle):

    # Coefficients
    k = 0.65  # Coefficient of restitution
    e_number = 1  # perfectly elastic

    # Bounce dt
    dh = 0.1  # TODO : some small distance tbd
    bounce_dt = 2*e_number*math.sqrt(2*dh/g)
    
    # Bounce equations / Physics updates
    vy_new = k * vy *-1
    vx_new = -1*(radius_of_ball*omega[2] + vx)
    vz_new = radius_of_ball*omega[0] + vz

    omega_new = np.array(omega)*(2/7)+np.array([vz, vy, vx])*(5/(7*radius_of_ball))  #assuming ball is solid sphere

    horizontal_angle_new = math.atan2(vx_new, vz_new)
    elevation_angle_new = math.atan2(vy_new, vz_new)


    # Debug
    with open(directory_test_case_results+"/plot3D_debug.txt", "a") as f_debug:
        f_debug.write("\n\nBounce function.\n")
        f_debug.write(f"t={t:.3f},horizontal_angle={horizontal_angle:.5f},elevation_angle={elevation_angle:.5f} radians\n")
        f_debug.write(f"t={t:.3f},horizontal_angle={math.degrees(horizontal_angle):.5f},elevation_angle={math.degrees(elevation_angle):.5f} degrees\n")
        f_debug.write(f"t={t:.3f},horizontal_angle_new={horizontal_angle_new:.5f},elevation_angle_new={elevation_angle_new:.5f} radians\n")
        f_debug.write(f"t={t:.3f},horizontal_angle_new={math.degrees(horizontal_angle_new):.5f},elevation_angle_new={math.degrees(elevation_angle_new):.5f} degrees\n")
        f_debug.write(f"omega={omega[0]:.5f},{omega[1]:.5f},{omega[2]:.5f},mag(omega)={np.linalg.norm(omega):.5f}\n")
        f_debug.write(f"omega_new={omega_new[0]:.5f},{omega_new[1]:.5f},{omega_new[2]:.5f},mag(omega_new)={np.linalg.norm(omega_new):.5f}\n")
        om_scaled = np.array(omega)*(2/7)
        f_debug.write(f"omega_scaled={om_scaled[0]:.5f},{om_scaled[1]:.5f},{om_scaled[2]:.5f},mag(omega_scaled)={np.linalg.norm(om_scaled):.5f}\n")
        speed_vector = np.array([vx, vy, vz])
        f_debug.write(f"speed_vector={speed_vector[0]:.5f},{speed_vector[1]:.5f},{speed_vector[2]:.5f}\n")

    # TODO: is there a change in spin axis angle upon bounce? - yes compute from mag of components

    return omega_new, vx_new, vy_new, vz_new, horizontal_angle_new, elevation_angle_new, bounce_dt

def main():
    global x, y, z, vx, vy, vz, elevation_angle, horizontal_angle, omega, t
    global completed_bounce
    global radius_of_ball

    #print("In plots3D.py in main()")
    # --- Store position and time for plots ---
    with open(directory_test_case_results+"/plot3D_output.txt", "a") as f:
        f.write(f"{t:.3f},{x:.3f},{y:.3f},{z:.3f},{vx:.3f},{vy:.3f},{vz:.3f},{elevation_angle:.3f},{horizontal_angle:.3f}\n")

    if z > batter_stumps_distance:
        with open(directory_test_case_results+"/plot3D_exit_status.txt", "a") as f:
            f.write("Ball is in line with the batter's stumps. Stopping simulation.\n")
        print("Ball is in line with the batter's stumps. Stopping simulation.")
        stop_simulation = True
        plot_main()

    elif y < 0 and completed_bounce:  # stop after one bounce when it hits ground again
        with open(directory_test_case_results+"/plot3D_exit_status.txt", "a") as f:
            f.write("Ball is hitting ground a second time. Stopping simulation.\n")
        print("Ball is hitting ground a second time. Stopping simulation.")
        stop_simulation = True
        plot_main() 
    
    elif t > 8 or abs(x) > pitch_width:
        with open(directory_test_case_results+"/plot3D_exit_status.txt", "a") as f:
            f.write("Ball has gone too wide or taken too long to complete motion. Stopping simulation.\n")
        print("Ball has gone too wide or taken too long to complete motion. Stopping simulation.")
        stop_simulation = True
        plot_main()

    elif y <= 0+radius_of_ball and not completed_bounce:  # stop at ground - scaled up ball will look as if it is in the ground a bit more

        omega, vx, vy, vz, horizontal_angle, elevation_angle, bounce_dt = bounce(omega, vx, vy, vz, horizontal_angle, elevation_angle)
        completed_bounce = True
        
        # TODO: x,y,z remain the same? Roll?
        x += vx * dt
        y += vy * dt
        z += vz * dt

        t += bounce_dt
        main()
    
    else:
        omega, vx, vy, vz, horizontal_angle, elevation_angle = flight(omega, vx, vy, vz, horizontal_angle, elevation_angle)

        x += vx * dt
        y += vy * dt
        z += vz * dt

        t += dt
        main()
    

def plot_main():
    import matplotlib.pyplot as plt

    #print("In plots3D.py in plot_main()")

    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))  # t, x, y, z, vx, vy, vz, horizontal_angle, elevation_angle
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

    # Sort by time_values and rearrange corresponding arrays
    sort_indices = np.argsort(time_values)
    time_values = time_values[sort_indices]
    x_values = x_values[sort_indices]
    y_values = y_values[sort_indices]
    z_values = z_values[sort_indices]
    vx_values = vx_values[sort_indices]
    vy_values = vy_values[sort_indices]
    vz_values = vz_values[sort_indices]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_values, z_values, np.ones(len(y_values))*(0), color='grey')
    ax.plot(x_values, np.ones(len(z_values))*(pitch_length/2), y_values, color='grey') 
    ax.plot(np.ones(len(x_values))*(-pitch_width/2), z_values, y_values, color='grey')
    ax.plot(x_values, z_values, y_values, color='red')
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length/2, pitch_length/2) 
    ax.set_xlabel("x (m)")
    ax.invert_xaxis()
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_title("3D Ball Trajectory")
    plt.savefig(directory_test_case_results+"/plot3D_trajectory_line.png")
    plt.close()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values, z_values, np.zeros(len(y_values)), color='grey', s=1)
    ax.scatter(x_values, z_values, y_values, color='red', s=10)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_title("3D Ball Trajectory")
    # Set equal scale for x and z axes
    x_range = x_values.max() - x_values.min()
    z_range = z_values.max() - z_values.min()
    max_range = max(x_range, z_range)
    x_mid = (x_values.max() + x_values.min()) / 2
    z_mid = (z_values.max() + z_values.min()) / 2
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.invert_xaxis()
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length/2, pitch_length/2 + 5)
    plt.savefig(directory_test_case_results+"/plot3D_trajectory_dots.png")
    plt.close()

    modulo_dots = 10
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values[::modulo_dots], z_values[::modulo_dots], np.zeros(len(y_values[::modulo_dots])), color='grey', s=1)
    ax.scatter(x_values[::modulo_dots], z_values[::modulo_dots], y_values[::modulo_dots], color='red', s=10)  # y_values represent height, bigger dots
    ax.set_xlim(-pitch_width/2, pitch_width/2)
    ax.set_zlim(0, max(y_values)*1.1)
    ax.set_ylim(-pitch_length/2, pitch_length/2 + 5)
    ax.set_xlabel("x (m)")
    ax.invert_xaxis()
    ax.set_ylabel("z (m)")
    ax.set_zlabel("y (m)")
    ax.set_title("3D Ball Trajectory")
    plt.savefig(directory_test_case_results+"/plot3D_trajectory_fewer_dots.png")
    plt.close()

    # Top down, i.e. bird's eye view
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.set_xlabel("z (m)")
    ax.set_ylabel("x (m)")
    ax.set_title("2D Ball Trajectory")
    ax.plot(z_values, (x_values*0)+initial_x, color='black', linestyle="dashed", label="Line x=initial_x")
    ax.plot(z_values, x_values, label="Trajectory")
    ax.set_ylim(-pitch_width/2, pitch_width/2)
    ax.set_xlim(-pitch_length/2, pitch_length/2)  # z along pitch length
    ax.set_aspect('equal', adjustable='box')
    ax.legend()
    plt.savefig(directory_test_case_results+"/plot2D_trajectory_line_topdown.png", bbox_inches="tight")
    plt.close()

    print("Plots saved.")
    return
    
if __name__ == "__main__":
    global case
    case = int(sys.argv[1])

    global debug_mode
    debug_mode = int(sys.argv[2])

    if case == 0:
        print("0 is an invalid case number. Running case 1 instead.")
        case = 1

    #print("In plots3D.py running case", case)

    global viewpoint
    viewpoint = "sideon"  # other options: "bowler", "diagonal", "top-down"

    global directory_test_case_results

    # Status booleans
    completed_bounce = False  # there will be one bounce
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
            elevation_angle = float(params[5])  # zy
            horizontal_angle = float(params[6])  #zx
            initial_speed_vector = [initial_speed*math.cos(elevation_angle)*math.sin(horizontal_angle), initial_speed*math.sin(elevation_angle), initial_speed*math.cos(elevation_angle)*math.cos(horizontal_angle)] # v_x, v_y, v_z
            global spin_rate
            spin_rate = float(params[7])
            spin_axis_angle_up = float(params[8])
            spin_axis_angle_side = float(params[9])
            initial_speed_vector = [initial_speed_vector[0], initial_speed_vector[1], initial_speed_vector[2]]  # v_x, v_y, v_z
            spin_axis_angle = [spin_axis_angle_up, spin_axis_angle_side]
            initial_omega = [spin_rate*math.cos(spin_axis_angle_up)*math.cos(spin_axis_angle[1]), 0, spin_rate*math.cos(spin_axis_angle_up)*math.sin(spin_axis_angle[1])] # w_x, w_y, w_z            
            # using spherical coordinates to get 3 components of spin from the 2 angles and magnitude
            omega = initial_omega

            description = params[10]
            print("Testing case:", description)
            if int(sys.argv[2]) == 1:
                print("Simulation Parameters:")
                print(f"  Time step (dt): {dt}")
                print(f"  Gravity (g): {g}")
                print(f"  Air density (rho): {rho}")
                print(f"  Drag coefficient (k_d): {k_d}")
                print(f"  Initial speed: {initial_speed}")
                print(f"  Elevation angle: {elevation_angle}")
                print(f"  Horizontal angle: {horizontal_angle:.5f}")
                print(f"  Initial speed vector: {initial_speed_vector}")
                print(f"  Initial angular velocity (spin rate): {spin_rate}")
                print(f"  Spin axis angle up: {spin_axis_angle_up}")
                print(f"  Spin axis angle side: {spin_axis_angle_side}")
                print(f"  Initial angular velocity (omega): {omega}")
                print(f"  Description: {description}")

            # Set recursion depth limit to be greater than default
            n = int(100 * 1/dt)
            sys.setrecursionlimit(n)

            # Set initial conditions based on test case
            vx, vy, vz = initial_speed_vector

            x, y, z = initial_x, bowler_release_height, bowler_release_distance
            t = 0.0
            completed_bounce = False


            directory_name_for_test_case = description.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")
            directory_test_case_results = "../test/test_results/" + directory_name_for_test_case
            
            os.makedirs(directory_test_case_results, exist_ok=True)

            # Set up output files
            if os.path.exists(directory_test_case_results+"/plot3D_exit_status.txt"):
                os.remove(directory_test_case_results+"/plot3D_exit_status.txt")
            with open(directory_test_case_results+"/plot3D_exit_status.txt", "w") as f:
                f.write(f"Started model execution.\n")
            if os.path.exists(directory_test_case_results+"/plot3D_output.txt"):
                os.remove(directory_test_case_results+"/plot3D_output.txt")
            with open(directory_test_case_results+"/plot3D_output.txt", "w") as f:
                f.write(f"t,x,y,z,vx,vy,vz,horizontal_angle,elevation_angle\n")
            if os.path.exists(directory_test_case_results+"/plot3D_forces.txt"):
                os.remove(directory_test_case_results+"/plot3D_forces.txt")
            with open(directory_test_case_results+"/plot3D_forces.txt", "w") as f:
                f.write(f"t,ax,ay,az,Fd,Fl_mag,Flx,Fly,Flz\n")
            if os.path.exists(directory_test_case_results+"/plot3D_debug.txt"):
                os.remove(directory_test_case_results+"/plot3D_debug.txt")
            with open(directory_test_case_results+"/plot3D_debug.txt", "w") as f:
                f.write(f"DEBUG STARTED\n")
                f.write(f"Testing case: {description}\n")
                f.write("Simulation Parameters:\n")
                f.write(f"  Time step (dt): {dt}\n")
                f.write(f"  Gravity (g): {g}\n")
                f.write(f"  Air density (rho): {rho}\n")
                f.write(f"  Drag coefficient (k_d): {k_d}\n")
                f.write(f"  Initial speed: {initial_speed}\n")
                f.write(f"  Elevation angle: {elevation_angle}\n")
                f.write(f"  Horizontal angle: {horizontal_angle:.7f}\n")
                f.write(f"  Initial speed vector: {initial_speed_vector}\n")
                f.write(f"  Initial angular velocity (spin rate): {spin_rate}\n")
                f.write(f"  Spin axis angle up: {spin_axis_angle_up}\n")
                f.write(f"  Spin axis angle side: {spin_axis_angle_side}\n")
                f.write(f"  Initial angular velocity (omega): {omega}\n")
                f.write(f"  Description: {description}\n")

            main() # Run the simulation - stop at pitch boundaries not time
            plot_main()
