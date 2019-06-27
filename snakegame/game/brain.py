from snakegame.neural_network.neuralnetwork import NeuralNetwork


class Brain:

    def __init__(self, perception, number_of_cells):
        self.perception = perception
        self.number_of_cells = number_of_cells
        self.neural_network = NeuralNetwork(self.set_architecture())

    def set_architecture(self):
        nn_architecture = [
            {"input_dim": 7, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 40, "activation": "relu"},
            {"input_dim": 40, "output_dim": 4, "activation": "sigmoid"},
        ]
        return nn_architecture

    def predict(self, snake, number_of_cells):
        perception = getattr(self, self.perception)
        X = perception(snake, number_of_cells)
        return self.neural_network.predict(X)

    def mutate(self, mutation_rate):
        self.neural_network.mutate(mutation_rate)

    def combine(self, second_brain):
        self.neural_network.combine(second_brain.neural_network)

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

    def snake_vision(self, snake, number_of_cells):
        # left, ahead, right, apple, obstacle
        perception = [0] * 7
        head = snake.get_segments()[0]
        head_x = head.position_x
        head_y = head.position_y
        apple_position_x = snake.apple.position_x
        apple_position_y = snake.apple.position_y
        left_cell, ahead_cell, right_cell = self.find_cell_lef_ahead_right(snake)

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

        if self.is_cell_outside_of_the_map(left_cell, number_of_cells):
            perception[4] = 1
        elif self.is_cell_outside_of_the_map(ahead_cell, number_of_cells):
            perception[5] = 1
        elif self.is_cell_outside_of_the_map(right_cell, number_of_cells):
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

    def is_cell_outside_of_the_map(self, cell, number_of_cells):
        position_x = cell[0]
        position_y = cell[1]
        if position_y >= number_of_cells or position_y < 0 or position_x >= number_of_cells or position_x < 0:
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
