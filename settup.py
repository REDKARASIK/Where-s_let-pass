import pygame
from Button_class import Button
from main_functions import terminate

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()


def settings(screen):
    color = pygame.Color('black')
    color.hsva = (100, 0, 100, 100)
    image = pygame.Surface((screen.get_width(), screen.get_height()))
    pygame.draw.rect(image, color, (0, 0, screen.get_width(), screen.get_width()))
    screen.blit(image, (0, 0))
    exit = Button('Выйти из игры', 0, 0, all_sprites)
    continuing = Button('Продолжить', 0, 0, all_sprites)
    exit.rect.x = screen.get_width() // 2 - exit.rect.w // 2
    exit.rect.y = screen.get_height() // 2 + exit.rect.h // 2 + 50
    continuing.rect.x = screen.get_width() // 2 - continuing.rect.w // 2
    continuing.rect.y = screen.get_height() // 2 - continuing.rect.h - 40
    while True:
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if exit.click(event):
                terminate()
            if continuing.click(event):
                return
        all_sprites.draw(screen)
        pygame.display.flip()
