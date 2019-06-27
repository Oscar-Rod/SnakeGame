class BoardState:

    def __init__(self, number_of_cells):
        self.number_of_cells = number_of_cells

    def set_architecture(self):
        nn_architecture = [
            {"input_dim": self.number_of_cells**2, "output_dim": self.number_of_cells**2 * 2, "activation": "relu"},
            {"input_dim": self.number_of_cells**2 * 2, "output_dim": int(self.number_of_cells**2 / 2), "activation": "relu"},
            {"input_dim": int(self.number_of_cells**2 / 2), "output_dim": 4, "activation": "sigmoid"},
        ]
        return nn_architecture

    def get_perception(self, snake):
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