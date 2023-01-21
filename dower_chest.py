import random
import pygame
from main_functions import terminate
from main_functions import load_image
from player_class import Player
from class_map import Map
from item import Item




class DowerChest(pygame.sprite.Sprite):
    imageopen = pygame.transform.scale(load_image("chestopen.png", 'white'), (24, 24))
    imageclosed = pygame.transform.scale(load_image("chestclosed.png", 'white'), (24, 24))
    button_e = pygame.transform.scale(load_image('key_e.png', 'blue'), (20, 20))

    def __init__(self, item, pos, screen, player, *group):
        super().__init__(*group)
        self.group = group
        self.player = player
        self.screen = screen
        self.image = DowerChest.imageclosed
        self.item = item
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        if pygame.sprite.collide_rect(self, self.player) and self.image != DowerChest.imageopen:
            self.image_2 = pygame.Surface((21, 21))
            self.image_2.blit(DowerChest.button_e, (0, 0))
            self.screen.blit(self.image_2, (
                self.rect.x - self.image_2.get_width() / 2 + self.rect.w / 2, self.rect.y - self.image_2.get_height()))
        if pygame.sprite.collide_rect(self, self.player) and args[0][
            pygame.K_e] and self.image == DowerChest.imageclosed:
            self.image = DowerChest.imageopen
            Item(self.screen, self.rect.x + 4, self.rect.y + self.rect.h + 1, self.item, self.player, *self.group)

