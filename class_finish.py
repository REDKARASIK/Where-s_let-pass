# 128, 224
import pygame

from class_map import Map
from main_functions import load_image
from main_functions import terminate
from player_class import Player



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


