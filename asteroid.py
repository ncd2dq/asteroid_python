'''
Creates asteroids that can be either Large(1), Medium(2), or Small(3)
Asteroids should be able to show, move in a specific direction
Release smaller asteroids
'''
import random
from constants import *
from vectors import Vector
import pygame
import math

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
    smallish_r = ASTEROID_SMALLISH_R
    medium_r = ASTEROID_MEDIUM_R
    large_r = ASTEROID_LARGE_R
    color = ASTEROID_COLOR

    def __init__(self, allowable_positions, size=4):
        if allowable_positions == None:
            self.location = Vector( (random.choice(range(GAME_WIDTH)), random.choice(range(GAME_HEIGHT))) )
        else:
            self.location = Vector( (random.choice(allowable_positions[0]), random.choice(allowable_positions[1])) )
        self.size = size
        self.direction = self.choose_random_direction()
        self.x_class = self.direction.classify_direction(direction = 'x')
        self.y_class = self.direction.classify_direction(direction = 'y')

        if self.size == 4:
            self.radius = Asteroid.large_r
        elif self.size == 3:
            self.radius = Asteroid.medium_r
        elif self.size == 2:
            self.radius = Asteroid.smallish_r
        else:
            self.radius = Asteroid.small_r

        self.destroyed = False # Wether or not a bullet has hit this asteroid

    def choose_random_direction(self):
        ''' Creates a random direction for the asteroid to move in'''
        x_dir = random.random() * 2 - 1
        y_dir = random.random() * 2 - 1
        return Vector((x_dir, y_dir))

    def birth_babies(self):
        '''
        Once this asteroid has been hit, before it is removed from the asteroid list, call
        this function and it will return the two child asteroids (if it is a large or medium asteroid)
        with the correct velocity / momentum / ect. or it will return nothing if the asteroid cannot be broken anymore
        '''
        convFactor =  math.pi / 180
        theta_1 = 45
        theta_2 = 315
        # No need to translate because the directions are already based on the 0,0 origin
        # Asteroid Baby 1
        new_x_1 = self.direction.x * math.cos(theta_1 * convFactor) - self.direction.y * math.sin(theta_1 * convFactor)
        new_y_1 = self.direction.x * math.sin(theta_1 * convFactor) + self.direction.y * math.cos(theta_2 * convFactor)
        # Asteroid Baby 2
        new_x_2 = self.direction.x * math.cos(theta_2 * convFactor) - self.direction.y * math.sin(theta_2 * convFactor)
        new_y_2 = self.direction.x * math.sin(theta_2 * convFactor) + self.direction.y * math.cos(theta_2 * convFactor) 

        dir1 = Vector((new_x_1, new_y_1))
        dir2 = Vector((new_x_2, new_y_2))

        dir1 = dir1._mult(ASTEROID_BREAK_SPEED_FACTOR)
        dir2 = dir2._mult(ASTEROID_BREAK_SPEED_FACTOR)

        # Create dummy babies with dummy position lists (alter code later to avoid needing this)
        dummy_positions = [0, 1, 2]
        dummy_positions = (dummy_positions, dummy_positions)
        new_size = self.size - 1
        baby_1, baby_2 = Asteroid(dummy_positions, size=new_size), Asteroid(dummy_positions, size=new_size)

        baby_1.location = self.location
        baby_2.location = self.location

        baby_1.direction = dir1
        baby_2.direction = dir2

        baby_1.x_class = baby_1.direction.classify_direction(direction = 'x')
        baby_1.y_class = baby_1.direction.classify_direction(direction = 'y')

        baby_2.x_class = baby_2.direction.classify_direction(direction = 'x')
        baby_2.y_class = baby_2.direction.classify_direction(direction = 'y')


        return baby_1, baby_2


    def rotate(self, theta):
        relative = self.convert_to_relative(self.point_list)
        convFactor =  math.pi / 180
        rotated = []

        for vertex in relative:
            new_x = vertex[0] * math.cos(theta * convFactor) - vertex[1] * math.sin(theta * convFactor)
            new_y = vertex[0] * math.sin(theta * convFactor) + vertex[1] * math.cos(theta * convFactor)
            rotated.append((new_x, new_y))

        self.point_list = self.convert_to_map(rotated)


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

        if self.size == 4:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.large_r * 2, Asteroid.large_r * 2], 2)
        elif self.size == 3:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.medium_r * 2, Asteroid.medium_r * 2], 2)

        elif self.size == 2:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.smallish_r * 2, Asteroid.smallish_r * 2], 2)

        else:
            pygame.draw.ellipse(display, Asteroid.color, [self.location.x, self.location.y, Asteroid.small_r * 2, Asteroid.small_r * 2], 2)

    # need at add - asteroids should be able to explode and release 2 smaller versions of themselves
    # when the asteroids explode, the child asteroids should split based on the more important factor of their movement
    # for example, if the x-component of their velocity is the largest, they both inherit that x-component but then they
    # get a mirrored y component (this way they don't just entirely overlap)
