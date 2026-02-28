import math

class TestCase:
    def __init__(self, dt=0.01, g=9.80, rho=1.225, k_d=0.5, initial_speed=18.5, elevation_angle=math.radians(6), horizontal_angle=math.radians(0), spin_rate=56*math.pi, spin_axis_angle_up=math.radians(10), spin_axis_angle_side=math.radians(60), description=""):  # default spin_axis_angle_side should be 60
        self.dt = dt
        self.g = g
        self.rho = rho
        self.k_d = k_d  # drag coefficient is multiplicative factor in drag force calculation
        self.initial_speed = initial_speed
        self.elevation_angle = elevation_angle
        self.horizontal_angle = horizontal_angle
        self.spin_rate = spin_rate
        self.spin_axis_angle_up = spin_axis_angle_up 
        self.spin_axis_angle_side = spin_axis_angle_side        
        self.description = description

    def __repr__(self):
        return f"TestCase(dt={self.dt}, g={self.g}, rho={self.rho}, k_d={self.k_d}, initial_speed={self.initial_speed}, elevation={self.elevation_angle},horizontal={self.horizontal_angle}, spin_rate={self.spin_rate}, spin_axis_angle_zy={self.spin_axis_angle_up}, spin_axis_angle_zx={self.spin_axis_angle_side}, description='{self.description}')"

    def write_to_file(self):
        with open("test_cases.txt", "a") as f:
            f.write(f"{self.dt};{self.g};{self.rho};{self.k_d};{self.initial_speed};{self.elevation_angle};{self.horizontal_angle};{self.spin_rate};{self.spin_axis_angle_up};{self.spin_axis_angle_side};{self.description}\n")
with open("test_cases.txt", "w") as f:
    f.write("dt;g;k_d;initial_speed;elevation_angle;horizontal_angle;spin_rate;spin_angle_up;spin_angle_side;description\n")

## DEFINE TEST CASES ##
default_off = TestCase(description="Default off spin")
default_off.write_to_file()

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
# off spin
state_squad_player = TestCase(initial_speed=19.8, spin_rate=2*math.pi*27.2, spin_axis_angle_up=math.radians(11.4), spin_axis_angle_side=math.radians(48.2), description="Off-spin Player 1")
state_squad_player.write_to_file()
first_grade_club_player1 = TestCase(initial_speed=19.5, spin_rate=2*math.pi*26.8, spin_axis_angle_up=math.radians(14.8), spin_axis_angle_side=math.radians(62), description="Off-spin Player 2.1")
first_grade_club_player1.write_to_file()
first_grade_club_player2 = TestCase(initial_speed=18.1, spin_rate=2*math.pi*28.3, spin_axis_angle_up=math.radians(2.6), spin_axis_angle_side=math.radians(60.4), description="Off-spin Player 2.2")
first_grade_club_player2.write_to_file()
third_grade_club_player1 = TestCase(initial_speed=16.9, spin_rate=2*math.pi*20.2, spin_axis_angle_up=math.radians(17.1), spin_axis_angle_side=math.radians(64.9), description="Off-spin Player 3")
third_grade_club_player1.write_to_file()
part_time_player = TestCase(initial_speed=17.2, spin_rate=2*math.pi*16.4, spin_axis_angle_up=math.radians(12.1), spin_axis_angle_side=math.radians(126.8), description="Off-spin Player 4")
part_time_player.write_to_file()

