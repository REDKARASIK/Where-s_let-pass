import pygame
from main_functions import load_image


class health(pygame.sprite.Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.image = pygame.Surface((10 * 16, 14))
        pygame.draw.rect(self.image, 'red', (0, 0, 10 * 16, self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        self.image.fill('black')
        pygame.draw.rect(self.image, 'red', (0, 0, self.player.health // 10 * 16, self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 2)
