import math

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
pitch_length = 22.56
pitchstart_to_bowlingcrease = 1.22
bowlingcrease_to_poppingcrease = 1.22
poppingcrease_to_otherpoppingcrease = 17.68
pitchstart_to_poppingcrease = pitchstart_to_bowlingcrease + bowlingcrease_to_poppingcrease
height_of_stumps = 0.72
diameter_of_stumps = 0.04
bowler_stumps_distance = -pitch_length/2 + pitchstart_to_bowlingcrease
batter_stumps_distance = pitch_length/2 - pitchstart_to_bowlingcrease

# Bowler dimensions
bowler_release_height = 2.1  # approximate ball release height based on bowler's heights, arm lengths, and arm angles
half_bowler_stride = 0.505/2  # approximate half stride length to find distance between popping crease and x position of bowler's hand
bowler_release_distance = -pitch_length/2 + pitchstart_to_poppingcrease - half_bowler_stride
bowler_preferred_distance_from_centerline = 0.3 
bowler_release_x = 0.0 + bowler_preferred_distance_from_centerline  # for right-handed bowler and batsman

# Physics parameters
g = 9.81
dt = 0.01
initial_t = 0.0
max_time = 5  # seconds

# Initial position
initial_x = bowler_release_x # TODO: future possible offset in display: initial_x = bowler_release_x 
x, y, z = initial_x, bowler_release_height, bowler_release_distance  # start above ground, back from origin at popping crease
# x = along pitch, y = height, z = across pitch


# TODO: write all of these as a dictionary then write names and values to a file. Can then read in to other files as data['varname'] = value.
# then also need to update other files to say data['varname'] instead of just varname.
data = {}
data['k_l'] = k_l
data['m'] = m
data['circumference_of_ball'] = circumference_of_ball
data['diameter_of_ball'] = diameter_of_ball
data['radius_of_ball'] = radius_of_ball
data['A'] = A
data['ground_size'] = ground_size
data['pitch_width'] = pitch_width
data['pitch_length'] = pitch_length
data['pitchstart_to_bowlingcrease'] = pitchstart_to_bowlingcrease
data['bowlingcrease_to_poppingcrease'] = bowlingcrease_to_poppingcrease
data['poppingcrease_to_otherpoppingcrease'] = poppingcrease_to_otherpoppingcrease
data['pitchstart_to_poppingcrease'] = pitchstart_to_poppingcrease
data['height_of_stumps'] = height_of_stumps
data['diameter_of_stumps'] = diameter_of_stumps
data['bowler_stumps_distance'] = bowler_stumps_distance
data['batter_stumps_distance'] = batter_stumps_distance
data['bowler_release_height'] = bowler_release_height
data['half_bowler_stride'] = half_bowler_stride
data['bowler_release_distance'] = bowler_release_distance
data['bowler_preferred_distance_from_centerline'] = bowler_preferred_distance_from_centerline
data['bowler_release_x'] = bowler_release_x

data['g'] = g
data['dt'] = dt
data['initial_t'] = initial_t
data['max_time'] = max_time
data['initial_x'] = initial_x
data['x'] = x
data['y'] = y
data['z'] = z

# Write dictionary contents to file
with open("constants.txt", "w") as f:
    for key, value in data.items():
        f.write(f"{key}={value}\n")