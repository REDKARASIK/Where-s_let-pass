import pygame

from class_map import Map
from dower_chest import DowerChest
from main_functions import terminate
from player_class import Player
from camera_class import Camera
from class_enemy import Enemy
from class_finish import Finish
from health_and_stamina_class import Health, Stamina
from settup import settings

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_stats = pygame.sprite.Group()
fps = 10


def main_game(screen, name_level):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    borders = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 78]
    free_tiles = [6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map(name_level, list(map(lambda x: x + 1, free_tiles)), list(map(lambda x: x + 1, borders)), 0)
    start_pos = (80, 800)
    player = Player(*start_pos, map_level, enemy_group, player_group)
    player.speed_1 = 35 / fps * 6
    player.speed_2 = player.speed_1 * 2
    DowerChest((100, 70), screen, player, all_sprites)
    Health((1300, 800), player, screen, player_stats)
    Stamina((1300, 820), player, screen, player_stats)
    camera = Camera(screen, start_pos, map_level.width * map_level.tile_size, map_level.height * map_level.tile_size,
                    player.speed)
    Enemy(120, 120, map_level, player, enemy_group, all_sprites)
    finish = Finish((1845, 75), player, all_sprites)
    map_level.render()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings(screen)
        screen.fill('black')
        camera.update(player)
        map_level.render(*camera.apply())
        map_level.borderlines.draw(screen)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        player_group.draw(screen)
        player_stats.draw(screen)
        player_group.update(pygame.key.get_pressed())
        player_stats.update()
        if finish.is_finish():
            print('FINISH')
            exit()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_game(screen, 'project_of_map.tmx')
