import pygame
from constants import *
from asteroid import Asteroid
from ship import SpaceShip
from vectors import Vector
import time
from bullet import Bullet
#SHIP_ACCEL
def setup(WIDTH, HEIGHT):
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    return display, clock

def events(spaceship, bullets):

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

            if event.key == 32: #SPACE BAR
                ship_tip = spaceship.point_list[0]
                ship_dir = spaceship.find_ship_orientation()
                bullets.append(Bullet(ship_tip, ship_dir))
                #ship.find_ship_orientation  returns a vector
                #ship.point_list[0]   is ships head location



def create_game_end_message(display):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render('You Crashed!', False, (255, 0, 0))
    display.blit(textsurface, (GAME_WIDTH / 3, GAME_HEIGHT / 2))

# allowable_positions = ([full_x_coords], [full_y_coords])
def main():
    display, clock = setup(GAME_WIDTH, GAME_HEIGHT)
    allowable_x_1 = list(range(GAME_WIDTH // 3))
    allowable_x_2 = list(range(GAME_WIDTH * 2 // 3, GAME_WIDTH))
    allowable_y_1 = list(range(GAME_HEIGHT // 3))
    allowable_y_2 = list(range(GAME_HEIGHT * 2 // 3, GAME_HEIGHT))
    allowable_asteroid_positions = (allowable_x_1 + allowable_x_2, allowable_y_1 + allowable_y_2)
    asteroids = [Asteroid(allowable_asteroid_positions) for iter in range(5)]
    spaceship = SpaceShip()
    bullets = []
    global angle 
    global angle_change
    angle_change = 0
    angle = 0

    while True:
        display.fill(BACKGROUND_COLOR)
        events(spaceship, bullets)
        for asteroid in asteroids:
            asteroid.show(display)
            asteroid.move()

        for bullet in bullets:
            bullet.run(display, asteroids)
            if bullet.crashed:
                bullets.remove(bullet)

        spaceship.run(display, angle, SHIP_LOOP_OFFSET, asteroids)

        if spaceship.crashed:
            asteroids = [Asteroid(allowable_asteroid_positions) for iter in range(5)]
            spaceship = SpaceShip()
            bullets = []
            create_game_end_message(display)
            pygame.display.update()
            time.sleep(3)

        angle += angle_change
        pygame.display.update()
        clock.tick(FPS)
        
        
if __name__ == '__main__':
    main()


