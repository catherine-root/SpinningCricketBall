import math

class TestCase:
    def __init__(self, dt=0.01, g=9.80, rho=1.225, k_d=0.5, initial_speed=18.5, elevation_angle=math.radians(10), horizontal_angle=math.radians(0), spin_rate=56*math.pi, spin_axis_angle_up=math.radians(10), spin_axis_angle_side=math.radians(60), description=""): 
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
    f.write("dt;g;k_d;initial_speed;elevation_angle;horizontal_angle;spin_rate;spin_angle;description\n")


# TODO: add leg spin cases - these are all off-spin only
default_off = TestCase(description="Default off spin")
default_off.write_to_file()

default_leg = TestCase(spin_axis_angle_side=math.radians(360-45), description="Default leg spin")
default_leg.write_to_file()

no_spin = TestCase(spin_rate=0, description="No spin")
no_spin.write_to_file()

no_flight = TestCase(initial_speed=0, description="No flight")
no_flight.write_to_file()

no_drag = TestCase(k_d=0, description="No drag")
no_drag.write_to_file() # also do big
# do zero drag with each of the default, no spin, no flight

no_elevation = TestCase(elevation_angle=0, description="No elevation angle")
no_elevation.write_to_file()

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
# for later comparison with each other
spin_rate = 20
spin_rate20 = TestCase(spin_rate=spin_rate, description="Spin rate 20")
spin_rate20.write_to_file()
spin_rate150 = TestCase(spin_rate=150, description="Spin rate 150")
spin_rate150.write_to_file()
spin_rate160 = TestCase(spin_rate=160, description="Spin rate 160")
spin_rate160.write_to_file()
spin_rate170 = TestCase(spin_rate=170, description="Spin rate 170")
spin_rate170.write_to_file()
spin_rate180 = TestCase(spin_rate=180, description="Spin rate 180")
spin_rate180.write_to_file()
# find range - ensure realistic - overlay as 2D plot

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

# Non-pro stats from https://researchers.mq.edu.au/en/publications/measuring-spin-characteristics-of-a-cricket-ball/
# off spin
# initial speed set to average speed!!!!!!!!!!!!!!!!!!!! ?????????????????????????????
state_squad_player = TestCase(initial_speed=19.8, spin_rate=2*math.pi*27.2, elevation_angle=math.radians(11.4), horizontal_angle=math.radians(180-48.2), description="Off-spin Player 1")
state_squad_player.write_to_file()
first_grade_club_player1 = TestCase(initial_speed=19.5, spin_rate=2*math.pi*26.8, elevation_angle=math.radians(14.8), horizontal_angle=math.radians(180-62), description="Off-spin Player 2.1")
first_grade_club_player1.write_to_file()
first_grade_club_player2 = TestCase(initial_speed=18.1, spin_rate=2*math.pi*28.3, elevation_angle=math.radians(2.6), horizontal_angle=math.radians(180-60.4), description="Off-spin Player 2.2")
first_grade_club_player2.write_to_file()
third_grade_club_player1 = TestCase(initial_speed=16.9, spin_rate=2*math.pi*20.2, elevation_angle=math.radians(17.1), horizontal_angle=math.radians(180-64.9), description="Off-spin Player 3")
third_grade_club_player1.write_to_file()
part_time_player = TestCase(initial_speed=17.2, spin_rate=2*math.pi*16.4, elevation_angle=math.radians(12.1), horizontal_angle=math.radians(180-126.8), description="Off-spin Player 4")
part_time_player.write_to_file()

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
# TODO: add air densities too / frictions
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

# horizontal angle with -ve x-axis
angle60 = TestCase(horizontal_angle=math.radians(60), description="Horizontal angle (deg) 60")
angle60.write_to_file()
angle75 = TestCase(horizontal_angle=math.radians(75), description="Horizontal angle (deg) 75")
angle75.write_to_file()
straight = TestCase(horizontal_angle=math.radians(90), description="Horizontal angle (deg) 90")
straight.write_to_file()
angle120 = TestCase(horizontal_angle=math.radians(120), description="Horizontal angle (deg) 120")
angle120.write_to_file()
angle135 = TestCase(horizontal_angle=math.radians(135), description="Horizontal angle (deg) 135")
angle135.write_to_file()

# extras for fun
high_back_spin = TestCase(spin_rate=-500, description="High back spin")
high_back_spin.write_to_file()

print("Generated all test cases.")