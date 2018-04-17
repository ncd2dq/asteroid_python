from constants import *
from vectors import Vector 
import pygame
import math
import time

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
SPACESHIP_COLOR = (100, 0, 0)
FPS = 40
BACKGROUND_COLOR = (255, 255, 255)
'''

# left key rotates the ship counterclockwise
# right key rotates the ship clockwise
# forward key increases the speed
# backward key decreases the speed

# for a spaceship we are going to need 4 points
# it'll essentially be an isocelles triangle but instead of a 
# flat butt it'll  be indented a little bit to look like a paper airpline
# from a birdseye view
#  .
#    .   
#      .        .
#    .
#  .    

class SpaceShip(object):

    def __init__(self):
        middle_x = GAME_WIDTH / 2
        middle_y = GAME_HEIGHT / 2
        self.location = Vector((middle_x, middle_y))
        self.momentum_direction = Vector((0.0, 0.0))
        self.ship_direction = Vector((0.0, -1.0)) # potentially useless
        self.acceleration = Vector((0.0, 0.0))
        self.point_list = []
        self.calculate_vertices()

    def calculate_vertices(self):
        '''
        Calculates all 4 points that make up the spaceship
        '''
        head = (self.location.x + SPACESHIP_RADIUS, self.location.y)
        back = (self.location.x + SPACESHIP_RADIUS, self.location.y + SPACESHIP_HEIGHT - SPACESHIP_HEIGHT_OFFSET)
        left = (self.location.x, self.location.y + SPACESHIP_HEIGHT)
        right = (self.location.x + SPACESHIP_RADIUS * 2, self.location.y + SPACESHIP_HEIGHT)
        point_list = [head, left, back, right]
        self.point_list = point_list

    def loop_position(self, loop_offset):
        ''' 
        This method calculates the center point of the ship by finding the midpoint between
        the head of the ship and the back indent of the ship

        Since the self.point_list is all tuples and not vectors (because the pygame.polygon method
        needs just tuples), we have to first convert them all to vectors
        '''
        vector_list = []
        for point_pair in self.point_list:
            vector_list.append(Vector(point_pair))

        center_vector = vector_list[0] - vector_list[2]
        center_vector.x, center_vector.y = center_vector.x / 2, center_vector.y / 2
        midpoint = vector_list[0] - center_vector
        #print(midpoint)
        loop = False
        if midpoint.x >= GAME_WIDTH + loop_offset: # Works
            self.location = Vector((loop_offset * -1, self.location.y))
            loop = True
        elif midpoint.x <= loop_offset * -1:
            self.location = Vector((GAME_WIDTH, self.location.y))
            loop = True
        elif midpoint.y <= loop_offset * -1:
            self.location = Vector((self.location.x, GAME_HEIGHT))
            loop = True
        elif midpoint.y >= GAME_HEIGHT + loop_offset: # Works
            self.location = Vector((self.location.x, loop_offset * -1))
            loop = True
        if loop:
            print('loop')
            self.calculate_vertices()
            #time.sleep(3)

    def update(self):
        self.momentum_direction += self.acceleration
        self.location += self.momentum_direction
        self.acceleration = Vector((0.0, 0.0))

    def find_ship_orientation(self):
        #head left, back, right
        #Returns the unit direction that the ship is oriented
        ship_facing_vector = Vector(self.point_list[0]) - Vector(self.point_list[2])
        ship_facing_vector._normalize()
        return ship_facing_vector

    def boost(self, acceleration):
        self.acceleration = acceleration

    def convert_to_relative(self, to_convert):
        ''' This method converts all points in the point list
        to relative to the center of the ship, so that you 
        rotate around the center of the ship, not around the origin
        '''

        converted = []
        center = (self.location.x + SPACESHIP_RADIUS, self.location.y + SPACESHIP_RADIUS)

        for vertex in to_convert:
            new_x = vertex[0] - center[0]  ## problem is here one is a float
            new_y = vertex[1] - center[1]
            converted.append((new_x, new_y))
        return converted

    def convert_to_map(self, to_convert):

        converted = []
        center = (self.location.x + SPACESHIP_RADIUS, self.location.y + SPACESHIP_RADIUS)

        for vertex in to_convert:
            new_x = vertex[0] + center[0]
            new_y = vertex[1] + center[1]
            converted.append((new_x, new_y))

        return converted

    def rotate(self, theta):
        relative = self.convert_to_relative(self.point_list)
        convFactor =  math.pi / 180
        rotated = []

        for vertex in relative:
            new_x = vertex[0] * math.cos(theta * convFactor) - vertex[1] * math.sin(theta * convFactor)
            new_y = vertex[0] * math.sin(theta * convFactor) + vertex[1] * math.cos(theta * convFactor)
            rotated.append((new_x, new_y))

        self.point_list = self.convert_to_map(rotated)
        '''
        new_location = (self.location.x, self.location.y)
        relative = self.convert_to_relative(new_location)
        new_x = relative[0] * math.cos(theta * convFactor) - relative[1] * math.sin(theta * convFactor)
        new_y = relative[0] * math.sin(theta * convFactor) + relative[1] * math.cos(theta * convFactor)
        converted_back = self.convert_to_map((new_x, new_y))
        self.location = Vector((converted_back[0], converted_back[1]))
        '''

    def show(self, display):
        pygame.draw.polygon(display, SPACESHIP_COLOR, self.point_list, 2)

    def run(self, display, theta, ship_loop_offset):
        # ignoring boost / update / loop_position
        self.calculate_vertices()
        self.rotate(theta)
        self.update()
        self.loop_position(ship_loop_offset)
        self.show(display)