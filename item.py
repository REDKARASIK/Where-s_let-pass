import random

import pygame
from main_functions import load_image

pygame.init()


class Item(pygame.sprite.Sprite):
    medicine = pygame.transform.scale(load_image('first-aid-kit.png'), (20, 20))
    button_e = pygame.transform.scale(load_image('key_e.png', 'blue'), (20, 20))

    def __init__(self, screen, x, y, type, player, *group):
        super().__init__(*group)
        self.type = type
        self.player = player
        if type == 'medicine chest':
            self.image = Item.medicine
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen

    def update(self, *args):
        if pygame.sprite.collide_rect(self, self.player):
            self.image_2 = pygame.Surface((21, 21))
            self.image_2.blit(Item.button_e, (0, 0))
            self.screen.blit(self.image_2, (
                self.rect.x - self.image_2.get_width() / 2 + self.rect.w / 2, self.rect.y - self.image_2.get_height()))
        if pygame.sprite.collide_rect(self, self.player) and args[0][pygame.K_e]:
            if self.type in self.player.inventory:
                self.player.inventory[self.type] += 1
            else:
                self.player.inventory[self.type] = 1
            self.kill()
