import sys

import pygame

from snakegame.game.snake import Snake


class Motor:
    def __init__(self, map_size=600, snake_color=(255, 255, 255), background_color=(0, 0, 0),
                 cell_size=15, frames_per_second=60):
        self.map_size = map_size
        self.snake_color = snake_color
        self.background_color = background_color
        self.cell_size = cell_size
        self.frames_per_second = frames_per_second
        self.snake = Snake(map_size, square_size=cell_size, speed=1)

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((self.map_size, self.map_size))
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:

            for event in pygame.event.get():
                print(event)

                self.check_for_exit(event)

                self.update_direction(event)

            screen.fill(self.background_color)
            self.snake.update_position()
            if self.snake.alive is False:
                game_over = True
            else:
                self.draw_snake(screen)

            clock.tick(self.frames_per_second)

            pygame.display.update()

    def update_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.snake.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                self.snake.set_direction("right")
            elif event.key == pygame.K_UP:
                self.snake.set_direction("up")
            elif event.key == pygame.K_DOWN:
                self.snake.set_direction("down")

    def draw_snake(self, screen):
        segments = self.snake.get_segments()
        for segment in segments:
            pygame.draw.rect(screen, self.snake_color, (
                segment.position_x, segment.position_y, self.snake.square_size, self.snake.square_size))

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()
