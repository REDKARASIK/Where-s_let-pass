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
        self.cut_sheet(self.idle_frames, load_image('zombie_Idle.png', 'white'), 8, 1)
        self.walk_frames = []
        self.cut_sheet(self.walk_frames, load_image('zombie_Walk.png', 'white'), 8, 1)
        self.fight_frames = []
        self.cut_sheet(self.fight_frames, load_image('zombie_Attack.png', 'white'), 5, 1)
        self.dead_frames = []
        self.cut_sheet(self.dead_frames, load_image('zombie_Dead.png', 'white'), 5, 1)
        self.cur_frame = 0
        self.image = self.idle_frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.speed = 7
        self.walk_check = False
        self.attack = True
        self.health = 100
        self.damage = 10

    def cut_sheet(self, frames, sheet, columns, rows):
        k = 0.7
        sheet = pygame.transform.scale(sheet, (int(sheet.get_width() * k), int(sheet.get_height() * k)))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        # for j in range(rows):
        #     for i in range(columns):
        #         frame_location = (self.rect.w * i, self.rect.h * j)
        #         image = sheet.subsurface(pygame.Rect(frame_location, (self.rect.width, self.rect.height)))
        #         pixel_rect = image.get_bounding_rect()
        #         trimmed_surface = pygame.Surface(pixel_rect.size)
        #         trimmed_surface.blit(image, (0, 0), pixel_rect)
        #         frames.append(trimmed_surface)
        #         print(trimmed_surface.get_width())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, (self.rect.width, self.rect.height)))
                frames.append(image)

    def update(self, player):
        self.player = player
        target_x, target_y = player.rect.x, player.rect.y
        x, y = self.rect.x, self.rect.y
        distance = ((target_x - x) ** 2 + (target_y - y) ** 2) ** 0.5

        if not (pygame.sprite.collide_rect(self, player)) and distance <= 200:
            self.follow_player(x, y, target_x, target_y)
            self.walk_player()
        if pygame.sprite.collide_rect(self, player):
            if self.attack:
                self.cur_frame = 0
            self.fight_player()
        if distance >= 200:
            self.idle_enemy()

    def follow_player(self, x1, y1, x2, y2):
        coords_of_angles = [(x1, y1), (x1 + self.rect.width, y1), (x1 + self.rect.width, y1 + self.rect.height),
                            (x1, y1 + self.rect.height)]
        if x1 > x2:
            coords = list(
                map(lambda x: [(x[0] - self.speed) // self.map_check.tile_size, x[1] // self.map_check.height],
                    coords_of_angles))
            if all(self.map_check.is_free(coord) for coord in coords):
                self.rect.x -= self.speed
                self.transform = True
        if x1 < x2:
            coords = list(
                map(lambda x: [(x[0] + self.speed) // self.map_check.tile_size, x[1] // self.map_check.height],
                    coords_of_angles))
            if all(self.map_check.is_free(coord) for coord in coords):
                self.rect.x += self.speed
                self.transform = False
        if y1 > y2:
            coords = list(
                map(lambda x: [x[0] // self.map_check.tile_size, (x[1] - self.speed) // self.map_check.height],
                    coords_of_angles))
            if all(self.map_check.is_free(coord) for coord in coords):
                self.rect.y -= self.speed
        if y1 < y2:
            coords = list(
                map(lambda x: [x[0] // self.map_check.tile_size, (x[1] + self.speed) // self.map_check.height],
                    coords_of_angles))
            if all(self.map_check.is_free(coord) for coord in coords):
                self.rect.y += self.speed

    def fight_player(self):
        self.player.health -= self.damage
        self.image = self.fight_frames[self.cur_frame]
        self.cur_frame = (self.cur_frame + 1) % len(self.fight_frames)
        print(self.cur_frame, 123214214234)
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)
        self.attack = False

    def walk_player(self):
        self.attack = True
        self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames)
        self.image = self.walk_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)

    def idle_enemy(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.idle_frames)
        self.image = self.idle_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)

    def dead_enemy(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.dead_frames)
        self.image = self.dead_frames[self.cur_frame]
        if self.transform:
            self.image = pygame.transform.flip(self.image, True, False)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    free_tiles = [6, 7, 8, 9, 16, 17, 18, 19, 26, 27, 28, 29, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 60, 61,
                  62, 63, 70, 71, 72, 73, 79]
    map_level = Map('project_of_map.tmx',
                    list(map(lambda x: x + 1, free_tiles)), 50)
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
        all_enemy.update(player)
        all_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
