import pygame
from read_values import SCREEN_HEIGHT, SCREEN_WIDTH
from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def create_shape(self):
        pass

class ObjectFactory(ABC):
    @abstractmethod
    def create_object(self):
        pass

class Rectangle(GameObject):
    def __init__(self, width, height, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._width = width
        self._height = height
        self._color = color
        self.x = x
        self.y = y
        self.create_shape()

    def create_shape(self):
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

class Circle(GameObject):
    def __init__(self, radius, center, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._radius = radius
        self._color = color
        self.x = x
        self.y = y
        self.center = center

    def draw(self, screen):
        pygame.draw.circle(screen, self._color, self.center, self._radius)

    def create_shape(self):
        pass

    def get_radius(self):
        return self._radius

class RectangleFactory(ObjectFactory):
    def __init__(self, width, height, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._width = width
        self._height = height
        self._color = color
        self._x = x
        self._y = y

    def create_object(self):
        return Rectangle(self._width, self._height, self._color, self._x, self._y)

class CircleFactory(ObjectFactory):
    def __init__(self, radius, center, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._radius = radius
        self._color = color
        self._x = x
        self._y = y
        self.center = center

    def create_object(self):
        return Circle(self._radius, self.center, self._color, self._x, self._y)

class Player(GameObject):
    def __init__(self, width, height, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._width = width
        self._height = height
        self._color = color
        self.x = x
        self.y = y
        self.create_shape()

    def create_shape(self):
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

class PlayerBuilder():
    def __init__(self):
        self._width = 125
        self._height = 25
        self._color = (0, 255, 255)
        self._x = SCREEN_WIDTH / 2
        self._y = SCREEN_HEIGHT - 65 - self._height

    def set_width(self, width):
        self._width = width
        return self

    def set_height(self, height):
        self._height = height
        return self

    def set_color(self, color):
        self._color = color
        return self

    def set_position(self, x, y):
        self._x = x
        self._y = y
        return self

    def build(self):
        return Player(self._width, self._height, self._color, self._x, self._y)

def draw_object(obj, screen):
    obj.draw(screen)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Volley Pong")
icon = pygame.image.load("VP_icon.jpg")
pygame.display.set_icon(icon)


NET_height = 350
NET_width = 20
height = 25
center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
radius = 20

rectangle_factory = RectangleFactory(20, 350, (255, 255, 255), (SCREEN_WIDTH+20)/2, SCREEN_HEIGHT-65-350)

player_builder = PlayerBuilder()
player_builder.set_color((255, 0, 0))
player_builder.set_position(100, 100)

com_factory = RectangleFactory(125, 25, (0, 255, 255), 900, SCREEN_HEIGHT-65-25)
ball_factory = RectangleFactory(15, 15, (0, 255, 255))
visual_factory = CircleFactory(radius, center, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

NET = rectangle_factory.create_object()
player_key = player_builder.build()
com = com_factory.create_object()
ball = ball_factory.create_object()
visual = visual_factory.create_object()
