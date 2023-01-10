import pygame

from main_functions import load_image, terminate

pygame.init()
screen = pygame.display.set_mode((500, 500))
all_sprites = pygame.sprite.Group()
fps = 15


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.idle_frames = []
        self.cut_sheet(self.idle_frames, load_image('Man_idle.png'), 4, 1)
        self.walk_frames = []
        self.cut_sheet(self.walk_frames, load_image('Man_walk.png'), 6, 1)
        self.fight_frames = []
        self.cut_sheet(self.fight_frames, load_image('Man_attack.png'), 4, 1)
        self.cur_frame = 0
        self.image = self.idle_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.transform = False
        self.speed = 2
        self.walk_check = False
        self.attack = False

    def cut_sheet(self, frames, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, (22, 48))))

    def update(self, *args):
        if args[0][pygame.K_f]:
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
        if self.walk_check:
            self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.cur_frame]
            if self.transform:
                self.image = pygame.transform.flip(self.image, True, False)
        if not self.attack:
            if args[0][pygame.K_d]:
                self.rect.x += self.speed
                self.transform = False
            if args[0][pygame.K_a]:
                self.transform = True
                self.rect.x -= self.speed
            if args[0][pygame.K_s]:
                self.rect.y += self.speed
            if args[0][pygame.K_w]:
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
    player = Player(50, 50, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update(pygame.key.get_pressed())
        pygame.display.flip()
        clock.tick(fps)
