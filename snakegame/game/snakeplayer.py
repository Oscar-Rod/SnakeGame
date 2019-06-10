from snakegame.game.snake import Snake


class SnakePlayer(Snake):
    def __init__(self, position, direction, cell_size=15, length=5, speed=1):
        super().__init__(position, direction, cell_size, length, speed)

    def set_direction(self, direction):
        is_valid = self.check_is_a_valid_direction(direction)
        if is_valid:
            self.direction = direction
            self.set_speeds(direction)
