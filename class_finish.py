# 128, 224
import pygame

from class_map import Map
from main_functions import load_image
from main_functions import terminate
from player_class import Player

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
    clock = pygame.time.Clock()
    Finish((40, 40), players, all_sprites)
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
