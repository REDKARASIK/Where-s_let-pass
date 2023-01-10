import random
import pygame
from main_functions import terminate
from main_functions import load_image
from player_class import Player
from class_map import Map

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
maps = Map('project_of_map.tmx', [7], 1)
player = Player(50, 50, maps, all_sprites)
player_sprites = pygame.sprite.Group()
player_sprites.add(player)
fps = 15


class dower_chest(pygame.sprite.Sprite):
    imageopen = pygame.transform.scale(load_image("chestopen.png"), (16, 16))
    imageclosed = pygame.transform.scale(load_image("chestclosed.png"), (16, 16))

    def __init__(self, pos, player, *group):
        super().__init__(*group)
        self.player = player
        self.items = ["medicine chest", "money chest", ""]
        self.image = dower_chest.imageclosed
        self.item = random.choice(self.items)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.move(pos[0], pos[1])

    def update(self, *args):
        if pygame.sprite.collide_rect(self, player) and args[0][pygame.K_e]:
            self.image = dower_chest.imageopen
            # return self.item


if __name__ == '__main__':
    clock = pygame.time.Clock()
    dower_chest((40, 40), player, all_sprites)
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