default_leg = TestCase(spin_axis_angle_side=math.radians(-45), description="Default leg spin")
default_leg.write_to_file()

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
# leg spin
first_grade_club_player = TestCase(initial_speed=17.5, spin_rate=2*math.pi*29.2, spin_axis_angle_up=math.radians(-8.2), spin_axis_angle_side=math.radians(-50), description="Leg-spin Player 1")
first_grade_club_player.write_to_file()
third_grade_club_player1 = TestCase(initial_speed=18.2, spin_rate=2*math.pi*27.9, spin_axis_angle_up=math.radians(17.1), spin_axis_angle_side=math.radians(-37.7), description="Leg-spin Player 2.1")
third_grade_club_player1.write_to_file()
third_grade_club_player2 = TestCase(initial_speed=20.1, spin_rate=2*math.pi*24.4, spin_axis_angle_up=math.radians(-16.3), spin_axis_angle_side=math.radians(-27.2), description="Leg-spin Player 2.2")
third_grade_club_player2.write_to_file()
third_grade_club_player3 = TestCase(initial_speed=18.6, spin_rate=2*math.pi*24.9, spin_axis_angle_up=math.radians(9), spin_axis_angle_side=math.radians(-43.7), description="Leg-spin Player 2.3")
third_grade_club_player3.write_to_file()
avg_initial_speed = (17.5+18.2+20.1+18.6)/4
avg_spin = (29.2+27.9+24.4+24.9)/4
avg_angle_up = (-8.2+17.1-16.3+9)/4
avg_angle_side = (50+37.7+27.2+43.7)/4
average_player = TestCase(initial_speed=17.2, spin_rate=2*math.pi*avg_spin, spin_axis_angle_up=math.radians(avg_angle_up), spin_axis_angle_side=math.radians(180-avg_angle_side), description="Leg-spin Player 3")
average_player.write_to_file()

top_spin = TestCase(spin_rate=60*math.pi, spin_axis_angle_up=math.radians(90), spin_axis_angle_side=math.radians(0), description="Top spin")
top_spin.write_to_file()

no_spin = TestCase(spin_rate=0, description="No spin")
no_spin.write_to_file()

no_flight_off = TestCase(initial_speed=0, description="No flight Off")
no_flight_off.write_to_file()
no_flight_leg = TestCase(initial_speed=0, spin_axis_angle_side=math.radians(-45), description="No flight Leg")
no_flight_leg.write_to_file()

no_drag_off = TestCase(k_d=0, description="No drag Off")
no_drag_off.write_to_file()
no_drag_leg = TestCase(k_d=0, spin_axis_angle_side=math.radians(-45), description="No drag Leg")
no_drag_leg.write_to_file()

large_drag_off = TestCase(k_d=10, description="Large drag Off")
large_drag_off.write_to_file()
large_drag_leg = TestCase(k_d=10, spin_axis_angle_side=math.radians(-45), description="Large drag Leg")
large_drag_leg.write_to_file()

no_elevation = TestCase(elevation_angle=0, description="No elevation angle")
no_elevation.write_to_file()

# Spin vector (backspin = spin around x-axis, pointing left-right)
# assume clockwise round x (top spin rate), clockwise round y (), clockwise round z ??????????
# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
# for later comparison with each other
spin_rate20 = TestCase(spin_rate=20, description="Spin rate 20")
spin_rate20.write_to_file()
spin_rate60 = TestCase(spin_rate=60, description="Spin rate 60")
spin_rate60.write_to_file()
spin_rate100 = TestCase(spin_rate=100, description="Spin rate 100")
spin_rate100.write_to_file()
spin_rate140 = TestCase(spin_rate=140, description="Spin rate 140")
spin_rate140.write_to_file()
spin_rate180 = TestCase(spin_rate=180, description="Spin rate 180")
spin_rate180.write_to_file()

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
speed = 14
speed14 = TestCase(initial_speed=speed, description="Initial speed "+str(speed))
speed14.write_to_file()
speed = 16
speed16 = TestCase(initial_speed=speed, description="Initial speed "+str(speed))
speed16.write_to_file()
speed = 18
speed18 = TestCase(initial_speed=speed, description="Initial speed "+str(speed))
speed18.write_to_file()
speed = 20
speed20 = TestCase(initial_speed=speed, description="Initial speed "+str(speed))
speed20.write_to_file()
speed = 22
speed22 = TestCase(initial_speed=speed, description="Initial speed "+str(speed))
speed22.write_to_file()

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
ea = -10
ea_10 = TestCase(elevation_angle=math.radians(ea), description="Initial elevation angle (deg) "+str(ea))
ea_10.write_to_file()
ea = 0
ea0 = TestCase(elevation_angle=math.radians(ea), description="Initial elevation angle (deg) "+str(ea))
ea0.write_to_file()
ea = 10
ea10 = TestCase(elevation_angle=math.radians(ea), description="Initial elevation angle (deg) "+str(ea))
ea10.write_to_file()
ea = 20
ea20 = TestCase(elevation_angle=math.radians(ea), description="Initial elevation angle (deg) "+str(ea))
ea20.write_to_file()
ea = 30
ea30 = TestCase(elevation_angle=math.radians(ea), description="Initial elevation angle (deg) "+str(ea))
ea30.write_to_file()



