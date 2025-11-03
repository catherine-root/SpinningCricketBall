import math

class TestCase:
    def __init__(self, dt=0.01, k_d=0.5, initial_speed=22.4, elevation_angle=math.radians(30), horiztonal_angle=math.radians(90), initial_omega=[170,0], description=""):
        self.dt = dt
        self.k_d = k_d  # drag coefficient is multiplicative factor in drag force calculation
        self.initial_speed = initial_speed
        self.elevation_angle = elevation_angle
        self.horiztonal_angle = horiztonal_angle
        self.initial_omega = initial_omega
        self.description = description

    def __repr__(self):
        return f"TestCase(dt={self.dt}, k_d={self.k_d}, initial_speed={self.initial_speed}, elevation_angle={self.elevation_angle}, horiztonal_angle={self.horiztonal_angle}, initial_omega={self.initial_omega}, description='{self.description}')"

    def write_to_file(self):
        with open("test_cases.txt", "a") as f:
            f.write(f"{self.dt};{self.k_d};{self.initial_speed};{self.elevation_angle};{self.horiztonal_angle};{self.initial_omega[0]};{self.initial_omega[1]};{self.description}\n")


with open("test_cases.txt", "w") as f:
    f.write("dt;k_d;initial_speed;elevation_angle;horiztonal_angle;initial_omega_x;initial_omega_y;description\n")

default = TestCase(description="Default off spin")
default.write_to_file()

no_spin = TestCase(initial_omega=[0,0], description="No spin")
no_spin.write_to_file()

no_flight = TestCase(initial_speed=0, description="No flight")
no_flight.write_to_file()

no_drag = TestCase(k_d=0, description="No drag")
no_drag.write_to_file() # also do big
# do zero drag with each of the default, no spin, no flight

no_elevation = TestCase(elevation_angle=0, description="No elevation angle")
no_elevation.write_to_file()

# for later comparison with each other
spin_rate140 = TestCase(initial_omega=[140,0], description="Spin rate 140")
spin_rate140.write_to_file()
spin_rate150 = TestCase(initial_omega=[150,0], description="Spin rate 150")
spin_rate150.write_to_file()
spin_rate160 = TestCase(initial_omega=[160,0], description="Spin rate 160")
spin_rate160.write_to_file()
spin_rate170 = TestCase(initial_omega=[170,0], description="Spin rate 170")
spin_rate170.write_to_file()
spin_rate180 = TestCase(initial_omega=[180,0], description="Spin rate 180")
spin_rate180.write_to_file()
# find range - ensure realistic - overlay as 2D plot

speed18 = TestCase(initial_speed=18, description="Initial speed 18")
speed18.write_to_file()
speed20 = TestCase(initial_speed=20, description="Initial speed 20")
speed20.write_to_file()
speed22 = TestCase(initial_speed=22, description="Initial speed 22")
speed22.write_to_file()
speed24 = TestCase(initial_speed=24, description="Initial speed 24")
speed24.write_to_file()
speed26 = TestCase(initial_speed=26, description="Initial speed 26")
speed26.write_to_file()

# extras for fun
high_back_spin = TestCase(initial_omega=[-500,0], description="High back spin")
high_back_spin.write_to_file()
