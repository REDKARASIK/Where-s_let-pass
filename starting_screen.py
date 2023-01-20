import sys
import pygame
import os
import random
from main_functions import load_image, terminate
from Button_class import Button

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def start_screen(screen, current_level):
    sound = pygame.mixer.Sound('data/start_screen.mp3')
    fps = 30
    clock = pygame.time.Clock()
    all_buttons = pygame.sprite.Group()
    intro_text = ["Where's let-pass?", '', 'Новая игра', 'Продолжить игру', 'Выйти из игры']
    fon = pygame.transform.scale(load_image('fon.jpg'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    new_game = Button(intro_text[2], 50, screen.get_height() / 2, all_buttons)
    if current_level:
        continue_game = Button(intro_text[3], 50, screen.get_height() / 2 + 70, all_buttons)
    else:
        continue_game = False
        font = pygame.font.Font(None, 50)
        text = font.render('Начните "Новую игру"', True, 'white')
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(screen, 'gray', (50, screen.get_height() / 2 + 70, text_w + 15 * 2, text_h + 15 * 2))
        screen.blit(text, (50 + 15, screen.get_height() / 2 + 70 + 15))
        pygame.draw.rect(screen, 'white', (50, screen.get_height() / 2 + 70, text_w + 15 * 2, text_h + 15 * 2), 2)
    exit_game = Button(intro_text[4], 50, screen.get_height() / 2 + 140, all_buttons)
    font = pygame.font.Font(None, 150)
    text = font.render(intro_text[0], True, 'white')
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (50, 50))
    sound.set_volume(0.6)
    sound.play(-1)
    while True:
        for event in pygame.event.get():
            all_buttons.update(event)
            if exit_game.click(event):
                terminate()
            if new_game.click(event):
                sound.stop()
                return 1
            if continue_game:
                if continue_game.click(event):
                    sound.stop()
                    return current_level + 1
        all_buttons.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    start_screen(screen, 0)
