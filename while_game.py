import pygame
from main_game import main_game
from starting_screen import start_screen

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
c = 0
if c == 0:
    c = start_screen(screen, c)
if c == 1:
    main_game(screen, 'project_of_map.tmx')
if c == 2:
    # start level
    pass