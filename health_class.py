import pygame
from main_functions import load_image


class health(pygame.sprite.Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.image = pygame.Surface((10 * 16, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        self.image = pygame.Surface((self.player.health // 10 * 16, 16))
        self.image.fill((255, 0, 0))