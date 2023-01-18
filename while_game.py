import pygame
from main_game import main_game
from starting_screen import start_screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.init()
c = 0
while True:
    if c == 0:
        c = start_screen(screen, c)
    if c == 1:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        c = main_game(screen, 'first_level.tmx')
    if c == 2:
        # start level
        pass