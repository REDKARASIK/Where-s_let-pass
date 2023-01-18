import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, wall: bool, image, *args):
        super().__init__(*args)
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.wall = wall
