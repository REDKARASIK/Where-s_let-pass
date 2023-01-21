import sqlite3

import pygame

from class_map import Map
from dower_chest import DowerChest
from main_functions import terminate, load_image
from player_class import Player
from camera_class import Camera
from class_enemy import *
from health_and_stamina_class import Health, Stamina
from settup import settings
from inventory_class import Inventory
from dead_class import dead


class Finish(pygame.sprite.Sprite):
    def __init__(self, pos, player, *group):
        super().__init__(*group)
        self.player = player
        self.image = pygame.transform.scale(load_image("finish.png", 'white'), (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def is_finish(self):
        # image = pygame.Surface([self.player.rect.width - 40, self.player.rect.height])
        # sprite = pygame.sprite.Sprite()
        # sprite.image = image
        # sprite.rect = image.get_rect()
        # sprite.rect.x = self.player.rect.x + 40
        # sprite.rect.y = self.player.rect.y
        self.player.mask = pygame.mask.from_surface(self.player.image)
        if pygame.sprite.collide_mask(self, self.player):
            return 1


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()
    all_enemy = pygame.sprite.Group()
    fps = 25
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1, free_tiles)), [1], 1)
    player = Player(64, 64, map_level, all_enemy, all_sprites)
    enemy = Enemy(120, 120, map_level, player, all_enemy)
    Finish((64, 64), player, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        all_enemy.update(player)
        all_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
