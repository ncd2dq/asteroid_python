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
        self.direction = Vector((0,0))

    def calculate_vertices(self):
        # return the 3 points of the triangle in the format needed for the
        # show function
        pass

    def show(self, display):

        pygame.draw.polygon(display, SPACESHIP_COLOR, [(300,300),(300,400),(400,350)], 2)