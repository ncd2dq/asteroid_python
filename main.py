import pygame
from constants import *
from asteroid import Asteroid
from ship import SpaceShip
from vectors import Vector
#SHIP_ACCEL
def setup(WIDTH, HEIGHT):
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    return display, clock

def events(spaceship):

    global game_exit
    global angle_change

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
            pygame.display.quit()
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                accelerate_vector = spaceship.find_ship_orientation()
                spaceship.boost(accelerate_vector)
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_RIGHT:
                angle_change = 0
            if event.key == pygame.K_LEFT:
                angle_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                accelerate_vector = spaceship.find_ship_orientation()
                spaceship.boost(accelerate_vector)
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_RIGHT:
                angle_change = 5
            if event.key == pygame.K_LEFT:
                angle_change = -5

def main():
    display, clock = setup(GAME_WIDTH, GAME_HEIGHT)
    asteroids = [Asteroid() for iter in range(5)]
    spaceship = SpaceShip()
    global angle 
    global angle_change
    angle_change = 0
    angle = 0

    while True:
        display.fill(BACKGROUND_COLOR)
        events(spaceship)
        for asteroid in asteroids:
            asteroid.show(display)
            asteroid.move()

        spaceship.run(display, angle, SHIP_LOOP_OFFSET)

        angle += angle_change
        pygame.display.update()
        clock.tick(FPS)
        
        
if __name__ == '__main__':
    main()


