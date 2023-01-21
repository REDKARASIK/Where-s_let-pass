import pygame
from main_functions import load_image


class Health(pygame.sprite.Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.image = pygame.Surface((player.max_health / 10 * 16, 14))
        pygame.draw.rect(self.image, 'red', (0, 0, player.health / 10 * 16, self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.font = pygame.font.Font(None, 20)

    def update(self, *args):
        self.image.fill('black')
        pygame.draw.rect(self.image, 'red', (0, 0, self.player.health // (self.player.max_health / 10) * 16, self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 2)
        self.screen.blit(self.font.render(str(self.player.health) + '%', True, 'white'),
                         (self.rect.x + self.image.get_width() + 10, self.rect.y))


class Stamina(pygame.sprite.Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.image = pygame.Surface((player.max_stamina / 10 * 16, 14))
        pygame.draw.rect(self.image, 'blue', (0, 0, player.stamina / 10 * 16, self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.font = pygame.font.Font(None, 20)

    def update(self, *args):
        self.image.fill('black')
        pygame.draw.rect(self.image, 'blue', (0, 0, self.player.stamina // (self.player.max_stamina / 10) * 16,
                                              self.image.get_height()))
        pygame.draw.rect(self.image, 'darkblue', (0, 0, self.image.get_width(), self.image.get_height()), 2)
        self.screen.blit(self.font.render(str(self.player.stamina) + '%', True, 'white'),
                         (self.rect.x + self.image.get_width() + 10, self.rect.y))
