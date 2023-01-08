import pygame
import pytmx

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class Map:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'maps/firstmap.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))


if __name__ == "__main__":
    map = Map('1stmap.tmx', 0, 0)
    while True:
        screen.fill('black')
        map.render(screen)
        pygame.display.flip()
