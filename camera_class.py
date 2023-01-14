import pygame

pygame.init()


class Camera:
    def __init__(self, screen, start_pos, map_width, map_height, speed):
        self.map_w = map_width - screen.get_width()
        self.map_h = map_height - screen.get_height()
        self.w = 0
        self.h = 0
        self.dx = 0
        self.dy = 0
        self.screen = screen
        self.start_pos = start_pos
        self.stop = False
        self.speed = speed

    def apply(self, obj=None):
        if self.w + -self.dx > self.map_w or self.w + -self.dx < 0:
            self.dx = 0
        if self.h + -self.dy > self.map_h or self.h + -self.dy < 0:
            self.dy = 0
        self.w += -self.dx
        self.h += -self.dy
        if not (self.dx or self.dy):
            self.stop = True
        else:
            self.stop = False
        if obj:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        else:
            return self.dx, self.dy

    def update(self, target):
        self.dx = -(target.rect.x - self.start_pos[0])
        self.dy = -(target.rect.y - self.start_pos[1])
        self.start_pos = (target.rect.x, target.rect.y)
        if self.stop:
            target.speed = self.speed * 2
        else:
            target.speed = self.speed
