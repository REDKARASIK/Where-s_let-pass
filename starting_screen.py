import sys
import pygame
import os
import random
from Button_class import Button

pygame.init()


def start_screen(screen, current_level):
    intro_text = ["Where's let-pass?", '', 'Новая игра', 'Продолжить игру', 'Выйти из игры']


class NewGameButton(Button):
    def __init__(self, text, pos_x, pos_y, *group):
        super().__init__(text, pos_x, pos_y, *group)

    def start_game(self):
        pass