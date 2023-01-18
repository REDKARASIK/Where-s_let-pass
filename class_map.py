import pygame
import pytmx

from borderline_class import Block
from main_functions import terminate

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class Map:
    def __init__(self, filename, free_tiles, border_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'maps/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.border_tiles = border_tiles
        self.finish_tile = finish_tile
        self.dx = 0
        self.dy = 0
        self.borderlines = pygame.sprite.Group()

    def render(self, dx=0, dy=0):
        self.dx += dx
        self.dy += dy
        self.borderlines.empty()
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                #image2 = self.map.get_tile_image(x, y, 1)
                pos = (x * self.tile_size + self.dx, y * self.tile_size + self.dy)
                # screen.blit(image, pos)
                flag = False if self.is_free((x, y)) else True
                Block(pos, flag, image, self.borderlines)

    def get_tile_id(self, position):
        return self.map.get_tile_gid(*position, 0)

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


if __name__ == "__main__":
    borders = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 78]
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    maps = Map('first_level.tmx', list(map(lambda x: x + 1, free_tiles)), list(map(lambda x: x + 1, borders)), 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        maps.render(screen)
        pygame.display.flip()
