import sqlite3
from main_functions import load_image, terminate
from Button_class import Button

import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def ending(screen):
    sound = pygame.mixer.Sound('data/end_music.mp3')
    sound.set_volume(0.6)
    pygame.mouse.set_visible(True)
    with sqlite3.connect('data/game_db.sqlite') as db_file:
        db_c = db_file.cursor()
        db_c.execute('update level set current_level = 0 where id = 1')
        score = db_c.execute('select score from score where id = 1').fetchall()[0][0]
        score_play = db_c.execute('select score from players_stats where id = 1').fetchall()[0][0]
    if score_play > score:
        db_c.execute(f'update score set score = {score_play} where id = 1')
        db_file.commit()
    fon = pygame.transform.scale(load_image('end_fon.jpg'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    all_buttons = pygame.sprite.Group()
    exit_game = Button('Выйти из игры', 0, 0, all_buttons)
    exit_game.rect.x = screen.get_width() / 2 - exit_game.rect.w
    exit_game.rect.y = screen.get_height() / 2 + exit_game.rect.h / 2 + 50
    menu = Button('Вернуться в меню', 0, 0, all_buttons)
    menu.rect.x = screen.get_width() / 2 - menu.rect.w + 30
    menu.rect.y = screen.get_height() / 2 + exit_game.rect.h / 2 - 30
    font = pygame.font.Font(None, 150)
    text = font.render('Вы прошли игру!', True, 'white')
    font2 = pygame.font.Font(None, 100)
    text1 = font2.render(f'Лучший результат: {score}', True, 'white')
    text2 = font2.render(f'Ваш результат: {score_play}', True, 'white')
    screen.blit(text1, (60, 300))
    screen.blit(text2, (60, 220))
    screen.blit(text, (60, 60))
    if score_play > score:
        font3 = pygame.font.Font(None, 50)
        text3 = font3.render('Новый рекорд!', True, 'white')
        screen.blit(text3, (1200, 60))
    sound.play(-1)
    while True:
        for event in pygame.event.get():
            all_buttons.update(event)
            if exit_game.click(event):
                terminate()
            if menu.click(event):
                sound.stop()
                return 'start_screen'
        all_buttons.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    ending(screen)
