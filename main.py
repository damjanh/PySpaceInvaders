import pygame
import sys
from player import Player
import obstacle


class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height), screen_width, screen_height, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, start_x=screen_width / 15 , start_y=480)

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

    def run(self):
        self.player.update()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