dt1 = TestCase(dt=1, description="Flight dt 1")
dt1.write_to_file()
dt05 = TestCase(dt=0.5, description="Flight dt 0.5")
dt05.write_to_file()
dt01 = TestCase(dt=0.1, description="Flight dt 0.1")
dt01.write_to_file()
dt001 = TestCase(dt=0.01, description="Flight dt 0.01")
dt001.write_to_file()
dt0001 = TestCase(dt=0.001, description="Flight dt 0.001")
dt0001.write_to_file()

# gravity in m/s^2
gEarth = TestCase(g=9.80, description="Gravity 9.80")
gEarth.write_to_file()
gNeptune = TestCase(g=11.15, description="Gravity 11.15")
gNeptune.write_to_file()
gVenus = TestCase(g=8.87, description="Gravity 8.87")
gVenus.write_to_file()
gMars = TestCase(g=3.71, description="Gravity 3.71")
gMars.write_to_file()
gMoon = TestCase(g=1.62, description="Gravity 1.62")
gMoon.write_to_file()

# horizontal angle from +z-axis to +x-axis
angle12 = TestCase(horizontal_angle=math.radians(1.2), description="Horizontal angle (deg) 1.2")
angle12.write_to_file()
angle6 = TestCase(horizontal_angle=math.radians(0.6), description="Horizontal angle (deg) 0.6")
angle6.write_to_file()
straight = TestCase(horizontal_angle=math.radians(0), description="Horizontal angle (deg) 0")
straight.write_to_file()
angle_6 = TestCase(horizontal_angle=math.radians(-0.6), description="Horizontal angle (deg) -0.6")
angle_6.write_to_file()
angle_12 = TestCase(horizontal_angle=math.radians(-1.2), description="Horizontal angle (deg) -1.2")
angle_12.write_to_file()

# extras for fun
pure_side_spin_clockwise_slow = TestCase(initial_speed=3, spin_rate=2*math.pi*200, spin_axis_angle_up=math.radians(0), spin_axis_angle_side=math.radians(180), description="Pure side spin clockwise slow")
pure_side_spin_clockwise_slow.write_to_file()
pure_side_spin_clockwise = TestCase(spin_rate=2*math.pi*200, spin_axis_angle_up=math.radians(0), spin_axis_angle_side=math.radians(180), description="Pure side spin clockwise")
pure_side_spin_clockwise.write_to_file()
pure_side_spin_anticlockwise = TestCase(spin_rate=2*math.pi*200, spin_axis_angle_up=math.radians(0), spin_axis_angle_side=math.radians(0), description="Pure side spin anticlockwise")
pure_side_spin_anticlockwise.write_to_file()
high_off_spin = TestCase(spin_rate=2*math.pi*100, description="High off spin")
high_off_spin.write_to_file()
high_leg_spin = TestCase(spin_axis_angle_side=math.radians(-45), spin_rate=2*math.pi*100, description="High leg spin")
high_leg_spin.write_to_file()
high_top_spin = TestCase(spin_rate=2*math.pi*200, spin_axis_angle_up=math.radians(0), spin_axis_angle_side=math.radians(90), description="High top spin and slow")
high_top_spin.write_to_file()
high_back_spin = TestCase(spin_rate=2*math.pi*200, spin_axis_angle_up=math.radians(180), spin_axis_angle_side=math.radians(90), description="High back spin (vector flip)")
high_back_spin.write_to_file()
high_back_spin = TestCase(spin_rate=2*math.pi*-200, spin_axis_angle_up=math.radians(0), spin_axis_angle_side=math.radians(90), description="High back spin (sign of rate flip)")
high_back_spin.write_to_file()
high_back_spin.write_to_file()

print("Generated all test cases.")