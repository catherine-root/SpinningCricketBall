import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import shutil

### Get folder/testcase name and values tested in range
name = str(sys.argv[1])
values = sorted(np.array(sys.argv[2].strip().split(",")))[:5]
print(f"Running collation for test case {name} with values {values}.")

# TODO : pull into data file possibly so these numbers stay consistent across all files
### Field and Pitch dimensions
ground_size = 140  # diameter
pitch_width = 3.05
pitch_length = 22.56  # TODO: pitch length is double what is should be - see calculations = -pitch_length instead of -pitch_length/2
pitchstart_to_bowlingcrease = 1.22
bowlingcrease_to_poppingcrease = 1.22
poppingcrease_to_otherpoppingcrease = 17.68
pitchstart_to_poppingcrease = pitchstart_to_bowlingcrease + bowlingcrease_to_poppingcrease
height_of_stumps = 0.72
diameter_of_stumps = 0.04
bowler_stumps_distance = -pitch_length + pitchstart_to_bowlingcrease
batter_stumps_distance = pitch_length - pitchstart_to_bowlingcrease


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

for i, v in enumerate(values):
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

    ax.plot(x_values, z_values, y_values, label=f'{v}')  # y_values represent height

ax.legend(title='Values', bbox_to_anchor=(1.05, 1), loc='upper left') 
ax.set_xlim(-pitch_width/2, pitch_width/2)
ax.invert_xaxis()
ax.set_zlim(0, max_y_value*1.1)
ax.set_ylim(-pitch_length, pitch_length) # TODO: pitch length is double what it should be - see calculations
plt.savefig(target+f"/plot3D_trajectory_line_{name}s_{''.join([str(v) for v in values])}.png")

## 2D

# Side-on
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.set_xlabel("z (m)")
ax.set_ylabel("y (m)")
ax.set_title("2D Ball Trajectory - Different " + name.replace("_", " ") + " (z vs y)")

colours = plt.cm.viridis(np.linspace(0, 1, len(values)))
max_y_value = 0

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
    y_values = data_matrix[:, 2]
    z_values = data_matrix[:, 3]

    ax.plot(z_values, y_values, color=colours[idx], label=f'{v}')

ax.legend(title='Values', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_ylim(0, max_y_value*1.1)
ax.set_xlim(-pitch_length, pitch_length)  # z along pitch length
ax.set_aspect('equal', adjustable='box')
plt.savefig(target + f"/plot2D_trajectory_line_{name}s_{''.join([str(v) for v in values])}_sideon.png")
plt.close()

# Top down, i.e. bird's eye view
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.set_xlabel("z (m)")
ax.set_ylabel("x (m)")
ax.set_title("2D Ball Trajectory - Different " + name.replace("_", " ") + " (z vs x)")

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
plt.savefig(target + f"/plot2D_trajectory_line_{name}s_{''.join([str(v) for v in values])}_topdown.png")
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

#out_path = os.path.join(target, "results.txt")
with open(target+"/results.txt", "w") as fh:
    fh.write(f"Maximum statistics for {target}:\n")
    fh.write(f"Maximum x: {max_x:.2f}m at value {max_x_value}\n")
    fh.write(f"Minimum x: {min_x:.2f}m at value {min_x_value}\n")
    fh.write(f"Maximum height (y): {max_y:.2f}m at value {max_y_value}\n")
    fh.write(f"Minimum height (y): {min_y:.2f}m at value {min_y_value}\n")
    fh.write(f"Maximum z: {max_z:.2f}m at value {max_z_value}\n")
    fh.write(f"Minimum z: {min_z:.2f}m at value {min_z_value}\n")

## ??