import pygame
import pytmx
from main_functions import terminate

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
print(screen.get_size())


class Map:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'maps/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile
        self.dx = 0
        self.dy = 0
        self.finish_id = 75

    def render(self, screen, dx=0, dy=0):
        self.dx += dx
        self.dy += dy
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                image2 = self.map.get_tile_image(x, y, 1)
                screen.blit(image, (x * self.tile_size + self.dx, y * self.tile_size + self.dy))
                if image2:
                    screen.blit(image2, (x * self.tile_size + self.dx, y * self.tile_size + self.dy))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


if __name__ == "__main__":
    maps = Map('project_of_map.tmx', 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        maps.render(screen)
        pygame.display.flip()
