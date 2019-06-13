from snakegame.game.snake import Snake
from snakegame.neural_network.my_neuralnetwork import NeuralNetwork


class SnakeAI(Snake):
    def __init__(self, position, direction, number_of_cells, length=5, speed=1):
        super().__init__(position, direction, length, speed)
        self.brain = NeuralNetwork(self.set_architecture(number_of_cells))

    def set_architecture(self, number_of_cells):
        # nn_architecture = [
        #     {"input_dim": int(number_of_cells ** 2), "output_dim": int(number_of_cells), "activation": "relu"},
        #     {"input_dim": int(number_of_cells), "output_dim": int(number_of_cells), "activation": "relu"},
        #     {"input_dim": int(number_of_cells), "output_dim": int(number_of_cells), "activation": "relu"},
        #     {"input_dim": int(number_of_cells), "output_dim": int(number_of_cells), "activation": "relu"},
        #     {"input_dim": int(number_of_cells), "output_dim": int(number_of_cells / 2), "activation": "relu"},
        #     {"input_dim": int(number_of_cells / 2), "output_dim": 4, "activation": "sigmoid"},
        # ]
        nn_architecture = [
            {"input_dim": 7, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 4, "activation": "sigmoid"},
        ]
        return nn_architecture

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
