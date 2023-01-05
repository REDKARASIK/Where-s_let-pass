import pygame

from main_functions import terminate

pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos_x, pos_y, *group):
        super().__init__(*group)
        self.text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.step = 15
        self.font = pygame.font.Font(None, 50)
        self.text_m = self.font.render(self.text, True, 'white')
        self.text_width = self.text_m.get_width()
        self.text_height = self.text_m.get_height()
        self.image = pygame.Surface([self.text_width + self.step * 2, self.text_height + self.step * 2])
        pygame.draw.rect(self.image, 'white', (0, 0, self.text_width + self.step * 2,
                                               self.text_height + self.step * 2), 2)
        self.image.blit(self.text_m, (self.step, self.step))
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.text_width + self.step * 2,
                                self.text_height + self.step * 2)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(args[0].pos):
                pygame.draw.rect(self.image, 'blue',
                                 (0, 0, self.text_width + self.step * 2, self.text_width + self.step * 2))
                pygame.draw.rect(self.image, 'white', (0, 0, self.text_width + self.step * 2,
                                                       self.text_height + self.step * 2), 2)
                self.image.blit(self.text_m, (self.step, self.step))
            else:
                pygame.draw.rect(self.image, 'black',
                                 (0, 0, self.text_width + self.step * 2, self.text_width + self.step * 2))
                pygame.draw.rect(self.image, 'white', (0, 0, self.text_width + self.step * 2,
                                                       self.text_height + self.step * 2), 2)
                self.image.blit(self.text_m, (self.step, self.step))
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                pygame.draw.rect(self.image, 'darkblue',
                                 (0, 0, self.text_width + self.step * 2, self.text_width + self.step * 2))
                pygame.draw.rect(self.image, 'white', (0, 0, self.text_width + self.step * 2,
                                                       self.text_height + self.step * 2), 2)
                self.image.blit(self.text_m, (self.step, self.step))
        if args and args[0].type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(args[0].pos):
                pygame.draw.rect(self.image, 'blue',
                                 (0, 0, self.text_width + self.step * 2, self.text_width + self.step * 2))
                pygame.draw.rect(self.image, 'white', (0, 0, self.text_width + self.step * 2,
                                                       self.text_height + self.step * 2), 2)
                self.image.blit(self.text_m, (self.step, self.step))

    def click(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            return True


if __name__ == '__main__':
    running = True
    button = Button('Привет', 'кнопка', 100, 100, all_sprites)
    while True:
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
