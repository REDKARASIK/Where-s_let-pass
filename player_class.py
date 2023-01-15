import pygame

from class_map import Map
from main_functions import load_image, terminate

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()
fps = 25


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, level, *groups):
        super().__init__(*groups)
        self.map_check = level
        self.idle_frames = []
        self.cut_sheet(self.idle_frames, load_image('main_idle.png'), 7, 1)
        self.walk_frames = []
        self.cut_sheet(self.walk_frames, load_image('main_walk.png'), 7, 1)
        self.fight_frames = []
        self.cut_sheet(self.fight_frames, load_image('main_attack1.png'), 10, 1)
        self.fight_frames.append(self.fight_frames[-1])
        self.fight_frames_2 = []
        self.cut_sheet(self.fight_frames_2, load_image('main_attack_2.png'), 4, 1)
        self.fight_frames_2.append(self.fight_frames_2[-1])
        self.cur_frame = 0
        self.image = self.idle_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.speed = 10
        self.walk_check = False
        self.attack = False
        self.attack_2 = False

    def cut_sheet(self, frames, sheet, columns, rows):
        k = 0.8
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * k), int(sheet.get_height() * k)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, (self.rect.width, self.rect.height))))


    def update(self, *args):
        k = 60
        if args[0][pygame.K_f] and not self.attack_2:
            self.cur_frame = 0
            self.attack = True
            self.walk_check = False
        if self.attack:
            self.image = self.fight_frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames)
            if self.transform:
                self.image = pygame.transform.flip(self.image, True, False)
            if not self.cur_frame:
                self.attack = False
                self.cur_frame = 0
        if args[0][pygame.K_g] and not self.attack:
            self.cur_frame = 0
            self.attack_2 = True
            self.walk_check = False
        if self.attack_2:
            self.image = self.fight_frames_2[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames_2)
            if self.transform:
                self.image = pygame.transform.flip(self.image, True, False)
            if not self.cur_frame:
                self.attack_2 = False
                self.cur_frame = 0
        if self.walk_check:
            self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.cur_frame]
            if self.transform:
                self.image = pygame.transform.flip(self.image, True, False)
        if not self.attack and not self.attack_2:
            if args[0][pygame.K_d]:
                if self.map_check.is_free(((self.rect.x + self.speed + -self.map_check.dx + k) // self.map_check.tile_size,
                                           (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width + self.speed - k + -self.map_check.dx)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + -self.map_check.dy)
                                                // self.map_check.height)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width + self.speed - k + -self.map_check.dx)
                                                // self.map_check.tile_size,
                                                (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                        self.map_check.is_free(((self.rect.x + self.speed + -self.map_check.dx + k)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + -self.map_check.dy)
                                                // self.map_check.height)):
                    self.rect.x += self.speed
                    self.transform = False
            if args[0][pygame.K_a]:
                if self.map_check.is_free(((self.rect.x - self.speed + -self.map_check.dx + k) // self.map_check.tile_size,
                                           (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width - self.speed - k + -self.map_check.dx)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + -self.map_check.dy)
                                                // self.map_check.height)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width - self.speed - k + -self.map_check.dx)
                                                // self.map_check.height,
                                                (self.rect.y + -self.map_check.dy) // self.map_check.tile_size)) and \
                        self.map_check.is_free(((self.rect.x - self.speed + -self.map_check.dx + k)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + -self.map_check.dy)
                                                // self.map_check.tile_size)):
                    self.transform = True
                    self.rect.x -= self.speed
            if args[0][pygame.K_s]:
                if self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                           (
                                                   self.rect.y + self.speed + -self.map_check.dy)
                                           // self.map_check.tile_size)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width - k + -self.map_check.dx)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + self.speed + -self.map_check.dy)
                                                // self.map_check.tile_size)) and \
                        self.map_check.is_free(((self.rect.x + self.rect.width - k + -self.map_check.dx)
                                                // self.map_check.tile_size,
                                                (self.rect.y + self.speed + -self.map_check.dy)
                                                // self.map_check.tile_size)) and \
                        self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                                (self.rect.y + self.rect.height + self.speed + -self.map_check.dy)
                                                // self.map_check.tile_size)):
                    self.rect.y += self.speed
            if args[0][pygame.K_w]:
                if self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                           (
                                                   self.rect.y - self.speed + -self.map_check.dy) // self.map_check.tile_size)) and \
                        self.map_check.is_free(
                            ((self.rect.x + self.rect.width - k + -self.map_check.dx) // self.map_check.tile_size,
                             (
                                     self.rect.y + self.rect.height - self.speed + -self.map_check.dy) // self.map_check.tile_size)) and \
                        self.map_check.is_free(
                            ((self.rect.x + self.rect.width - k + -self.map_check.dx) // self.map_check.tile_size,
                             (self.rect.y - self.speed + -self.map_check.dy) // self.map_check.tile_size)) and \
                        self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                                (((
                                                          self.rect.y + -self.map_check.dy) + self.rect.height) - self.speed) // self.map_check.tile_size)):
                    self.rect.y -= self.speed
            if not (args[0][pygame.K_w] or args[0][pygame.K_s] or args[0][pygame.K_a] or args[0][pygame.K_d]):
                if self.walk_check:
                    self.cur_frame = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.cur_frame]
                if self.transform:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.walk_check = False
            else:
                if not self.walk_check:
                    self.cur_frame = 0
                self.walk_check = True


if __name__ == '__main__':
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1, free_tiles)), 50)
    player = Player(64, 64, map_level, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        pygame.display.flip()
        clock.tick(fps)
