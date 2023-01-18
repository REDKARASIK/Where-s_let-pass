import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class Inventory(pygame.sprite.Sprite):
    def __init__(self, screen, player, x, y, *args):
        super().__init__(*args)
        self.screen = screen
        self.player = player
        self.image = pygame.Surface((self.screen.get_width() / 2, self.screen.get_height()))
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'black',
                         (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
        self.rect.x = x
        self.rect.y = y
        self.open_check = False

    def update(self, *args):
        if self.open_check:
            self.open_check = False
        else:
            self.open_check = True
