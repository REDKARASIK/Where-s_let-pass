import pygame
from main_game import main_game
from starting_screen import start_screen
from end_screen import ending

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.init()
c = 'start_screen'
while True:
    screen.fill('black')
    if c == 'start_screen':
        c = start_screen(screen)
    if c < 4:
        screen.fill('black')
        c = main_game(screen, c)
    if c == 4:
        c = ending(screen)
