import random
import sys

import pygame

from snakegame.game.apple import Apple
from snakegame.game.snake import Snake


class Motor:
    def __init__(self, snake_speed, map_size=600, snake_color=(255, 255, 255), background_color=(0, 0, 0),
                 cell_size=15, frames_per_second=60, apple_color=(0, 255, 0)):
        self.map_size = map_size
        self.snake_speed = snake_speed
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.background_color = background_color
        self.cell_size = cell_size
        self.frames_per_second = frames_per_second
        self.snake = Snake(map_size, square_size=cell_size, speed=snake_speed)
        self.apple = self.generate_apple()

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((self.map_size, self.map_size))
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:

            for event in pygame.event.get():

                self.check_for_exit(event)

                self.update_direction(event)

            screen.fill(self.background_color)

            self.snake.update_position()
            self.check_if_apple_has_been_eaten()

            if self.snake.alive is False:
                game_over = True
                pass

            self.draw_snake(screen)
            self.draw_apple(screen)

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

    def draw_apple(self, screen):
        pygame.draw.rect(screen, self.apple_color, (
            self.apple.position_x, self.apple.position_y, self.cell_size, self.cell_size))

    def generate_apple(self):
        segments = self.snake.get_segments()
        positions_blocked_by_snake = [[], []]
        for segment in segments:
            positions_blocked_by_snake[0].append(segment.position_x)
            positions_blocked_by_snake[1].append(segment.position_y)
        position_x = random.randrange(0, self.map_size - self.cell_size, self.cell_size)
        while position_x in positions_blocked_by_snake[0]:
            position_x = random.randrange(0, self.map_size - self.cell_size, self.cell_size)
        position_y = random.randrange(0, self.map_size - self.cell_size, self.cell_size)
        while position_y in positions_blocked_by_snake[1]:
            position_y = random.randrange(0, self.map_size - self.cell_size, self.cell_size)
        return Apple(position_x, position_y)

    def check_if_apple_has_been_eaten(self):
        segments = self.snake.get_segments()
        head_of_snake = segments[0]
        if head_of_snake.position_x == self.apple.position_x and head_of_snake.position_y == self.apple.position_y:
            self.apple.eaten = True
            self.apple = self.generate_apple()
            self.snake.add_a_segment()

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()
