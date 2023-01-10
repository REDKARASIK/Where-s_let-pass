import pygame
from player_class import Player
from main_functions import terminate
from class_map import Map
from dower_chest import DowerChest

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
fps = 20


def main_game(screen, name_level):
    clock = pygame.time.Clock()
    map_level = Map(name_level,
                    [7, 8, 9, 16, 18, 19, 29, 60, 61, 62, 63, 70, 71, 72, 73, 12, 13, 14, 22,
                     23, 24, 32, 33, 34, 20, 10, 29, 30, 17, 28, 27], 50)
    player = Player(64, 64, map_level, player_group)
    player.speed = 40 / fps
    DowerChest((100, 70), player, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        all_sprites.draw(screen)
        player_group.draw(screen)
        player_group.update(pygame.key.get_pressed())
        all_sprites.update(pygame.key.get_pressed())
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_game(screen, 'project_of_map.tmx')
