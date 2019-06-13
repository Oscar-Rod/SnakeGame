class Painter:

    def __init__(self, pygame, cell_size, number_of_cells, snake_color, apple_color, background_color,
                 frames_per_second):
        self.pygame = pygame
        self.pygame.init()
        self.cell_size = cell_size
        self.number_of_cells = number_of_cells
        self.map_size = int(cell_size * (number_of_cells + 4))
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.background_color = background_color
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.map_size, self.map_size))
        self.frames_per_second = frames_per_second

    def paint(self, snakes):
        self.screen.fill(self.background_color)
        self.pygame.draw.lines(self.screen, self.snake_color, True,
                               [[self.cell_size * 2, self.cell_size * 2],
                                [self.map_size - self.cell_size * 2, self.cell_size * 2],
                                [self.map_size - self.cell_size * 2, self.map_size - self.cell_size * 2],
                                [self.cell_size * 2, self.map_size - self.cell_size * 2]])

        for snake in snakes:
            segments = snake.get_segments()
            for segment in segments:
                self.pygame.draw.rect(self.screen, self.snake_color, (
                    (segment.position_x + 2) * self.cell_size, (segment.position_y + 2) * self.cell_size,
                    self.cell_size,
                    self.cell_size))

            self.pygame.draw.rect(self.screen, self.apple_color, (
                (snake.apple.position_x + 2) * self.cell_size,
                (snake.apple.position_y + 2) * self.cell_size, self.cell_size,
                self.cell_size))

        self.clock.tick(self.frames_per_second)

        self.pygame.display.update()
