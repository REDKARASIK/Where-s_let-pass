import pygame
from main_functions import *
from player_class import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
fps = 25


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, level, *groups):
        super().__init__(*groups)
        self.map_check = level
        self.idle_frames = []
        # self.cut_sheet(self.idle_frames, load_image('Man_idle.png', 'white'), 4, 1)
        self.walk_frames = []
        # self.cut_sheet(self.walk_frames, load_image('Man_walk.png', 'white'), 6, 1)
        self.fight_frames = []
        # self.cut_sheet(self.fight_frames, load_image('Man_attack.png', 'white'), 4, 1)
        self.cur_frame = 0
        self.image = load_image('chestopen.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.speed = 9
        self.walk_check = False
        self.attack = False

    def cut_sheet(self, frames, sheet, columns, rows):
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * 1.5), int(sheet.get_height() * 1.5)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, (22 * 1.5, self.rect.height))))

    def update(self, player_coords):
        target_x, target_y = player_coords
        x, y = self.rect.x, self.rect.y
        distance = ((target_x - x) ** 2 + (target_y - y) ** 2) ** 0.5
        if distance <= 100:
            self.follow_player(x, y, target_x, target_y)
        if distance <= 2:
            self.fight_player()

    def follow_player(self, x1, y1, x2, y2):
        if x1 > x2:
            self.rect.x -= self.speed
        elif x1 < x2:
            self.rect.x += self.speed
        if y1 > y2:
            self.rect.y -= self.speed
        elif y1 < y2:
            self.rect.y += self.speed

    def fight_player(self):
        return 0




if __name__ == '__main__':
    clock = pygame.time.Clock()
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1,
                             [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 60, 61, 62, 63, 70, 71, 72, 73, 11, 12, 13,
                              14, 21, 22,
                              23, 24, 31, 32, 33, 34, 41, 43])), 50)
    player = Player(64, 64, map_level, all_sprites)
    enemy = Enemy(120, 120, map_level, all_enemy)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        all_enemy.update((player.rect.x, player.rect.y))
        all_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(fps)



