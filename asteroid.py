'''
Creates asteroids that can be either Large(1), Medium(2), or Small(3)
Asteroids should be able to show, move in a specific direction
Release smaller asteroids
'''
import random
from constants import *
from vectors import Vector
import pygame

'''
vectors 
+/-   _mult  _normalize  _direction  _magnitude  

constants

GAME_WIDTH = 600
GAME_HEIGHT = 600
ASTEROID_LARGE_R = 55
ASTEROID_MEDIUM_R = 35
ASTEROID_SMALL_R = 15
ASTEROID_COLOR = (0, 0, 0)
FPS = 40
BACKGROUND_COLOR = (255, 255, 255)
'''

class Asteroid(object):
    small_r = ASTEROID_SMALL_R
    medium_r = ASTEROID_MEDIUM_R
    large_r = ASTEROID_LARGE_R
    color = ASTEROID_COLOR

    def __init__(self, size=3):
        self.location = Vector( (random.choice(range(GAME_WIDTH)), random.choice(range(GAME_HEIGHT))) )
        self.size = size
        self.direction = self.choose_random_direction()
        self.x_class = self.direction.classify_direction(direction = 'x')
        self.y_class = self.direction.classify_direction(direction = 'y')
        if self.size == 3:
            self.radius = Asteroid.large_r
        elif self.size == 2:
            self.radius = Asteroid.medium_r
        else:
            self.radius = Asteroid.small_r

    def choose_random_direction(self):
        ''' Creates a random direction for the asteroid to move in'''
        x_dir = random.random() * 2 - 1
        y_dir = random.random() * 2 - 1
        return Vector((x_dir, y_dir))

    # looping function
    # x + r / y + r is the center of the circle
    def loop_position(self):
        '''
        Ensures that the asteroid is heading towards the correct wall, then
        allows for it to travel a bit off screen, before appearing offscreen
        on the other side of the map
        '''

        if self.location.x > GAME_WIDTH and self.x_class != 'left': 
            self.location.x = 0 - self.radius * 2

        if self.location.x < 0 - self.radius * 2 and self.x_class != 'right':
            self.location.x = GAME_WIDTH + self.radius * 2

        if self.location.y > GAME_HEIGHT and self.y_class != 'up': 
            self.location.y = 0 - self.radius * 2

        if self.location.y < 0 - self.radius * 2 and self.y_class != 'down':
            self.location.y = GAME_HEIGHT + self.radius * 2

    def move(self):
        self.loop_position()
        self.location += self.direction


    def show(self, display):
        if self.size == 3:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.large_r, Asteroid.large_r], 2)

        elif self.size == 2:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.medium_r, Asteroid.medium_r])

        else:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.small_r, Asteroid.smaller_r])

    # need at add - asteroids should be able to explode and release 2 smaller versions of themselves
    # when the asteroids explode, the child asteroids should split based on the more important factor of their movement
    # for example, if the x-component of their velocity is the largest, they both inherit that x-component but then they
    # get a mirrored y component (this way they don't just entirely overlap)