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
                accelerate_vector = spaceship.find_ship_orientation()
                accelerate_vector = accelerate_vector._mult(-1)
                spaceship.boost(accelerate_vector)
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

class GameStats(object):
    def __init__(self):
        self.level = 1
        self.score = 0
        self.level_show, self.score_show = self.create_messages(self.level, self.score)

    def create_messages(self, level, score):
        pygame.font.init()
        myfontLevel = pygame.font.SysFont('Comic Sans MS', 25)
        myfontScore = pygame.font.SysFont('Comic Sans MS', 25)
        levelSurface = myfontLevel.render('Level: {}'.format(str(level)), False, (0, 0, 0))
        scoreSurface = myfontScore.render('Score: {}'.format(str(score)), False, (0, 0, 0))
        return levelSurface, scoreSurface

    def show(self, display):
        self.level_show, self.score_show = self.create_messages(self.level, self.score)
        display.blit(self.level_show, (LEVEL_MESSAGE_X, LEVEL_MESSAGE_Y))
        display.blit(self.score_show, (SCORE_MESSAGE_X, SCORE_MESSAGE_Y))

def create_level_advance_message(display):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render('Next Level!', False, (0, 255, 0))
    display.blit(textsurface, (CRASH_MESSAGE_X, CRASH_MESSAGE_Y))

def create_game_end_message(display):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render('You Crashed!', False, (255, 0, 0))
    display.blit(textsurface, (CRASH_MESSAGE_X, CRASH_MESSAGE_Y))

# allowable_positions = ([full_x_coords], [full_y_coords])
def main():
    display, clock = setup(GAME_WIDTH, GAME_HEIGHT)
    allowable_x_1 = list(range(GAME_WIDTH // 3))
    allowable_x_2 = list(range(GAME_WIDTH * 2 // 3, GAME_WIDTH))
    allowable_y_1 = list(range(GAME_HEIGHT // 3))
    allowable_y_2 = list(range(GAME_HEIGHT * 2 // 3, GAME_HEIGHT))
    allowable_asteroid_positions = (allowable_x_1 + allowable_x_2, allowable_y_1 + allowable_y_2)
    asteroids = [Asteroid(allowable_asteroid_positions) for iter in range(ASTEROID_COUNT)]
    spaceship = SpaceShip()
    bullets = []
    global angle 
    global angle_change
    angle_change = 0
    angle = 0
    baby_asteroids = []
    stats = GameStats()

    while True:
        display.fill(BACKGROUND_COLOR)
        events(spaceship, bullets)
        for asteroid in asteroids:
            asteroid.show(display)
            asteroid.move()

        for asteroid in asteroids:
            if asteroid.destroyed:
                stats.score += 1
                if asteroid.size >= 2:
                    baby_1, baby_2 = asteroid.birth_babies()
                    asteroids.remove(asteroid)
                    baby_asteroids.append(baby_1)
                    baby_asteroids.append(baby_2)
                else:
                    asteroids.remove(asteroid)
        else:
            asteroids += baby_asteroids
            baby_asteroids = []

        for bullet in bullets:
            bullet.run(display, asteroids)
            if bullet.crashed:
                bullets.remove(bullet)

        spaceship.run(display, angle, SHIP_LOOP_OFFSET, asteroids)
        stats.show(display)

        if spaceship.crashed:
            asteroids = [Asteroid(allowable_asteroid_positions) for iter in range(ASTEROID_COUNT)]
            spaceship = SpaceShip()
            bullets = []
            stats = GameStats()
            ASTEROID_BREAK_SPEED_FACTOR = INITIAL_SPEED_FACTOR
            ADDITIONAL_ASTEROIDS = INITIAL_ADDITIONAL_ASTEROIDS

            create_game_end_message(display)
            pygame.display.update()
            time.sleep(3)


        if len(asteroids) == 0:
            ADDITIONAL_ASTEROIDS += INITIAL_ADDITIONAL_ASTEROIDS
            ASTEROID_BREAK_SPEED_FACTOR *= INITIAL_SPEED_FACTOR
            asteroids = [Asteroid(allowable_asteroid_positions) for iter in range(ADDITIONAL_ASTEROIDS)]
            spaceship = SpaceShip()
            bullets = []
            stats.level += 1
            create_level_advance_message(display)
            pygame.display.update()
            time.sleep(2)


        angle += angle_change
        pygame.display.update()
        clock.tick(FPS)
        
        
if __name__ == '__main__':
    main()


