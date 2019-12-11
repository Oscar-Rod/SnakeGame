class Painter:

    def __init__(self, pygame, cell_size, number_of_cells, snake_color, apple_color, background_color,
                 frames_per_second, resolution):
        self.pygame = pygame
        self.pygame.init()
        self.cell_size = cell_size
        self.number_of_cells = number_of_cells
        self.map_size = int(cell_size * (number_of_cells + 4))
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.background_color = background_color
        self.clock = pygame.time.Clock()
        self.resolution = resolution
        self.limit_of_the_game = 1 / 3
        self.screen = pygame.display.set_mode(resolution)
        self.frames_per_second = frames_per_second
        self.center_of_playable_zone_x = (self.resolution[0] + self.resolution[0] * self.limit_of_the_game) / 2
        self.center_of_playable_zone_y = self.resolution[1] / 2
        self.length_of_playable_zone = self.cell_size * self.number_of_cells
        self.upper_left_corner_of_playable_game = (self.center_of_playable_zone_x - self.length_of_playable_zone / 2,
                                                   self.center_of_playable_zone_y - self.length_of_playable_zone / 2)

    def paint(self, snakes):
        self.screen.fill(self.background_color)
        self.paints_limits_of_the_playable_zone()
        self.paints_limits_of_the_game()

        for snake in snakes:
            segments = snake.get_segments()
            for segment in segments:
                self.pygame.draw.rect(self.screen, self.snake_color, (
                    (segment.position_x * self.cell_size + self.upper_left_corner_of_playable_game[0]),
                    (segment.position_y * self.cell_size + self.upper_left_corner_of_playable_game[1]),
                    self.cell_size,
                    self.cell_size))

            self.pygame.draw.rect(self.screen, self.apple_color, (
                (snake.apple.position_x * self.cell_size + self.upper_left_corner_of_playable_game[0]),
                (snake.apple.position_y * self.cell_size + self.upper_left_corner_of_playable_game[1]),
                self.cell_size,
                self.cell_size))

        self.clock.tick(self.frames_per_second)

        self.pygame.display.update()

    def paints_limits_of_the_playable_zone(self):

        self.pygame.draw.lines(self.screen, self.snake_color, True,
                               [[self.center_of_playable_zone_x - self.length_of_playable_zone / 2,
                                 self.center_of_playable_zone_y - self.length_of_playable_zone / 2],
                                [self.center_of_playable_zone_x + self.length_of_playable_zone / 2,
                                 self.center_of_playable_zone_y - self.length_of_playable_zone / 2],
                                [self.center_of_playable_zone_x + self.length_of_playable_zone / 2,
                                 self.center_of_playable_zone_y + self.length_of_playable_zone / 2],
                                [self.center_of_playable_zone_x - self.length_of_playable_zone / 2,
                                 self.center_of_playable_zone_y + self.length_of_playable_zone / 2]])

    def paints_limits_of_the_game(self):
        self.pygame.draw.lines(self.screen, self.snake_color, True,
                               [[self.resolution[0] * self.limit_of_the_game, 0],
                                [self.resolution[0], 0],
                                [self.resolution[0], self.resolution[1]],
                                [self.resolution[0] * self.limit_of_the_game, self.resolution[1]]])
