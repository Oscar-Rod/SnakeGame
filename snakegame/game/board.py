import random

from snakegame.game.apple import Apple
from snakegame.game.snakeAI import SnakeAI
from snakegame.game.snakeplayer import SnakePlayer


class Board:
    def __init__(self, number_of_cells):
        self.number_of_cells = number_of_cells

    def find_position_for_apple(self, snake):
        segments = snake.get_segments()
        positions_blocked_by_snake = set()
        for segment in segments:
            positions_blocked_by_snake.add((segment.position_x, segment.position_y))
        apple_position = (random.randrange(0, self.number_of_cells), random.randrange(0, self.number_of_cells))
        while apple_position in positions_blocked_by_snake:
            apple_position = (random.randrange(0, self.number_of_cells), random.randrange(0, self.number_of_cells))
        return apple_position[0], apple_position[1]

    def generate_snakes(self, number_of_snakes, snake_initial_size, snake_speed, perception, human_player):
        snakes = []
        for i in range(number_of_snakes):
            snake_direction = random.choice(["left", "right", "up", "down"])
            snake_position = [
                random.randrange((snake_initial_size - 1), self.number_of_cells - snake_initial_size),
                random.randrange((snake_initial_size - 1), self.number_of_cells - snake_initial_size)]
            if human_player:
                snake = SnakePlayer(snake_position, snake_direction, speed=snake_speed,
                                    length=snake_initial_size)
            else:
                snake = SnakeAI(snake_position, snake_direction, perception, self.number_of_cells,
                                speed=snake_speed, length=snake_initial_size)
            position_x, position_y = self.find_position_for_apple(snake)
            snake.set_apple(Apple(position_x, position_y))
            snakes.append(snake)
        if len(snakes) == 1:
            return snakes[0]
        else:
            return snakes

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

    def check_if_apple_has_been_eaten(self, snake):
        segments = snake.get_segments()
        head_of_snake = segments[0]
        if head_of_snake.position_x == snake.apple.position_x and \
                head_of_snake.position_y == snake.apple.position_y:
            snake.apple.eaten = True
            position_x, position_y = self.find_position_for_apple(snake)
            snake.set_apple(Apple(position_x, position_y))
            snake.add_a_segment()