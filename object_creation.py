from Rec_class import Rectangle, Circle, Player
from read_values import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Volley Pong")
icon = pygame.image.load("VP_icon.jpg")
pygame.display.set_icon(icon)

NET_height = 350
NET_width = 20
NET = Rectangle(NET_width, NET_height, (255, 255, 255), (SCREEN_WIDTH+NET_width)/2, SCREEN_HEIGHT-65-NET_height)
NET.create_shape()

player_mouse = Player(50, 50, (0, 255, 255))
player_mouse.create_shape()

height = 25
player_key = Player(125, height, (0, 255, 255), 100, SCREEN_HEIGHT-65-height)
player_key.create_shape()


com = Player(125, height, (0, 255, 255), 900, SCREEN_HEIGHT-65-height)
com.create_shape()

ball = Rectangle(15, 15, (0, 255, 255))
ball.x = player_key.x + (player_key.width - ball.width)/2
ball.y = (player_key.y - ball.height)+1
ball.create_shape()

visual = Circle(20)


center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
radius = 20