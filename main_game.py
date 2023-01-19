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
from inventory_class import Inventory
from dead_class import dead

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_stats = pygame.sprite.Group()
inventory_group = pygame.sprite.Group()
fps = 10


def main_game(screen, name_level):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map(name_level,
                    list(map(lambda x: x + 1, free_tiles)), 50)
    start_pos = (64, 64)
    player = Player(*start_pos, map_level, enemy_group, player_group)
    player.speed_1 = 35 / fps
    player.speed_2 = player.speed_1 * 2
    DowerChest((100, 70), screen, player, all_sprites)
    Health((1300, 800), player, screen, player_stats)
    Stamina((1300, 820), player, screen, player_stats)
    camera = Camera(screen, start_pos, map_level.width * map_level.tile_size, map_level.height * map_level.tile_size,
                    player.speed)
    print(camera.map_w, camera.map_h, map_level.width, map_level.height, map_level.tile_size)
    print(120 * 32, 64 * 32)
    Enemy(120, 120, map_level, player, enemy_group, all_sprites)
    inventory = Inventory(screen, player, screen.get_width() // 2, 0, inventory_group)
    finish = Finish((1845, 75), player, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings(screen)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        inventory.change_open()
        screen.fill('black')
        camera.update(player)
        map_level.render(screen, *camera.apply())
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        player_group.draw(screen)
        player_stats.draw(screen)
        player_group.update(pygame.key.get_pressed())
        if player.deads:
            for x in all_sprites:
                x.kill()
            for x in player_group:
                x.kill()
            return dead(screen)
        player_stats.update()
        if inventory.open_check:
            inventory_group.update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
            print(pygame.mouse.get_pos())
            inventory_group.draw(screen)
        if finish.is_finish():
            print('FINISH')
            exit()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_game(screen, 'project_of_map.tmx')
