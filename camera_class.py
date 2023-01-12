import pygame

pygame.init()


class Camera:
    def __init__(self, screen, start_pos):
        self.dx = 0
        self.dy = 0
        self.screen = screen
        self.start_pos = start_pos

    def apply(self, obj=None):
        if obj:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        else:
            return self.dx, self.dy

    def update(self, target):
        self.dx = -(target.rect.x - self.start_pos[0])
        self.dy = -(target.rect.y - self.start_pos[1])
        self.start_pos = (target.rect.x, target.rect.y)
        print(self.dx, self.dy)
