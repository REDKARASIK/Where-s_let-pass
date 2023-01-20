import random
import pygame
from main_functions import terminate
from main_functions import load_image
from player_class import Player
from class_map import Map
from item import Item

# лучший класс отвечаю!!!!!!!!!
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
maps = Map('project_of_map.tmx', [7], 1)
players = Player(50, 50, maps, all_sprites)
player_sprites = pygame.sprite.Group()
player_sprites.add(players)
fps = 15


class DowerChest(pygame.sprite.Sprite):
    imageopen = pygame.transform.scale(load_image("chestopen.png", 'white'), (24, 24))
    imageclosed = pygame.transform.scale(load_image("chestclosed.png", 'white'), (24, 24))
    button_e = pygame.transform.scale(load_image('key_e.png', 'blue'), (20, 20))

    def __init__(self, pos, screen, player, *group):
        super().__init__(*group)
        self.group = group
        self.player = player
        self.screen = screen
        self.items = ["medicine chest", 'stamina chest', 'fireball']
        self.image = DowerChest.imageclosed
        self.item = random.choice(self.items)
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


if __name__ == '__main__':
    clock = pygame.time.Clock()
    DowerChest((40, 40), screen, players, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        maps.render(screen)
        all_sprites.update(pygame.key.get_pressed())
        all_sprites.draw(screen)
        player_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
