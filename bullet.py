import pygame
from vectors import Vector
from constants import *

class Bullet(object):
    def __init__(self, spaceship_tip, spaceship_facing):
        self.location = Vector((spaceship_tip[0], spaceship_tip[1]))
        self.direction = spaceship_facing
        self.fuel = BULLET_FUEL
        self.crashed = False

    def update(self):
        velocity = self.direction._mult(BULLET_SPEED)
        self.fuel -= velocity._magnitude()
        self.location += velocity

    def show(self, display):
        if not self.crashed:
            pygame.draw.ellipse(display, BULLET_COLOR, [self.location.x, self.location.y, BULLET_RADIUS * 2, BULLET_RADIUS * 2])

    def fuel_depletion(self):
        if self.fuel <= 0:
            self.crashed = True

    def loop_position(self, loop_offset=3):
        if self.location.x >= GAME_WIDTH + loop_offset: # Works
            self.location = Vector((loop_offset * -1, self.location.y))
            loop = True
        elif self.location.x <= loop_offset * -1:
            self.location = Vector((GAME_WIDTH, self.location.y))
            loop = True
        elif self.location.y <= loop_offset * -1:
            self.location = Vector((self.location.x, GAME_HEIGHT))
            loop = True
        elif self.location.y >= GAME_HEIGHT + loop_offset: # Works
            self.location = Vector((self.location.x, loop_offset * -1))

    def collide_with_asteroid(self, asteroid_list):
        for asteroid in asteroid_list:
            asteroid_center = (asteroid.location.x + asteroid.radius, asteroid.location.y + asteroid.radius)
            # circle equation (x - h)**2 + (y - k)**2 = r**2
            # center is at pooint (h,k)
            left_side = (self.location.x - asteroid_center[0]) ** 2 + (self.location.y - asteroid_center[1]) ** 2
            right_side = asteroid.radius ** 2
            if left_side <= right_side:
                self.crashed = True

    def run(self, display, asteroid_list):
        self.update()
        self.loop_position()
        self.show(display)
        self.fuel_depletion()
        self.collide_with_asteroid(asteroid_list)