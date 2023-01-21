import pygame
from Button_class import Button
from main_functions import terminate

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()


def settings(screen):
    pygame.mouse.set_visible(True)
    color = pygame.Color('black')
    color.hsva = (100, 0, 100, 100)
    image = pygame.Surface((screen.get_width(), screen.get_height()))
    image.set_alpha(150)
    pygame.draw.rect(image, color, (0, 0, screen.get_width(), screen.get_width()))
    screen.blit(image, (0, 0))
    exit = Button('Выйти из игры', 0, 0, all_sprites)
    continuing = Button('Продолжить', 0, 0, all_sprites)
    start_screen = Button('Вернуться в меню', 0, 0, all_sprites)
    repeat = Button('Начать заново', 0, 0, all_sprites)
    exit.rect.x = screen.get_width() // 2 - exit.rect.w // 2
    exit.rect.y = screen.get_height() // 2 + exit.rect.h // 2 + 70
    continuing.rect.x = screen.get_width() // 2 - continuing.rect.w // 2
    continuing.rect.y = screen.get_height() // 2 - continuing.rect.h - 50
    start_screen.rect.x = screen.get_width() // 2 - start_screen.rect.w // 2
    start_screen.rect.y = screen.get_height() // 2 - continuing.rect.h + 95
    repeat.rect.x = screen.get_width() // 2 - repeat.rect.w // 2
    repeat.rect.y = screen.get_height() // 2 - continuing.rect.h + 25
    while True:
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    return
            if exit.click(event):
                terminate()
            if continuing.click(event):
                pygame.mouse.set_visible(False)
                return
            if start_screen.click(event):
                return 'start_screen'
            if repeat.click(event):
                return 1
        all_sprites.draw(screen)
        pygame.display.flip()
