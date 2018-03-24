'''
Creates asteroids that can be either Large(1), Medium(2), or Small(3)
Asteroids should be able to show, move in a specific direction
Release smaller asteroids
'''
import random
from constants import *
from vectors import Vector
import pygame

class Asteroid(object):
    small_r = ASTEROID_SMALL_R
    medium_r = ASTEROID_MEDIUM_R
    large_r = ASTEROID_LARGE_R
    color = ASTEROID_COLOR

    def __init__(self, size=3):
        self.location = Vector( (random.choice(range(GAME_WIDTH)), random.choice(range(GAME_HEIGHT))) )
        self.size = size


    def show(self, display):
        if self.size == 3:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.large_r, Asteroid.large_r])

        elif self.size == 2:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.medium_r, Asteroid.medium_r])

        else:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.small_r, Asteroid.smaller_r])