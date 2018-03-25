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
        self.ship_direction = Vector((0.0, -1.0))
        self.acceleration = Vector((0.0, 0.0))
        self.point_list = self.calculate_vertices()

    def calculate_vertices(self):
        '''
        Calculates all 4 points that make up the spaceship
        '''
        head = (self.location.x, self.location.y)
        back = (self.location.x, self.location.y + SPACESHIP_HEIGHT - SPACESHIP_HEIGHT_OFFSET)
        left = (self.location.x - SPACESHIP_RADIUS, self.location.y + SPACESHIP_HEIGHT)
        right = (self.location.x + SPACESHIP_RADIUS, self.location.y + SPACESHIP_HEIGHT)
        point_list = [head, left, back, right]
        self.point_list = point_list

        return point_list

    def loop_position(self):
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


    def update(self):
        self.momentum_direction += self.acceleration
        self.location += self.momentum_direction
        self.acceleration = Vector((0.0, 0.0))


    def boost(self, acceleration):
        self.acceleration = acceleration

    def rotate(self, direction):
        pass

    def show(self, display):
        point_list = self.calculate_vertices()
        pygame.draw.polygon(display, SPACESHIP_COLOR, point_list, 2)