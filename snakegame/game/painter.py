import pygame

from snakegame.game.button import Button


class Painter:

    def __init__(self, cell_size, number_of_cells, snake_color, apple_color, background_color,
                 frames_per_second, resolution):
        pygame.init()
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
        self.buttons = self.initialize_buttons()

    def paint(self, snakes):
        self.screen.fill(self.background_color)
        self.paints_limits_of_the_playable_zone()
        self.paints_limits_of_the_game()
        self.paint_buttons()

        if snakes is not None:
            for snake in snakes:
                segments = snake.get_segments()
                for segment in segments:
                    pygame.draw.rect(self.screen, self.snake_color, (
                        (segment.position_x * self.cell_size + self.upper_left_corner_of_playable_game[0]),
                        (segment.position_y * self.cell_size + self.upper_left_corner_of_playable_game[1]),
                        self.cell_size,
                        self.cell_size))

                pygame.draw.rect(self.screen, self.apple_color, (
                    (snake.apple.position_x * self.cell_size + self.upper_left_corner_of_playable_game[0]),
                    (snake.apple.position_y * self.cell_size + self.upper_left_corner_of_playable_game[1]),
                    self.cell_size,
                    self.cell_size))

        self.clock.tick(self.frames_per_second)

        pygame.display.update()

    def paints_limits_of_the_playable_zone(self):

        pygame.draw.lines(self.screen, self.snake_color, True,
                          [[self.center_of_playable_zone_x - self.length_of_playable_zone / 2,
                            self.center_of_playable_zone_y - self.length_of_playable_zone / 2],
                           [self.center_of_playable_zone_x + self.length_of_playable_zone / 2,
                            self.center_of_playable_zone_y - self.length_of_playable_zone / 2],
                           [self.center_of_playable_zone_x + self.length_of_playable_zone / 2,
                            self.center_of_playable_zone_y + self.length_of_playable_zone / 2],
                           [self.center_of_playable_zone_x - self.length_of_playable_zone / 2,
                            self.center_of_playable_zone_y + self.length_of_playable_zone / 2]])

    def paints_limits_of_the_game(self):
        pygame.draw.lines(self.screen, self.snake_color, True,
                          [[self.resolution[0] * self.limit_of_the_game, 0],
                           [self.resolution[0], 0],
                           [self.resolution[0], self.resolution[1]],
                           [self.resolution[0] * self.limit_of_the_game, self.resolution[1]]])

    def paint_buttons(self):
        for button in self.buttons:
            button.draw()

    def initialize_buttons(self):
        buttons = []
        button_height = 50
        button_width = 100
        center_of_the_buttons_area = (self.resolution[0] * self.limit_of_the_game / 2, self.resolution[1] / 2)
        center_of_the_start_button = (center_of_the_buttons_area[0] - button_width / 2, center_of_the_buttons_area[1])
        center_of_the_stop_button = (center_of_the_buttons_area[0] + button_width / 2, center_of_the_buttons_area[1])

        start_button = Button(Button.start_the_game, "Start", "black", "green", center_of_the_start_button,
                              button_width, button_height,
                              self.screen)

        stop_button = Button(Button.stop_the_game, "Stop", "black", "red", center_of_the_stop_button, button_width,
                             button_height,
                             self.screen)
        buttons.append(start_button)
        buttons.append(stop_button)
        return buttons
