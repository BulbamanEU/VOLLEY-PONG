import pygame
from read_values import SCREEN_HEIGHT, SCREEN_WIDTH
from abc import abstractmethod
class Object():
    def __init__(self, color=(255,255,255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self.x = x
        self.y = y
        self.color = color

    def create_shape(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class Rectangle(Object):
    def __init__(self, width, height, color=(255,255,255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        super().__init__(color, x, y)
        self.height = height
        self.width = width

    def create_shape(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Circle(Object):
    def __init__(self, radius, color=(255,255,255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        super().__init__(color, x, y)
        self.center = (self.x, self.y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

class Player(Rectangle):
    def __init__(self, width, height, color=(255,255,255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        super().__init__(width, height, color, x, y)

    def is_inverted(func):
        def wrapper(self, *args, **kwargs):
            ball.y -= traveled_y
            if invert:
                ball.x += (dist_wall - traveled_x)
            else:
                ball.x += traveled_x
        return wrapper


    def move(self, traveled_x, traveled_y, invert, dist_wall=0):
        self.x += 2
        self.y += 2