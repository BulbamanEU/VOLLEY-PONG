import math

def calculate_trajectory(initial_speed, gravity, launch_angle, time, initial_x=0, initial_y=0):
    launch_angle_rad = math.radians(launch_angle)

    initial_speed_x = initial_speed * math.cos(launch_angle_rad)

    initial_speed_y = initial_speed * math.sin(launch_angle_rad)

    x = initial_x + initial_speed_x * time
    y = initial_y + (initial_speed_y * time - 0.5 * gravity * time ** 2)
    return x, y