import copy
import random
import sys

import pygame

from snakegame.game.apple import Apple
from snakegame.game.snakeAI import SnakeAI
from snakegame.game.snakeplayer import SnakePlayer


class Motor:
    def __init__(self, snake_speed, screen, snake_color=(255, 255, 255), background_color=(0, 0, 0), number_of_cells=40,
                 cell_size=15,
                 frames_per_second=60, apple_color=(0, 255, 0), snake_initial_size=5, is_training=False,
                 number_of_generations=10, number_of_snakes=10, mutation_rate=0.1):
        self.map_size = int(cell_size * number_of_cells)
        self.number_of_cells = number_of_cells
        self.snake_speed = snake_speed
        self.snake_initial_size = snake_initial_size
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.background_color = background_color
        self.cell_size = cell_size
        self.frames_per_second = frames_per_second
        self.is_training = is_training
        self.snakes = []
        self.dead_snakes = []
        self.number_of_generations = number_of_generations
        self.number_of_snakes = number_of_snakes
        self.mutation_rate = mutation_rate
        self.screen = screen

    def play_game(self):
        clock = None
        screen = None
        if self.screen:
            pygame.init()
            screen = pygame.display.set_mode((self.map_size, self.map_size))
            clock = pygame.time.Clock()
        self.snakes = self.generate_snakes()

        for i in range(self.number_of_generations):
            self.play_generation(i + 1, clock, screen)
            self.mutate_snakes()

    def play_generation(self, gen, clock=None, screen=None):
        print("GENERATION: " + str(gen))
        game_over = False
        self.dead_snakes = []
        while not game_over:
            if self.screen:
                screen.fill(self.background_color)
                self.message_display('Generation {}'.format(gen), 20, 70, 35, screen)

                for event in pygame.event.get():
                    self.check_for_exit(event)

                # if not self.is_training:
                #     self.update_direction(event)

            for i in range(len(self.snakes)):
                self.play_one_turn_for_snake(i)

            self.remove_dead_snakes()

            if len(self.snakes) is 0:
                game_over = True
                pass

            if self.screen:
                for i in range(len(self.snakes)):
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
                segment.position_x * self.cell_size, segment.position_y * self.cell_size, self.cell_size,
                self.cell_size))

    def draw_apple(self, screen, snake_number):
        pygame.draw.rect(screen, self.apple_color, (
            self.snakes[snake_number].apple.position_x * self.cell_size,
            self.snakes[snake_number].apple.position_y * self.cell_size, self.cell_size,
            self.cell_size))

    def find_position_for_apple(self, snake):
        segments = snake.get_segments()
        positions_blocked_by_snake = [[], []]
        for segment in segments:
            positions_blocked_by_snake[0].append(segment.position_x)
            positions_blocked_by_snake[1].append(segment.position_y)
        position_x = random.randrange(0, self.number_of_cells)
        while position_x in positions_blocked_by_snake[0]:
            position_x = random.randrange(0, self.number_of_cells)
        position_y = random.randrange(0, self.number_of_cells)
        while position_y in positions_blocked_by_snake[1]:
            position_y = random.randrange(0, self.number_of_cells)
        return position_x, position_y

    def generate_snakes(self):
        snakes = []
        for i in range(self.number_of_snakes):
            snake_direction = random.choice(["left", "right", "up", "down"])
            snake_position = [
                random.randrange((self.snake_initial_size - 1), self.number_of_cells - self.snake_initial_size),
                random.randrange((self.snake_initial_size - 1), self.number_of_cells - self.snake_initial_size)]
            if not self.is_training:
                snake = SnakePlayer(snake_position, snake_direction, speed=self.snake_speed,
                                    length=self.snake_initial_size)
            else:
                snake = SnakeAI(snake_position, snake_direction, self.number_of_cells,
                                speed=self.snake_speed, length=self.snake_initial_size)
            position_x, position_y = self.find_position_for_apple(snake)
            snake.set_apple(Apple(position_x, position_y))
            snakes.append(snake)
        return snakes

    def check_if_apple_has_been_eaten(self, snake_number):
        segments = self.snakes[snake_number].get_segments()
        head_of_snake = segments[0]
        if head_of_snake.position_x == self.snakes[snake_number].apple.position_x and \
                head_of_snake.position_y == self.snakes[snake_number].apple.position_y:
            self.snakes[snake_number].apple.eaten = True
            position_x, position_y = self.find_position_for_apple(self.snakes[snake_number])
            self.snakes[snake_number].set_apple(Apple(position_x, position_y))
            self.snakes[snake_number].add_a_segment()

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()

    def check_if_snake_is_dead(self, snake_number):
        hit_border = self.check_if_snake_hit_border(snake_number)
        hit_itself = self.check_if_snake_hit_itself(snake_number)
        if hit_border or hit_itself or self.snakes[snake_number].time_since_last_apple > self.number_of_cells ** 2:
            self.snakes[snake_number].alive = False

    def check_if_snake_hit_border(self, snake_number):
        head_of_the_snake = self.snakes[snake_number].get_segments()[0]
        if head_of_the_snake.position_x < 0 or head_of_the_snake.position_x >= self.number_of_cells:
            return True
        if head_of_the_snake.position_y < 0 or head_of_the_snake.position_y >= self.number_of_cells:
            return True

        return False

    def check_if_snake_hit_itself(self, snake_number):
        head_of_the_snake = self.snakes[snake_number].get_segments()[0]
        segments = self.snakes[snake_number].get_segments()[1:]
        for segment in segments:
            if head_of_the_snake.position_x == segment.position_x and head_of_the_snake.position_y == segment.position_y:
                return True
        return False

    def get_state_of_the_board(self, snake_number):
        state_of_the_game = [-1] * self.number_of_cells * self.number_of_cells

        apple_cell_x = int(self.snakes[snake_number].apple.position_x / self.cell_size)
        apple_cell_y = int(self.snakes[snake_number].apple.position_y / self.cell_size)
        state_of_the_game[apple_cell_x + apple_cell_y * self.number_of_cells] = -10

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (apple_cell_x + i < 0) or (apple_cell_x + i >= self.number_of_cells) or (
                        apple_cell_y + j < 0) or (apple_cell_y + j >= self.number_of_cells):
                    continue

                state_of_the_game[apple_cell_x + i + (apple_cell_y + j) * self.number_of_cells] = -5

        for i in range(len(self.snakes[snake_number].get_segments())):
            segments = self.snakes[snake_number].get_segments()
            if i is 0:
                index = int(segments[i].position_x / self.cell_size) + int(
                    segments[i].position_y / self.cell_size) * self.number_of_cells
                state_of_the_game[index] = 4
            else:
                state_of_the_game[int(segments[i].position_x / self.cell_size) + int(
                    segments[i].position_y / self.cell_size) * self.number_of_cells] = 2
        return state_of_the_game

    def get_snake_perceptions(self, snake_number):
        # perception left, up, right, down. First apple, then body
        perception = [0] * 4
        snake = self.snakes[snake_number]
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

    def get_snake_perceptions_2(self, snake_number):
        # left, ahead, right, apple, obstacle
        perception = [0] * 7
        snake = self.snakes[snake_number]
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

    def message_display(self, text, size, posx, posy, window):
        large_text = pygame.font.Font('freesansbold.ttf', size)
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.center = (posx, posy)
        window.blit(text_surf, text_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 255, 0))
        return text_surface, text_surface.get_rect()

    def remove_dead_snakes(self):
        for i in range(len(self.snakes)):
            if not self.snakes[i].alive:
                self.dead_snakes.append(self.snakes[i])
        self.snakes = [x for x in self.snakes if x.alive]

    def mutate_snakes(self):
        self.snakes = self.generate_snakes()
        self.order_dead_snakes_by_performance()
        number_of_snakes = len(self.dead_snakes)
        number_of_snakes_unchanged = int(number_of_snakes * 0.001)
        number_of_snakes_breded = int(number_of_snakes * 0.009)
        for i in range(int(number_of_snakes * 0.99)):
            if i is 0:
                print("score: " + str(self.dead_snakes[i].score))
                print("length: " + str(self.dead_snakes[i].length))
                print()
            if i <= number_of_snakes_unchanged:
                self.snakes[i].brain = self.dead_snakes[i].brain
            else:
                brain1 = random.choice(self.dead_snakes[number_of_snakes_unchanged:number_of_snakes_breded]).brain
                brain2 = random.choice(self.dead_snakes[number_of_snakes_unchanged:number_of_snakes_breded]).brain
                new_brain = copy.deepcopy(brain1)
                new_brain.combine(brain2)
                if bool(random.getrandbits(1)):
                    new_brain.mutate(self.mutation_rate)
                self.snakes[i].brain = new_brain

    def order_dead_snakes_by_performance(self):
        self.dead_snakes.sort(key=lambda x: x.score, reverse=True)

    def play_one_turn_for_snake(self, snake_number):
        self.snakes[snake_number].set_direction(self.get_snake_perceptions_2(snake_number))
        self.snakes[snake_number].update_position()
        self.check_if_apple_has_been_eaten(snake_number)
        self.check_if_snake_is_dead(snake_number)
