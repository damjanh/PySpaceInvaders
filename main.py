import pygame
import sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height), screen_width, screen_height, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 3
        self.lives_surface = pygame.image.load('graphics/player.png').convert_alpha()
        self.life_x_start_position = screen_width - (self.lives_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, start_x=screen_width / 15, start_y=480)

        self.alien_speed = 1
        self.aliens = pygame.sprite.Group()
        self.create_aliens(rows=6, cols=8)

        self.alien_lasers = pygame.sprite.Group()

        self.alien_extra = pygame.sprite.GroupSingle()
        self.alien_extra_spawn_time = randint(400, 800)

        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)

        self.explosion = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion.set_volume(0.2)

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.2)

        self.game_end = False

    def create_multiple_obstacle(self, *offset, start_x, start_y, ):
        for offset_x in offset:
            self.create_obstacle(start_x, start_y, offset_x)

    def create_obstacle(self, start_x, start_y, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    block = obstacle.Block(
                        self.block_size,
                        (241, 79, 80),
                        start_x + col_index * self.block_size + offset_x,
                        start_y + row_index * self.block_size
                    )
                    self.blocks.add(block)

    def create_aliens(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def check_alien_position(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_speed = -1
                self.alien_move_down(2)
            if alien.rect.left <= 0:
                self.alien_speed = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, screen_height, 6)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def check_update_spawn_extra(self):
        if not self.game_end:
            self.alien_extra_spawn_time -= 1
            if self.alien_extra_spawn_time <= 0:
                self.alien_extra.add(Extra(choice(['right', 'left']), screen_width))
                self.alien_extra_spawn_time = randint(400, 800)

    def check_collisions(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.score
                    laser.kill()
                    self.explosion.play()

                if pygame.sprite.spritecollide(laser, self.alien_extra, True):
                    self.score += self.alien_extra.sprite.score
                    laser.kill()
                    self.explosion.play()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for life in range(self.lives - 1):
            x = self.life_x_start_position + (life * (self.lives_surface.get_size()[0] + 10))
            screen.blit(self.lives_surface, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft=(10, -10))
        screen.blit(score_surface, score_rect)

    def check_display_victory_message(self):
        if not self.aliens.sprites():
            self.game_end = True
            victory_surface = self.font.render('You won!', False, 'white')
            victory_rect = victory_surface.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(victory_surface, victory_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_speed)
        self.alien_extra.update()
        self.alien_lasers.update()

        self.check_alien_position()
        self.check_update_spawn_extra()
        self.check_collisions()
        self.check_display_victory_message()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.alien_extra.draw(screen)

        self.display_lives()
        self.display_score()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)

        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    TIMER_ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_ALIEN_LASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TIMER_ALIEN_LASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)
