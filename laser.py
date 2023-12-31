import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, screen_height, speed=-8):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.screen_height + 50:
            self.kill()


