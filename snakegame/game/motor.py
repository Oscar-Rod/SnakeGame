import datetime
import random
import sys

import pygame

from snakegame.game.apple import Apple
from snakegame.game.painter import Painter
from snakegame.game.snakeAI import SnakeAI
from snakegame.game.snakeplayer import SnakePlayer
from snakegame.neural_network.geneticalgorithm import Breeder


class Motor:
    def __init__(self, snake_speed, show_screen=True, snake_color=(255, 255, 255), background_color=(0, 0, 0),
                 number_of_cells=40, cell_size=15, frames_per_second=60, apple_color=(0, 255, 0), snake_initial_size=5,
                 human_player=True, number_of_generations=10, number_of_snakes=10, mutation_rate=0.1,
                 number_of_snakes_to_save=10, batch_name=None, training=False):
        self.number_of_cells = number_of_cells
        self.snake_speed = snake_speed
        self.snake_initial_size = snake_initial_size
        self.human_player = human_player
        self.snakes = []
        self.dead_snakes = []
        self.number_of_generations = number_of_generations
        self.number_of_snakes = number_of_snakes
        self.show_screen = show_screen
        self.breeder = Breeder(mutation_rate)
        self.number_of_snakes_to_save = number_of_snakes_to_save
        self.batch_name = batch_name
        self.training = training
        if human_player or show_screen:
            self.painter = Painter(pygame, cell_size, number_of_cells, snake_color, apple_color, background_color,
                                   frames_per_second)

    def play_game(self):

        if not self.human_player:
            if self.training:
                self.snakes = self.generate_snakes(self.number_of_snakes)

                for i in range(self.number_of_generations):
                    self.play_generation(i + 1)
                    new_snakes = self.generate_snakes(self.number_of_snakes)
                    self.snakes = self.breeder.mutate_snakes(new_snakes, self.dead_snakes)

                self.save_best_snakes()
            else:
                snake = self.generate_snakes(1)
                snake.brain.load_from_file("2019_06_18_20_53_snake_1")
                self.play_snake(snake)

        else:
            snake = self.generate_snakes(1)
            self.play_snake(snake)

    def play_snake(self, snake):
        game_over = False

        if not self.human_player:
            while not game_over:

                self.painter.paint([snake])

                for event in pygame.event.get():
                    self.check_for_exit(event)

                self.play_one_turn_for_snake(snake)

                if not snake.alive:
                    game_over = True
                    pass

        else:
            while not game_over:

                self.painter.paint([snake])

                for event in pygame.event.get():
                    self.check_for_exit(event)
                    self.update_direction(event, snake)

                snake.update_position()
                self.check_if_apple_has_been_eaten(snake)
                self.check_if_snake_is_dead(snake)

                if not snake.alive:
                    game_over = True
                    pass

    @staticmethod
    def update_direction(event, snake):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                snake.set_direction("right")
            elif event.key == pygame.K_UP:
                snake.set_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.set_direction("down")

    def play_generation(self, gen):
        print("GENERATION: " + str(gen))
        game_over = False
        self.dead_snakes = []
        while not game_over:
            if self.show_screen:

                for event in pygame.event.get():
                    self.check_for_exit(event)

                self.painter.paint(self.snakes)

            for snake in self.snakes:
                self.play_one_turn_for_snake(snake)

            self.remove_dead_snakes()

            if len(self.snakes) is 0:
                game_over = True
                pass

    def find_position_for_apple(self, snake):
        segments = snake.get_segments()
        positions_blocked_by_snake = set()
        for segment in segments:
            positions_blocked_by_snake.add((segment.position_x, segment.position_y))
        apple_position = (random.randrange(0, self.number_of_cells), random.randrange(0, self.number_of_cells))
        while apple_position in positions_blocked_by_snake:
            apple_position = (random.randrange(0, self.number_of_cells), random.randrange(0, self.number_of_cells))
        return apple_position[0], apple_position[1]

    def generate_snakes(self, number_of_snakes):
        snakes = []
        for i in range(number_of_snakes):
            snake_direction = random.choice(["left", "right", "up", "down"])
            snake_position = [
                random.randrange((self.snake_initial_size - 1), self.number_of_cells - self.snake_initial_size),
                random.randrange((self.snake_initial_size - 1), self.number_of_cells - self.snake_initial_size)]
            if self.human_player:
                snake = SnakePlayer(snake_position, snake_direction, speed=self.snake_speed,
                                    length=self.snake_initial_size)
            else:
                snake = SnakeAI(snake_position, snake_direction, self.number_of_cells,
                                speed=self.snake_speed, length=self.snake_initial_size)
            position_x, position_y = self.find_position_for_apple(snake)
            snake.set_apple(Apple(position_x, position_y))
            snakes.append(snake)
        if len(snakes) == 1:
            return snakes[0]
        else:
            return snakes

    def check_if_apple_has_been_eaten(self, snake):
        segments = snake.get_segments()
        head_of_snake = segments[0]
        if head_of_snake.position_x == snake.apple.position_x and \
                head_of_snake.position_y == snake.apple.position_y:
            snake.apple.eaten = True
            position_x, position_y = self.find_position_for_apple(snake)
            snake.set_apple(Apple(position_x, position_y))
            snake.add_a_segment()

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()

    def check_if_snake_is_dead(self, snake):
        hit_border = self.check_if_snake_hit_border(snake)
        hit_itself = self.check_if_snake_hit_itself(snake)
        if hit_border or hit_itself or snake.time_since_last_apple > self.number_of_cells ** 2:
            snake.alive = False

    def check_if_snake_hit_border(self, snake):
        head_of_the_snake = snake.get_segments()[0]
        if head_of_the_snake.position_x < 0 or head_of_the_snake.position_x >= self.number_of_cells:
            return True
        if head_of_the_snake.position_y < 0 or head_of_the_snake.position_y >= self.number_of_cells:
            return True

        return False

    @staticmethod
    def check_if_snake_hit_itself(snake):
        head_of_the_snake = snake.get_segments()[0]
        segments = snake.get_segments()[1:]
        for segment in segments:
            if head_of_the_snake.position_x == segment.position_x and head_of_the_snake.position_y == segment.position_y:
                return True
        return False

    def get_state_of_the_board(self, snake):
        state_of_the_game = [-1] * self.number_of_cells * self.number_of_cells

        apple_cell_x = int(snake.apple.position_x)
        apple_cell_y = int(snake.apple.position_y)
        state_of_the_game[apple_cell_x + apple_cell_y * self.number_of_cells] = -10

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (apple_cell_x + i < 0) or (apple_cell_x + i >= self.number_of_cells) or (
                        apple_cell_y + j < 0) or (apple_cell_y + j >= self.number_of_cells):
                    continue

                state_of_the_game[apple_cell_x + i + (apple_cell_y + j) * self.number_of_cells] = -5

        for i in range(len(snake.get_segments())):
            segments = snake.get_segments()
            if i is 0:
                index = int(segments[i].position_x) + int(
                    segments[i].position_y) * self.number_of_cells
                state_of_the_game[index] = 4
            else:
                state_of_the_game[int(segments[i].position_x) + int(
                    segments[i].position_y) * self.number_of_cells] = 2
        return state_of_the_game

    def get_snake_perceptions(self, snake):
        # perception left, up, right, down. First apple, then body
        perception = [0] * 4
        head = snake.get_segments()[0]
        head_x = head.position_x
        head_y = head.position_y
        apple_position_x = snake.apple.position_x
        apple_position_y = snake.apple.position_y
        if head_x == apple_position_x:
            distance_in_y = head_y - apple_position_y
            if distance_in_y > 0:
                # Apple is up
                perception[1] = abs(distance_in_y)
            else:
                perception[3] = abs(distance_in_y)

        if head_y == apple_position_y:
            distance_in_x = head_x - apple_position_x
            if distance_in_x > 0:
                # Apple is left
                perception[0] = abs(distance_in_x)
            else:
                perception[2] = abs(distance_in_x)
        return perception

    def get_snake_perceptions_2(self, snake):
        # left, ahead, right, apple, obstacle
        perception = [0] * 7
        head = snake.get_segments()[0]
        head_x = head.position_x
        head_y = head.position_y
        apple_position_x = snake.apple.position_x
        apple_position_y = snake.apple.position_y
        left_cell, ahead_cell, right_cell = self.find_cell_lef_ahead_right(snake)
        # apple_cell = (snake.apple.position_x, snake.apple.position_y)
        # if apple_cell == left_cell:
        #     perception[0] = 1
        # elif apple_cell == ahead_cell:
        #     perception[1] = 1
        # elif apple_cell == right_cell:
        #     perception[2] = 1

        if head_x == apple_position_x:
            distance_in_y = head_y - apple_position_y
            if distance_in_y > 0:
                # Apple is up
                perception[1] = 1
            else:
                perception[3] = 1

        if head_y == apple_position_y:
            distance_in_x = head_x - apple_position_x
            if distance_in_x > 0:
                # Apple is left
                perception[0] = 1
            else:
                perception[2] = 1

        if self.is_cell_outside_of_the_map(left_cell):
            perception[4] = 1
        elif self.is_cell_outside_of_the_map(ahead_cell):
            perception[5] = 1
        elif self.is_cell_outside_of_the_map(right_cell):
            perception[6] = 1

        if self.is_cell_colliding_with_snake(left_cell, snake):
            perception[4] = 1
        elif self.is_cell_colliding_with_snake(ahead_cell, snake):
            perception[5] = 1
        elif self.is_cell_colliding_with_snake(right_cell, snake):
            perception[6] = 1

        return perception

    def find_cell_lef_ahead_right(self, snake):
        head = snake.get_segments()[0]
        head_x = head.position_x
        head_y = head.position_y
        if snake.direction is "up":
            left_cell = (head_x - 1, head_y)
            right_cell = (head_x + 1, head_y)
            ahead_cell = (head_x, head_y - 1)
        elif snake.direction is "down":
            left_cell = (head_x + 1, head_y)
            right_cell = (head_x - 1, head_y)
            ahead_cell = (head_x, head_y + 1)
        elif snake.direction is "right":
            left_cell = (head_x, head_y - 1)
            right_cell = (head_x, head_y + 1)
            ahead_cell = (head_x + 1, head_y)
        else:
            left_cell = (head_x, head_y + 1)
            right_cell = (head_x, head_y - 1)
            ahead_cell = (head_x - 1, head_y)

        return left_cell, ahead_cell, right_cell

    def is_cell_outside_of_the_map(self, cell):
        position_x = cell[0]
        position_y = cell[1]
        if position_y >= self.number_of_cells or position_y < 0 or position_x >= self.number_of_cells or position_x < 0:
            return True
        else:
            return False

    def is_cell_colliding_with_snake(self, cell, snake):
        position_x = cell[0]
        position_y = cell[1]
        segments = snake.get_segments()
        for segment in segments:
            if position_x == segment.position_x and position_y == segment.position_y:
                return True
        return False

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 255, 0))
        return text_surface, text_surface.get_rect()

    def remove_dead_snakes(self):
        for i in range(len(self.snakes)):
            if not self.snakes[i].alive:
                self.dead_snakes.append(self.snakes[i])
        self.snakes = [x for x in self.snakes if x.alive]

    def play_one_turn_for_snake(self, snake):
        snake.set_direction(self.get_snake_perceptions_2(snake))
        snake.update_position()
        self.check_if_apple_has_been_eaten(snake)
        self.check_if_snake_is_dead(snake)

    def save_best_snakes(self):
        if self.batch_name is None:
            now = datetime.datetime.now()
            self.batch_name = now.strftime("%Y_%m_%d_%H_%M")
        for i in range(self.number_of_snakes_to_save):
            self.snakes[i].brain.save_to_file(self.batch_name + "_snake_" + str(i))
