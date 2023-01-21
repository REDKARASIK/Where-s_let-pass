import sqlite3

import pygame

from class_map import Map
from dower_chest import DowerChest
from main_functions import terminate, load_image
from player_class import Player
from camera_class import Camera
from class_enemy import *
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
delete_group = pygame.sprite.Group()
fps = 10
MAP_LEVELS = {1: 'first_level.tmx', 2: 'second_level2.tmx', 3: ''}


def main_game(screen, name_level):
    main_sound = pygame.mixer.Sound('data/start_music.mp3')
    dead_sound = pygame.mixer.Sound('data/dead.mp3')
    dead_play = False
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    borders = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55]
    map_level = Map(MAP_LEVELS[name_level],
                    list(map(lambda x: x + 101, free_tiles)), list(map(lambda x: x + 101, borders)), 50)
    if name_level == 1:
        start_pos = (64, 64)
        player = Player(*start_pos, map_level, enemy_group, player_group, delete_group)
        player.speed_1 = 150 / fps
        player.speed_2 = player.speed_1 * 2
        Health((1300, 800), player, screen, player_stats, delete_group)
        Stamina((1300, 820), player, screen, player_stats, delete_group)
        camera = Camera(screen, start_pos, map_level.width * map_level.tile_size,
                        map_level.height * map_level.tile_size,
                        player.speed)
        DowerChest('stamina chest', (70, 900), screen, player, all_sprites, delete_group)
        Enemy(150, 800, map_level, player, enemy_group, all_sprites, delete_group)
        Enemy(890, 890, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('medicine chest', (920, 600), screen, player, all_sprites, delete_group)
        DowerChest('fireball', (1160, 500), screen, player, all_sprites, delete_group)
        Enemy(1300, 500, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('medicine chest', (2000, 1350), screen, player, all_sprites, delete_group)
        Enemy(1600, 1450, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('stamina chest', (1000, 470), screen, player, all_sprites, delete_group)
        Enemy(1050, 1100, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('fireball', (995, 1065), screen, player, all_sprites, delete_group)
        Enemy(800, 1300, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('medicine chest', (650, 1250), screen, player, all_sprites, delete_group)
        Enemy(300, 1500, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('fireball', (250, 1450), screen, player, all_sprites, delete_group)
        Enemy(300, 1800, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('stamina chest', (250, 1860), screen, player, all_sprites, delete_group)
        Enemy(2500, 1800, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('fireball', (2650, 1850), screen, player, all_sprites, delete_group)
        Enemy(1950, 1800, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('fireball', (2990, 1550), screen, player, all_sprites, delete_group)
        Enemy(2900, 1500, map_level, player, enemy_group, all_sprites, delete_group)
        Enemy(2900, 1000, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('stamina chest', (2990, 1000), screen, player, all_sprites, delete_group)
        Enemy(2400, 1000, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('medicine chest', (2490, 1000), screen, player, all_sprites, delete_group)
        DowerChest('fireball', (3500, 1550), screen, player, all_sprites, delete_group)
        Enemy(3500, 1500, map_level, player, enemy_group, all_sprites, delete_group)
        Enemy(3600, 1000, map_level, player, enemy_group, all_sprites, delete_group)
        DowerChest('medicine chest', (3650, 850), screen, player, all_sprites, delete_group)
        DowerChest('fireball', (2700, 440), screen, player, all_sprites, delete_group)
        Enemy(2800, 450, map_level, player, enemy_group, all_sprites, delete_group)
        Enemy(3200, 250, map_level, player, enemy_group, all_sprites, delete_group)
        inventory = Inventory(screen, player, screen.get_width() // 2, 0, inventory_group, delete_group)
        finish = Finish((3700, 125), player, all_sprites, delete_group)
    fon_dead = pygame.transform.scale(load_image('Game_over.png'), (600, 600))
    alpha = 50
    fon_dead.set_alpha(alpha)
    main_sound.set_volume(0.04)
    volume = 0.01
    dead_sound.set_volume(volume)
    main_sound.play(-1)
    with sqlite3.connect('data/game_db.sqlite') as db_file:
        db_c = db_file.cursor()
        stats = db_c.execute('select * from players_stats').fetchall()[0]
    player.health = stats[1]
    player.max_health = stats[2]
    player.stamina = stats[4]
    player.max_stamina = stats[4]
    player.inventory['medical chest'] = stats[5]
    player.inventory['stamina chest'] = stats[6]
    player.inventory['fireball'] = stats[7]
    player.score = stats[8]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    c = settings(screen)
                    if c == 1:
                        pygame.mixer.stop()
                        for x in delete_group:
                            x.kill()
                        return name_level
                    if c == 'start_screen':
                        for x in delete_group:
                            x.kill()
                        return c
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        inventory.change_open()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory.open_check:
                    inventory.take_from(pygame.mouse.get_pos())
        screen.fill('black')
        camera.update(player)
        map_level.wall_group.draw(screen)
        map_level.render(screen, *camera.apply())
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        player_group.draw(screen)
        player_stats.draw(screen)
        player_group.update(pygame.key.get_pressed())
        if player.timer != 0:
            main_sound.stop()
            if not dead_play:
                dead_sound.play(-1)
                dead_play = True
            dead_sound.set_volume(volume)
            screen.blit(fon_dead, (screen.get_width() / 2 - 300, -100))
            alpha += 50
            volume += 0.006
            fon_dead.set_alpha(alpha)
        if player.deads:
            for x in delete_group:
                x.kill()
            return dead(screen, name_level)
        player_stats.update()
        if inventory.open_check:
            inventory_group.update()
            inventory_group.draw(screen)
        if finish.is_finish():
            player.score += 20
            with sqlite3.connect('data/game_db.sqlite') as db_file:
                db_f = db_file.cursor()
                db_f.execute(f'update level set current_level = {name_level + 1} where id = 1')
                db_f.execute(
                    f'update players_stat set helth = {player.health}, medical = {player.inventory["medical chest"]}, energy = {player.inventory["stamina chest"]}, fireball = {player.inventory["fireball"]}, score : {player.score}')
                db_file.commit()
            return name_level + 1
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_game(screen, 1)
