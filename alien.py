import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if color == 'red':
            self.score = 100
        elif color == 'green':
            self.score = 200
        else:
            self.score = 300

    def update(self, direction):
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        self.screen_width = screen_width
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = - 50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -50 or self.rect.x >= self.screen_width + 50:
            self.kill()
