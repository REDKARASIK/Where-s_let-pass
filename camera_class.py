import pygame

pygame.init()


class Camera:
    def __init__(self, screen):
        self.dx = 0
        self.dy = 0
        self.screen = screen

    def apply(self, obj=None):
        if obj:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        else:
            return self.dx, self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.screen.get_width() // 2 + 668)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.screen.get_height() // 2 + 343)
        print(self.dx, self.dy)
