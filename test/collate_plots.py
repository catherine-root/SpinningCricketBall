import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import shutil

### Get folder/testcase name and values tested in range
name = str(sys.argv[1])
values = sorted(np.array(sys.argv[2].strip().split(",")))[:5]
#print(f"Running collation for test case {name} with values {values}.")

### START Retrieve constants from file (repeated in plots3D.py and sim3D.py) ###
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
### END Retrieve constants from file (repeated in plots3D.py and sim3D.py) ###

### Move folders into shared folder
target = f"test_results/{name}_{''.join([str(v) for v in values])}"
os.makedirs(target, exist_ok=True)

### Create overlay plot - i.e. all trajectories on same plot

## 3D
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("x (m)")
ax.set_ylabel("z (m)")
ax.set_zlabel("y (m)")
ax.set_title("3D Ball Trajectory - Different " + name.replace("_", " ") )

# Create color map for the range of values
colours = plt.cm.viridis(np.linspace(0, 1, len(values)))
max_y_value = 0

for idx, v in enumerate(values):
    src = f"{name}_{str(v)}"
    directory_test_case_results = f"test_results/{src}" #f"test_results/{target}/{src}"
    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))  # t, x, y, z, vx, vy, vz, angle_with_pos_x, angle_with_pos_z
        for i, line in enumerate(lines):
            data_matrix[i] = np.array(line.strip().split(','), dtype=float)

    time_values = data_matrix[:, 0]
    x_values = data_matrix[:, 1]
    y_values = data_matrix[:, 2]
    if max(y_values) > max_y_value:
        max_y_value = max(y_values)
    z_values = data_matrix[:, 3]
    vx_values = data_matrix[:, 4]
    vy_values = data_matrix[:, 5]
    vz_values = data_matrix[:, 6]

    ax.plot(x_values, z_values, y_values, color=colours[idx],label=f'{v}')  # y_values represent height

ax.legend(title='Values', bbox_to_anchor=(1.05, 1), loc='upper left') 
ax.set_xlim(-pitch_width/2, pitch_width/2)
ax.invert_xaxis()
ax.set_zlim(0, max_y_value*1.1)
ax.set_ylim(-pitch_length, pitch_length) # TODO: pitch length is double what it should be - see calculations
plt.savefig(target+f"/plot3D_trajectory_line_{name}s_{''.join([str(v) for v in values])}.png", bbox_inches="tight")

## 2D

# Side-on
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.set_xlabel("z (m)")
ax.set_ylabel("y (m)")
ax.set_title("2D Ball Trajectory - Different " + name.replace("_", " "))

colours = plt.cm.viridis(np.linspace(0, 1, len(values)))
max_y_value = 0
min_y_value = 0

for idx, v in enumerate(sorted(values)):
    src = f"{name}_{str(v)}"
    directory_test_case_results = f"test_results/{src}"
    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))  # t, x, y, z, vx, vy, vz, angle_with_pos_x, angle_with_pos_z
        for j, line in enumerate(lines):
            data_matrix[j] = np.array(line.strip().split(','), dtype=float)

    if max(y_values) > max_y_value:
        max_y_value = max(y_values)
    if "dt" in name and min(y_values) < min_y_value:  # so can see whole line for each dt tested
        min_y_value = min(y_values)
    y_values = data_matrix[:, 2]
    z_values = data_matrix[:, 3]

    ax.plot(z_values, y_values, color=colours[idx], label=f'{v}')

if "dt" in name:
    ax.plot([-pitch_length/2, pitch_length/2], [0, 0], color='black', linestyle="dashed", label="Ground, y=0")
ax.legend(title='Values', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_ylim(min_y_value, max_y_value*1.1)
ax.set_xlim(-pitch_length/2, pitch_length/2)  # z along pitch length
ax.set_aspect('equal', adjustable='box')
plt.savefig(target + f"/plot2D_trajectory_line_{name}s_{''.join([str(v) for v in values])}_sideon.png", bbox_inches="tight")
plt.close()

# Top down, i.e. bird's eye view
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.set_xlabel("z (m)")
ax.set_ylabel("x (m)")
ax.set_title("2D Ball Trajectory - Different " + name.replace("_", " "))

colours = plt.cm.viridis(np.linspace(0, 1, len(values)))

for idx, v in enumerate(sorted(values)):
    src = f"{name}_{str(v)}"
    directory_test_case_results = f"test_results/{src}"
    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))  # t, x, y, z, vx, vy, vz, angle_with_pos_x, angle_with_pos_z
        for j, line in enumerate(lines):
            data_matrix[j] = np.array(line.strip().split(','), dtype=float)

    x_values = data_matrix[:, 1]
    z_values = data_matrix[:, 3]

    ax.plot(z_values, x_values, color=colours[idx], label=f'{v}')

ax.legend(title='Values', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_ylim(-pitch_width/2, pitch_width/2)
ax.set_xlim(-pitch_length, pitch_length)  # z along pitch length
ax.set_aspect('equal', adjustable='box')
plt.savefig(target + f"/plot2D_trajectory_line_{name}s_{''.join([str(v) for v in values])}_topdown.png", bbox_inches="tight")
plt.close()

### Create statistics

## Which value causes maximum and minimum x, y, z values?
max_x = float('-inf')
min_x = float('inf')
max_y = float('-inf')
min_y = float('inf')
max_z = float('-inf')
min_z = float('inf')
max_x_value = None
min_x_value = None
max_y_value = None
min_y_value = None
max_z_value = None
min_z_value = None

for v in sorted(values):
    src = f"{name}_{str(v)}"
    directory_test_case_results = f"test_results/{src}"
    with open(directory_test_case_results+"/plot3D_output.txt", "r") as f:
        lines = f.readlines()[1:]  # Skip header
        data_matrix = np.zeros((len(lines), 9))
        for j, line in enumerate(lines):
            data_matrix[j] = np.array(line.strip().split(','), dtype=float)
    
    x_values = data_matrix[:, 1]
    y_values = data_matrix[:, 2]
    z_values = data_matrix[:, 3]
    
    if max(abs(x_values)) > max_x:
        max_x = max(abs(x_values))
        max_x_value = v
    if min(x_values) < min_x:
        min_x = min(x_values)
        min_x_value = v
    if max(y_values) > max_y:
        max_y = max(y_values)
        max_y_value = v
    if min(y_values) < min_y:
        min_y = min(y_values)
        min_y_value = v
    if max(abs(z_values)) > max_z:
        max_z = max(abs(z_values))
        max_z_value = v
    if min(z_values) < min_z:
        min_z = min(z_values)
        min_z_value = v

with open(target+"/results.txt", "w") as fh:
    fh.write(f"Maximum statistics for {target}:\n")
    fh.write(f"Maximum x: {max_x:.2f}m at value {max_x_value}\n")
    fh.write(f"Minimum x: {min_x:.2f}m at value {min_x_value}\n")
    fh.write(f"Maximum height (y): {max_y:.2f}m at value {max_y_value}\n")
    fh.write(f"Minimum height (y): {min_y:.2f}m at value {min_y_value}\n")
    fh.write(f"Maximum z: {max_z:.2f}m at value {max_z_value}\n")
    fh.write(f"Minimum z: {min_z:.2f}m at value {min_z_value}\n")
