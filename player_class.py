import pygame

from class_map import Map
from main_functions import load_image, terminate

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fps = 25


class Fireball(pygame.sprite.Sprite):
    def __init__(self, player, enemy_group, *groups):
        super().__init__(*groups)
        self.player = player
        self.enemy_group = enemy_group
        self.cur_frame = 0
        self.fire_frames = []
        self.cut_sheet(self.fire_frames, load_image('Charge.png'), 12, 1)
        self.image = self.fire_frames[self.cur_frame]
        if self.player.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if not self.player.transform:
            self.rect.x = self.player.rect.x + self.rect.w / 2 + 10
        else:
            self.rect.x = self.player.rect.x - 10
        self.rect.y = self.rect.y + self.player.rect.h
        self.enemy = None
        self.collide = False

    def cut_sheet(self, frames, sheet, columns, rows):
        k = 0.9
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * k), int(sheet.get_height() * k)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, (self.rect.width, self.rect.height))))

    def update(self, *args):
        self.cur_frame = (self.cur_frame + 1) % len(self.fire_frames)
        self.enemy = pygame.sprite.spritecollideany(self, self.enemy_group)
        if self.cur_frame:
            if not self.enemy:
                if self.player.transform:
                    self.rect.x -= 10
                else:
                    self.rect.x += 10
            else:
                if not self.collide:
                    self.enemy.health -= 20
                    self.collide = True
                self.enemy.time = 25
                self.enemy.hurt_check = True
                self.rect.x = self.enemy.rect.x + self.enemy.rect.w / 2 - 5
            self.image = self.fire_frames[self.cur_frame]
            if self.player.transform:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, level, enemy_group, *groups):
        super().__init__(*groups)
        self.groups = groups
        self.enemy_group = enemy_group
        self.map_check = level
        self.idle_frames = []
        self.cut_sheet(self.idle_frames, load_image('Idle.png', 'white'), 7, 1)
        self.walk_frames = []
        self.cut_sheet(self.walk_frames, load_image('Walk.png', 'white'), 6, 1)
        self.fight_frames = []
        self.cut_sheet(self.fight_frames, load_image('Attack_1.png', 'white'), 4, 1)
        self.fight_frames.append(self.fight_frames[-1])
        self.fight_frames_2 = []
        self.cut_sheet(self.fight_frames_2, load_image('Attack_2.png', 'white'), 4, 1)
        self.fight_frames_2.append(self.fight_frames_2[-1])
        self.hurt_frames = []
        self.cut_sheet(self.hurt_frames, load_image('Hurt.png', 'white'), 3, 1)
        self.cur_frame = 0
        self.run_frames = []
        self.cut_sheet(self.run_frames, load_image('Run.png', 'white'), 8, 1)
        self.flame_frames = []
        self.cut_sheet(self.flame_frames, load_image('Flame_jet.png', 'white'), 14, 1)
        self.flame_frames.append(self.flame_frames[-1])
        self.fire_ball_attack = []
        self.cut_sheet(self.fire_ball_attack, load_image('Fireball.png', 'white'), 8, 1)
        self.dead_frames = []
        self.cut_sheet(self.dead_frames, load_image('Dead.png'), 6, 1)
        self.dead_frames.append(self.dead_frames[-1])
        self.image = self.idle_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.walk_check = False
        self.dead_check = True
        self.attack = False
        self.dead = False
        self.deads = False
        self.damage_1 = 10
        self.attack_2 = False
        self.damage_2 = 20
        self.max_health = 100
        self.max_stamina = 100
        self.health = self.max_health
        self.hurt_check = False
        self.mask = pygame.mask.from_surface(self.image)
        self.stamina = self.max_stamina
        self.stamina_up = 0
        self.stamina_up_time = 20
        self.run_check = False
        self.speed_2 = 15
        self.speed_1 = 10
        self.speed = self.speed_1
        self.inventory = {'medicine chest': 1, 'fireball': 5}
        self.attack_flame = False
        self.attack_fire = False
        self.damage_3 = 10
        self.dead_time = 15
        self.timer = 0

    def cut_sheet(self, frames, sheet, columns, rows):
        k = 0.9
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * k), int(sheet.get_height() * k)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, (self.rect.width, self.rect.height))))

    def attack_1(self):
        self.image = self.fight_frames[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if not self.cur_frame:
            self.attack = False
            self.cur_frame = 0
            collide_enemy = pygame.sprite.spritecollideany(self, self.enemy_group)
            if collide_enemy:
                collide_enemy.hurt_check = True
                collide_enemy.health -= self.damage_1
                collide_enemy.time = 25

    def attack_3(self):
        attack = [5, 6, 7, 8]
        self.image = self.flame_frames[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.flame_frames)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.cur_frame in attack:
            self.stamina -= 10
            collide_enemy = pygame.sprite.spritecollideany(self, self.enemy_group)
            if collide_enemy:
                collide_enemy.hurt_check = True
                collide_enemy.health -= self.damage_3
                collide_enemy.time = 25
        if not self.cur_frame:
            self.attack_flame = False
            self.cur_frame = 0

    def attack_2_func(self):
        self.image = self.fight_frames_2[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames_2)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if not self.cur_frame:
            self.attack_2 = False
            self.cur_frame = 0
            collide_enemy = pygame.sprite.spritecollideany(self, self.enemy_group)
            if collide_enemy:
                collide_enemy.hurt_check = True
                collide_enemy.health -= self.damage_2
                collide_enemy.time = 25

    def attack_fireball(self):
        self.image = self.fire_ball_attack[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.fire_ball_attack)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.cur_frame == len(self.fire_ball_attack) - 1:
            Fireball(self, self.enemy_group, self.groups)
        if not self.cur_frame:
            self.attack_fire = False
            self.cur_frame = 0

    def hurt(self):
        self.image = self.hurt_frames[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.hurt_frames)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        if not self.cur_frame:
            self.hurt_check = False
            self.cur_frame = 0

    def run(self):
        self.image = self.run_frames[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.run_frames)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, *args):
        if self.dead_check:
            self.stamina_up = (self.stamina_up + 1) % self.stamina_up_time
            if self.stamina_up == 0:
                self.stamina += 10
                if self.stamina > self.max_stamina:
                    self.stamina = self.max_stamina
            if self.hurt_check and not self.attack and not self.attack_2:
                self.hurt()
            else:
                k = 45
                if args[0][
                    pygame.K_f] and not self.attack_2 and not self.attack and self.stamina >= 10 and not self.attack_flame and not self.attack_fire:
                    self.stamina -= 10
                    self.stamina_up = 0
                    self.cur_frame = 0
                    self.attack = True
                    self.walk_check = False
                    self.run_check = False
                if args[0][
                    pygame.K_v] and not self.attack and not self.attack_2 and not self.attack_flame and self.stamina >= 40 and not self.attack_fire:
                    self.stamina_up = 0
                    self.cur_frame = 0
                    self.attack_flame = True
                    self.walk_check = False
                    self.run_check = False
                if args[0][
                    pygame.K_g] and not self.attack and not self.attack_2 and self.stamina >= 25 and not self.attack_flame and not self.attack_fire:
                    self.stamina -= 25
                    self.cur_frame = 0
                    self.stamina_up = 0
                    self.attack_2 = True
                    self.walk_check = False
                    self.run_check = False
                if args[0][
                    pygame.K_x] and not self.attack_2 and not self.attack and not self.attack_flame and not self.attack_fire and \
                        self.inventory['fireball'] > 0:
                    self.stamina_up = 0
                    self.inventory['fireball'] -= 1
                    self.cur_frame = 0
                    self.attack_fire = True
                    self.walk_check = False
                    self.run_check = False
                if self.attack_flame:
                    self.attack_3()
                if self.attack:
                    self.attack_1()
                if self.attack_2:
                    self.attack_2_func()
                if self.attack_fire:
                    self.attack_fireball()
                if self.walk_check:
                    self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames)
                    self.image = self.walk_frames[self.cur_frame]
                    if self.transform:
                        self.image = pygame.transform.flip(self.image, True, False)
                if self.run_check:
                    self.run()
                if not self.attack and not self.attack_2 and not self.attack_flame and not self.attack_fire:
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and self.stamina >= 5:
                        self.stamina -= 2.5
                        self.speed = self.speed_2
                    else:
                        self.speed = self.speed_1
                    if args[0][pygame.K_d]:
                        if self.map_check.is_free(
                                ((self.rect.x + self.speed + -self.map_check.dx + k) // self.map_check.tile_size,
                                 (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + self.rect.width + self.speed - k + -self.map_check.dx)
                                     // self.map_check.tile_size,
                                     (self.rect.y + self.rect.height + -self.map_check.dy)
                                     // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + self.rect.width + self.speed - k + -self.map_check.dx)
                                     // self.map_check.tile_size,
                                     (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(((self.rect.x + self.speed + -self.map_check.dx + k)
                                                        // self.map_check.tile_size,
                                                        (self.rect.y + self.rect.height + -self.map_check.dy)
                                                        // self.map_check.height)):
                            self.rect.x += self.speed
                            self.transform = False
                    if args[0][pygame.K_a]:
                        if self.map_check.is_free(
                                ((self.rect.x - self.speed + -self.map_check.dx + k) // self.map_check.tile_size,
                                 (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + self.rect.width - self.speed - k + -self.map_check.dx)
                                     // self.map_check.tile_size,
                                     (self.rect.y + self.rect.height + -self.map_check.dy)
                                     // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + self.rect.width - self.speed - k + -self.map_check.dx)
                                     // self.map_check.tile_size,
                                     (self.rect.y + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(((self.rect.x - self.speed + -self.map_check.dx + k)
                                                        // self.map_check.tile_size,
                                                        (self.rect.y + self.rect.height + -self.map_check.dy)
                                                        // self.map_check.height)):
                            self.transform = True
                            self.rect.x -= self.speed
                    if args[0][pygame.K_s]:
                        if self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                                   (
                                                           self.rect.y + self.speed + -self.map_check.dy)
                                                   // self.map_check.height)) and \
                                self.map_check.is_free(((self.rect.x + self.rect.width - k + -self.map_check.dx)
                                                        // self.map_check.tile_size,
                                                        (
                                                                self.rect.y + self.rect.height + self.speed + -self.map_check.dy)
                                                        // self.map_check.height)) and \
                                self.map_check.is_free(((self.rect.x + self.rect.width - k + -self.map_check.dx)
                                                        // self.map_check.tile_size,
                                                        (self.rect.y + self.speed + -self.map_check.dy)
                                                        // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                     (self.rect.y + self.rect.height + self.speed + -self.map_check.dy)
                                     // self.map_check.height)):
                            self.rect.y += self.speed
                    if args[0][pygame.K_w]:
                        if self.map_check.is_free(((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                                   (
                                                           self.rect.y - self.speed + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((
                                             self.rect.x + self.rect.width - k + -self.map_check.dx) // self.map_check.tile_size,
                                     (
                                             self.rect.y + self.rect.height - self.speed + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((
                                             self.rect.x + self.rect.width - k + -self.map_check.dx) // self.map_check.tile_size,
                                     (self.rect.y - self.speed + -self.map_check.dy) // self.map_check.height)) and \
                                self.map_check.is_free(
                                    ((self.rect.x + -self.map_check.dx + k) // self.map_check.tile_size,
                                     (((
                                               self.rect.y + -self.map_check.dy) + self.rect.height) - self.speed) // self.map_check.height)):
                            self.rect.y -= self.speed
                    if not (args[0][pygame.K_w] or args[0][pygame.K_s] or args[0][pygame.K_a] or args[0][pygame.K_d]):
                        if self.walk_check or self.run_check:
                            self.cur_frame = 0
                        self.cur_frame = (self.cur_frame + 1) % len(self.idle_frames)
                        self.image = self.idle_frames[self.cur_frame]
                        if self.transform:
                            self.image = pygame.transform.flip(self.image, True, False)
                        self.walk_check = False
                        self.run_check = False
                    else:
                        if not self.walk_check and not self.run_check:
                            self.cur_frame = 0
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT and self.stamina >= 5:
                            self.run_check = True
                            self.walk_check = False
                        else:
                            self.walk_check = True
                            self.run_check = False
        if self.health <= 0:
            if self.dead_check:
                self.dead_check = False
                self.cur_frame = 0
            if self.timer == 0:
                self.image = self.dead_frames[self.cur_frame]
                self.cur_frame = (self.cur_frame + 1) % len(self.dead_frames)
                if self.transform:
                    self.image = pygame.transform.flip(self.image, True, False)
            if self.cur_frame == 0:
                if self.timer == self.dead_time:
                    self.deads = True
                self.timer += 1


if __name__ == '__main__':
    clock = pygame.time.Clock()
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1,
                             [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 60, 61, 62, 63, 70, 71, 72, 73, 11, 12, 13,
                              14, 21, 22,
                              23, 24, 31, 32, 33, 34, 41, 43])), 50)
    player = Player(64, 64, map_level, enemy_group, all_sprites)
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
