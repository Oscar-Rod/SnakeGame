import random
import sys

import pygame

from snakegame.game.apple import Apple
from snakegame.game.snakeAI import SnakeAI
from snakegame.game.snakeplayer import SnakePlayer


class Motor:
    def __init__(self, snake_speed, map_size=600, snake_color=(255, 255, 255), background_color=(0, 0, 0), cell_size=15,
                 frames_per_second=60, apple_color=(0, 255, 0), snake_initial_size=5, is_training=False,
                 number_of_generations=10, number_of_snakes=10):
        self.map_size = map_size
        self.snake_speed = snake_speed
        self.snake_initial_size = snake_initial_size
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.background_color = background_color
        self.cell_size = cell_size
        self.frames_per_second = frames_per_second
        self.is_training = is_training
        self.snakes = []
        self.apples = []
        self.number_of_generations = number_of_generations
        self.number_of_snakes = number_of_snakes

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((self.map_size, self.map_size))
        clock = pygame.time.Clock()
        for i in range(self.number_of_generations):
            self.play_generation(clock, i + 1, screen)

    def play_generation(self, clock, gen, screen):
        game_over = False
        self.snakes = self.generate_snakes()
        self.apples = self.generate_apples()
        while not game_over:
            screen.fill(self.background_color)
            self.message_display('Generation {}'.format(gen), 20, 70, 35, screen)

            for event in pygame.event.get():
                self.check_for_exit(event)

                # if not self.is_training:
                #     self.update_direction(event)

            for i in range(len(self.snakes)):
                self.snakes[i].set_direction(self.get_state_of_the_game(i))

                self.snakes[i].update_position()
                self.check_if_apple_has_been_eaten(i)
                snake_is_dead = self.check_if_snake_is_dead(i)

                if snake_is_dead:
                    game_over = True
                    pass

                self.draw_snake(screen, i)
                self.draw_apple(screen, i)

            clock.tick(self.frames_per_second)

            pygame.display.update()

    def update_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.snakes.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                self.snakes.set_direction("right")
            elif event.key == pygame.K_UP:
                self.snakes.set_direction("up")
            elif event.key == pygame.K_DOWN:
                self.snakes.set_direction("down")

    def draw_snake(self, screen, snake_number):
        segments = self.snakes[snake_number].get_segments()
        for segment in segments:
            pygame.draw.rect(screen, self.snake_color, (
                segment.position_x, segment.position_y, self.cell_size, self.cell_size))

    def draw_apple(self, screen, snake_number):
        pygame.draw.rect(screen, self.apple_color, (
            self.apples[snake_number].position_x, self.apples[snake_number].position_y, self.cell_size, self.cell_size))

    def generate_apples(self):
        apples = []
        for i in range(self.number_of_snakes):
            segments = self.snakes[i].get_segments()
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
            apples.append(Apple(position_x, position_y))
        return apples

    def generate_snakes(self):
        snakes = []
        for i in range(self.number_of_snakes):
            snake_direction = random.choice(["left", "right", "up", "down"])
            snake_position = [random.randrange((self.snake_initial_size - 1) * self.cell_size,
                                               self.map_size - self.snake_initial_size * self.cell_size,
                                               self.cell_size),
                              random.randrange((self.snake_initial_size - 1) * self.cell_size,
                                               self.map_size - self.snake_initial_size * self.cell_size,
                                               self.cell_size)]
            if not self.is_training:
                snake = SnakePlayer(snake_position, snake_direction, cell_size=self.cell_size, speed=self.snake_speed)
                snakes.append(snake)
            else:
                snake = SnakeAI(snake_position, snake_direction, cell_size=self.cell_size, speed=self.snake_speed)
                snakes.append(snake)
        return snakes

    def check_if_apple_has_been_eaten(self, snake_number):
        segments = self.snakes[snake_number].get_segments()
        head_of_snake = segments[0]
        if head_of_snake.position_x == self.apples[snake_number].position_x and \
                head_of_snake.position_y == self.apples[snake_number].position_y:
            self.apples.eaten = True
            # TODO ATTACH EACH APPLE TO EACH SNAKE
            self.apples = self.generate_apples()
            self.snakes[snake_number].add_a_segment()

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()

    def check_if_snake_is_dead(self, snake_number):
        hit_border = self.check_if_snake_hit_border(snake_number)
        hit_itself = self.check_if_snake_hit_itself(snake_number)
        return hit_border or hit_itself

    def check_if_snake_hit_border(self, snake_number):
        head_of_the_snake = self.snakes[snake_number].get_segments()[0]
        if head_of_the_snake.position_x < 0 or head_of_the_snake.position_x > (self.map_size - self.cell_size):
            return True
        if head_of_the_snake.position_y < 0 or head_of_the_snake.position_y > (self.map_size - self.cell_size):
            return True

        return False

    def check_if_snake_hit_itself(self, snake_number):
        head_of_the_snake = self.snakes[snake_number].get_segments()[0]
        segments = self.snakes[snake_number].get_segments()[1:]
        for segment in segments:
            if head_of_the_snake.position_x == segment.position_x and head_of_the_snake.position_y == segment.position_y:
                return True
        return False

    def get_state_of_the_game(self, snake_number):
        # Snake = 1
        # Apple = 2
        # Nothing = 0

        state_of_the_game = [0] * int((600 / 15)) * int((600 / 15))
        for segment in self.snakes[snake_number].get_segments():
            state_of_the_game[int(segment.position_x / 15) + int(segment.position_y / 15) * 40] = 1
        state_of_the_game[
            int(self.apples[snake_number].position_x / 15) + int(self.apples[snake_number].position_y / 15) * 40] = 2
        return state_of_the_game

    def message_display(self, text, size, posx, posy, window):
        large_text = pygame.font.Font('freesansbold.ttf', size)
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.center = (posx, posy)
        window.blit(text_surf, text_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 255, 0))
        return text_surface, text_surface.get_rect()
