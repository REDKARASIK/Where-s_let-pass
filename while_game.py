import pygame
from main_game import main_game
from starting_screen import start_screen

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.init()
c = 'start_screen'
while True:
    screen.fill('black')
    if c == 'start_screen':
        c = start_screen(screen)
    if c < 6:
        screen.fill('black')
        c = main_game(screen, c)
    if c == 6:
        pass
