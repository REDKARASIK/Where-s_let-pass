import pygame
from main_functions import load_image

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class Inventory(pygame.sprite.Sprite):
    medicine = pygame.transform.scale(load_image('first-aid-kit.png'), (64, 64))

    def __init__(self, screen, player, x, y, *args):
        super().__init__(*args)
        self.screen = screen
        self.player = player
        self.image = pygame.Surface((self.screen.get_width() / 2, self.screen.get_height()))
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'black',
                         (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
        self.rect.x = x
        self.rect.y = y
        self.open_check = False
        self.medicine = None

    def update(self, *args):
        pygame.mouse.set_visible(True)
        x = 10
        y = 10
        all_sprites = pygame.sprite.Group()
        self.image.fill('black')
        for i in self.player.inventory.keys():
            if self.player.inventory[i] > 0:
                if i == 'medicine chest':
                    self.medicine = pygame.sprite.Sprite()
                    self.medicine.image = pygame.Surface((70, 70))
                    self.medicine.rect = pygame.Rect((x - 2, y - 2, 68, 68))
                    all_sprites.add(self.medicine)
                    font = pygame.font.Font(None, 20)
                    self.image.blit(font.render(str(self.player.inventory[i]), True, 'white'), (x + 70, 70))
                    all_sprites.draw(self.image)
                    pygame.draw.rect(self.image, 'white',
                                     (x - 2, y - 2, 68, 68), 2)
                    self.image.blit(Inventory.medicine, (x, y))
                x += 15
                if x > self.rect.w:
                    y += 15

    def take_from(self, *args):
        if self.medicine:
            if self.medicine.rect.collidepoint(args[0][0] - self.screen.get_width() / 2,
                                               args[0][1]) and self.player.health < 100:
                self.player.health += 20
                if self.player.health > 100:
                    self.player.health = 100
                self.player.inventory['medicine chest'] -= 1
                self.medicine = None

    def change_open(self):
        if self.open_check:
            self.open_check = False
        else:
            self.open_check = True
