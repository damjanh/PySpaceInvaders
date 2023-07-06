import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen_width, screen_height, speed):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.can_shoot = True
        self.reload_time = 600
        self.shot_time = 0

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_laser()

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.screen_width:
            self.rect.right = self.screen_width

    def shoot_laser(self):
        self.can_shoot = False
        self.shot_time = pygame.time.get_ticks()
        self.lasers.add(Laser(self.rect.center, self.screen_height))

    def check_reload(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shot_time >= self.reload_time:
                self.can_shoot = True

    def update(self):
        self.check_reload()
        self.get_input()
        self.constraint()
        self.lasers.update()
