import pygame

from player_class import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
fps = 25


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, level, player, *groups):
        super().__init__(*groups)
        self.map_check = level
        self.idle_frames = []
        self.cut_sheet(self.idle_frames, load_image('zombie_Idle.png', 'white'), 8, 1)
        self.walk_frames = []
        self.cut_sheet(self.walk_frames, load_image('zombie_Walk.png', 'white'), 8, 1)
        self.fight_frames = []
        self.cut_sheet(self.fight_frames, load_image('zombie_Attack.png', 'white'), 5, 1)
        self.fight_frames2 = []
        self.cut_sheet(self.fight_frames2, load_image('zombie_Attack2.png', 'white'), 11, 1)
        self.dead_frames = []
        self.cut_sheet(self.dead_frames, load_image('zombie_Dead.png', 'white'), 5, 1)
        self.hurt_frames = []
        self.cut_sheet(self.hurt_frames, load_image('zombie_Hurt.png', 'white'), 3, 1)
        self.cur_frame = 0
        self.image = self.idle_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.speed = 7
        self.walk_check = False
        self.hurt_check = False
        self.attack = False
        self.health = 100
        self.damage = 10
        self.dead = True
        self.player = player
        self.time = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.cnt_attacks = 0
        self.distance = 0
        self.walk_distance = 250
        self.y_up = True
        self.y_down = True
        self.x_up = True
        self.x_down = True
        self.bite_sound = pygame.mixer.Sound('data/bite.mp3')
        self.bite_sound.set_volume(0.25)
        self.bite_check = False
        self.attack_sound = pygame.mixer.Sound('data/zombie_attack.mp3')
        self.attack_sound.set_volume(0.25)
        self.attack_sound_check = False

    def cut_sheet(self, frames, sheet, columns, rows):
        k = 0.9
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * k), int(sheet.get_height() * k)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, (self.rect.width, self.rect.height)))
                frames.append(image)

    def update(self, *args):
        if self.hurt_check and not self.attack and self.dead:
            self.hurt()
        else:
            target_x, target_y = self.player.rect.x, self.player.rect.y
            x, y = self.rect.x, self.rect.y
            self.distance = ((target_x - x) ** 2 + (target_y - y) ** 2) ** 0.5
            self.mask = pygame.mask.from_surface(self.image)
            self.player.mask = pygame.mask.from_surface(self.player.image)
            if not (pygame.sprite.collide_mask(self, self.player)) and self.dead:
                if not self.walk_check:
                    self.cur_frame = 0
                if self.distance <= self.walk_distance:
                    self.follow_player(x, y, target_x, target_y)
            if pygame.sprite.collide_mask(self, self.player) and self.dead and self.time == 0:
                if not self.attack or self.walk_check:
                    self.cur_frame = 0
                    self.bite_check = False
                    self.attack_sound_check = False
                self.fight_player()
            if (self.distance >= self.walk_distance and self.dead) or (self.dead and self.time != 0):
                if self.walk_check or self.attack:
                    self.cur_frame = 0
                self.idle_enemy()
            if self.health <= 0:
                if self.dead:
                    self.cur_frame = 0
                self.dead_enemy()
            if self.time > 0:
                self.time -= 1

    def follow_player(self, x1, y1, x2, y2):
        coords_of_angles = [(x1, y1), (x1 + self.rect.width, y1), (x1 + self.rect.width, y1 + self.rect.height),
                            (x1, y1 + self.rect.height)]
        delta_x, delta_y = abs(x1 - x2), abs(y1 - y2)
        collide = pygame.sprite.spritecollide(self, self.map_check.wall_group, False)
        if x1 > x2 and delta_x > delta_y and self.x_down:
            cnt = 0
            self.transform = True
            if self.distance <= self.walk_distance:
                if collide:
                    for obj in collide:
                        if pygame.sprite.collide_mask(self, obj):
                            self.x_down = False
                            self.x_up = True
                            cnt += 1
                            break
                if not cnt:
                    self.x_up = self.x_down = self.y_up = self.y_down = True
                    self.rect.x -= self.speed
                    self.walk_player()
                    for obj in pygame.sprite.spritecollide(self, self.map_check.wall_group, False):
                        if pygame.sprite.collide_mask(self, obj):
                            self.rect.x += self.speed
                            self.x_up = False
                            self.x_down = True
                            break
                else:
                    self.rect.x += self.speed
        if x1 < x2 and delta_x > delta_y and self.x_up:
            cnt = 0
            self.transform = False
            if self.distance <= self.walk_distance:
                if collide:
                    for obj in collide:
                        if pygame.sprite.collide_mask(self, obj):
                            self.x_down = True
                            self.x_up = False
                            cnt += 1
                            break
                if not cnt:
                    self.x_up = self.x_down = self.y_up = self.y_down = True
                    self.rect.x += self.speed
                    self.walk_player()
                    for obj in pygame.sprite.spritecollide(self, self.map_check.wall_group, False):
                        if pygame.sprite.collide_mask(self, obj):
                            self.rect.x -= self.speed
                            self.x_up = False
                            self.x_down = True
                            break
                else:
                    self.rect.x -= self.speed
        if y1 > y2 and delta_y > delta_x and self.y_down:
            cnt = 0
            if self.distance <= self.walk_distance:
                if collide:
                    for obj in collide:
                        if pygame.sprite.collide_mask(self, obj):
                            self.y_down = False
                            self.y_up = True
                            cnt += 1
                            break
                if not cnt:
                    self.x_up = self.x_down = self.y_up = self.y_down = True
                    self.rect.y -= self.speed
                    self.walk_player()
                    for obj in pygame.sprite.spritecollide(self, self.map_check.wall_group, False):
                        if pygame.sprite.collide_mask(self, obj):
                            self.rect.y += self.speed
                            self.y_up = False
                            self.y_down = True
                            break
                else:
                    self.rect.y += self.speed
        if y1 < y2 and delta_y > delta_x and self.y_up:
            cnt = 0
            if self.distance <= self.walk_distance:
                if collide:
                    for obj in collide:
                        if pygame.sprite.collide_mask(self, obj):
                            self.y_down = True
                            self.y_up = False
                            cnt += 1
                            break
                if not cnt:
                    self.x_up = self.x_down = self.y_up = self.y_down = True
                    self.rect.y += self.speed
                    self.walk_player()
                    for obj in pygame.sprite.spritecollide(self, self.map_check.wall_group, False):
                        if pygame.sprite.collide_mask(self, obj):
                            self.rect.y -= self.speed
                            self.y_up = True
                            self.y_down = False
                            break
                else:
                    self.rect.y -= self.speed

    def fight_player(self):
        if self.cnt_attacks != 2:
            self.image = self.fight_frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames)
        else:
            self.image = self.fight_frames2[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames2)
            if not self.bite_check:
                self.bite_sound.play()
                self.bite_check = True
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.cur_frame == 0:
            if self.cnt_attacks != 2:
                if not self.attack_sound_check:
                    self.attack_sound.play()
                    self.attack_sound_check = True
            self.player.hurt_check = True
            if not (self.player.attack or self.player.attack_2):
                self.player.cur_frame = 0
            if self.cnt_attacks != 2:
                self.player.health -= self.damage
                self.time = 25
            else:
                self.player.health -= self.damage * 2
                self.time = 50
            self.cnt_attacks = (self.cnt_attacks + 1) % 3
            self.attack = False
            self.bite_check = False
            self.attack_sound_check = False
        self.attack = True
        self.walk_check = False

    def walk_player(self):
        self.walk_check = True
        self.attack = True
        self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames)
        self.image = self.walk_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)

    def idle_enemy(self):
        self.walk_check = False
        self.cur_frame = (self.cur_frame + 1) % len(self.idle_frames)
        self.image = self.idle_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        self.attack = False

    def dead_enemy(self):
        self.dead = False
        if self.cur_frame != len(self.dead_frames) - 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.dead_frames)
            self.image = self.dead_frames[self.cur_frame]
            if self.transform:
                self.image = pygame.transform.flip(self.image, True, False)

    def hurt(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.hurt_frames)
        self.image = self.hurt_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if not self.cur_frame:
            self.hurt_check = False
            self.cur_frame = 0


if __name__ == '__main__':
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1, free_tiles)), 50)
    player = Player(64, 64, map_level, all_enemy, all_sprites)
    enemy = Enemy(120, 120, map_level, player, all_enemy)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill('black')
        map_level.render(screen)
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        all_enemy.update(player)
        all_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
