import pygame
from player_class import Player
from main_functions import terminate
from class_map import Map

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
player_group = pygame.sprite.Group()


def main_game(screen, name_level):
    clock = pygame.time.Clock()
    map_level = Map(name_level,
                    [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 60, 61, 62, 63, 70, 71, 72, 73, 11, 12, 13, 14, 21, 22,
                     23, 24, 31, 32, 33, 34, 79, 43], 50)
    player = Player(64, 64, map_level, player_group)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        player_group.draw(screen)
        player_group.update(pygame.key.get_pressed())
        pygame.display.flip()
        clock.tick(15)


if __name__ == '__main__':
    main_game(screen, 'project_of_map.tmx')
