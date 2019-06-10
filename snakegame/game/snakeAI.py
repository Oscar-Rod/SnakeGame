from snakegame.game.snake import Snake
from snakegame.neural_network.neuralnetwork import NeuralNetwork


class SnakeAI(Snake):
    def __init__(self, position, direction, cell_size=15, length=5, speed=1):
        super().__init__(position, direction, cell_size, length, speed)
        self.brain = NeuralNetwork(40 * 40, 20, 4)

    def set_direction(self, state_of_the_game):
        x = self.brain.predict(state_of_the_game)
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
