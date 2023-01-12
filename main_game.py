import pygame

from class_map import Map
from dower_chest import DowerChest
from main_functions import terminate
from player_class import Player

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
fps = 10


def main_game(screen, name_level):
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map(name_level,
                    list(map(lambda x: x + 1, free_tiles)), 50)
    player = Player(64, 64, map_level, player_group)
    player.speed = 30 / fps
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
