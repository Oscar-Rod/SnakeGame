from snakegame.game.brain import Brain
from snakegame.game.snake import Snake


class SnakeAI(Snake):
    def __init__(self, position, direction, number_of_cells, length=5, speed=1):
        super().__init__(position, direction, length, speed)
        self.brain = Brain(number_of_cells, None)

    def set_direction(self, number_of_cells):
        x = self.brain.predict(self, number_of_cells)
        max = -float("inf")
        value = -1
        for i in range(4):
            if x[i] > max:
                max = x[i]
                value = i
        directions = ["left", "right", "up", "down"]
        direction = directions[value]

        is_valid = self.check_is_a_valid_direction(direction)
        if is_valid:
            self.direction = direction
            self.set_speeds(direction)
