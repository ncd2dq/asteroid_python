import pygame
from constants import *
from asteroid import Asteroid

def setup(WIDTH, HEIGHT):
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    return display, clock

def events():

    global game_exit

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
            pygame.display.quit()
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_LEFT:
                pass
        if event.type == pygame.KEYDOWN:
            pass


def main():
    display, clock = setup(GAME_WIDTH, GAME_HEIGHT)
    asteroids = [Asteroid() for iter in range(5)]

    while True:
        display.fill(BACKGROUND_COLOR)
        events()
        
        for asteroid in asteroids:
            asteroid.show(display)
            
        pygame.display.update()
        clock.tick(FPS)
        
        
if __name__ == '__main__':
    main()


