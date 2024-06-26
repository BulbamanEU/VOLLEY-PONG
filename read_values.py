import json
from tkinter import messagebox
import pygame

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 680
SPEED = [1000, 1100, 1200, 1250]
PLAYER_ANGLE = [70, 65, 60, 60]
#COM_ANGLE = [180-angle for angle in PLAYER_ANGLE]
COM_ANGLE = [113, 115, 120, 120]
GRAVITY = 1000

def WARNING(error_file):
    messagebox.showwarning(title="Warning", message=(error_file+" is missing. Reinstall the game."))
    pygame.quit()

def get_values():
    try:
        with open("saved_values.json", "r") as file:
            config = json.load(file)

        TRAVEL_X = config["TRAVEL_X"]
        TRAVEL_Y = config["TRAVEL_Y"]
        travelling = config["travelling"]
        invert = config["invert"]
        ANGLE = config["ANGLE"]
        strength = config["strength"]
        dist_wall = config["dist_wall"]
        pause = config["pause"]
        start_time = config["start_time"]
        TURN_ON = config["TURN_ON"]

        return TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength, dist_wall, pause, start_time, TURN_ON

    except FileNotFoundError:
        WARNING('saved_values.json')


def update_values(TRAVEL_X, TRAVEL_Y,travelling, invert, ANGLE, strength, dist_wall, pause, start_time, TURN_ON):
    try:
        variables = {
            "TRAVEL_X": TRAVEL_X,
            "TRAVEL_Y": TRAVEL_Y,
            "travelling": travelling,
            "invert": invert,
            "ANGLE": ANGLE,
            "strength": strength,
            "dist_wall": dist_wall,
            "pause": pause,
            "start_time": start_time,
            "TURN_ON": TURN_ON
        }

        with open('saved_values.json', 'w') as json_file:
            json.dump(variables, json_file, indent=4)

    except FileNotFoundError:
        WARNING('saved_values.json')


def reset_values(source_file="start_value.json", destination_file="saved_values.json"):

    try:
        with open(source_file, 'r') as f:
            source_data = json.load(f)

        with open(destination_file, 'r') as f:
            destination_data = json.load(f)

        destination_data.update(source_data)

        with open(destination_file, 'w') as f:
            json.dump(destination_data, f, indent=4)

    except FileNotFoundError:
        WARNING(f"{source_file} or {destination_file}")

def reset_field(ball, player_key, com, visual):
    player_key.x = 100 + player_key.get_width()
    com.x = 900
    offset = com.get_height()/2
    ball.x = player_key.x - ball.get_width() / 2
    ball.y = player_key.y + offset
    player_key.rect.center = (player_key.x, player_key.y + offset)
    com.rect.center = (com.x + com.get_width()/2, com.y + offset)
    ball.rect.center = (ball.x, ball.y)
    visual.center = (ball.x, ball.y)
    player_key.x -= player_key.get_width()/2

def last_position(ball, com, player_key):
    try:
        variables = {
            "ball_x": ball.x,
            "ball_y": ball.y,
            "com_x": com.x,
            "player_x": player_key.x
        }

        with open('current_position.json', 'w') as json_file:
            json.dump(variables, json_file, indent=4)
    except FileNotFoundError:
        WARNING('current_position.json')

def get_last_position(ball, com, player_key):
    try:
        with open("current_position.json", "r") as file:
            config = json.load(file)

        ball.x = config["ball_x"]
        ball.y = config["ball_y"]
        com.x = config["com_x"]
        player_key.x = config["player_x"]
    except FileNotFoundError:
        WARNING("current_position.json")



