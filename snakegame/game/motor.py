import os
import pickle
import sys

import pygame

from snakegame.game.board import Board
from snakegame.game.button import Button
from snakegame.game.painter import Painter
from snakegame.neural_network.geneticalgorithm import Breeder


class Motor:
    def __init__(self, resolution, snake_speed, show_screen=True, snake_color=(255, 255, 255),
                 background_color=(0, 0, 0),
                 number_of_cells=40, cell_size=15, frames_per_second=60, apple_color=(0, 255, 0), snake_initial_size=5,
                 human_player=True, number_of_generations=10, number_of_snakes=10, mutation_rate=0.1,
                 number_of_snakes_to_save=10, perception=None, training=False):
        self.snake_speed = snake_speed
        self.snake_initial_size = snake_initial_size
        self.human_player = human_player
        self.snakes = []
        self.dead_snakes = []
        self.number_of_generations = number_of_generations
        self.number_of_snakes = number_of_snakes
        self.show_screen = show_screen
        self.breeder = Breeder(mutation_rate)
        self.number_of_snakes_to_save = number_of_snakes_to_save
        self.perception = perception
        self.training = training
        self.board = Board(number_of_cells)
        self.painter = Painter(cell_size, number_of_cells, snake_color, apple_color, background_color,
                               frames_per_second, resolution)

    def play_game(self):

        self.painter.paint([])
        start = False
        while not start:
            for event in pygame.event.get():
                self.check_for_exit(event)
                actions_list = Button.pass_event_to_all_buttons(event)
                if Button.start_the_game in actions_list:
                    start = True

        if self.training:
            self.train()
        else:
            self.play()

    def train(self):
        self.snakes = self.board.generate_snakes(self.number_of_snakes, self.snake_initial_size,
                                                 self.snake_speed, self.perception, self.human_player)
        for i in range(self.number_of_generations):
            self.train_generation(i + 1)
            new_snakes = self.board.generate_snakes(self.number_of_snakes, self.snake_initial_size,
                                                    self.snake_speed, self.perception, self.human_player)
            self.snakes = self.breeder.mutate_snakes(new_snakes, self.dead_snakes)
        self.save_best_snakes()

    def train_generation(self, gen):
        print("GENERATION: " + str(gen))
        game_over = False
        self.dead_snakes = []
        while not game_over:
            if self.show_screen:

                for event in pygame.event.get():
                    self.check_for_exit(event)
                    actions_list = Button.pass_event_to_all_buttons(event)
                    if Button.stop_the_game in actions_list:
                        sys.exit()

                self.painter.paint(self.snakes)

            for snake in self.snakes:
                self.play_one_turn_for_snake(snake)

            self.remove_dead_snakes()

            if len(self.snakes) is 0:
                game_over = True
                pass

    def play(self):
        snake = self.board.generate_snakes(1, self.snake_initial_size, self.snake_speed, None, self.human_player)
        if not self.human_player:
            self.load_from_file(snake, self.perception)
        self.play_snake(snake)

    def play_snake(self, snake):
        game_over = False

        if not self.human_player:
            while not game_over:

                self.painter.paint([snake])

                for event in pygame.event.get():
                    self.check_for_exit(event)
                    actions_list = Button.pass_event_to_all_buttons(event)
                    if Button.stop_the_game in actions_list:
                        sys.exit()

                self.play_one_turn_for_snake(snake)

                if not snake.alive:
                    game_over = True
                    pass

        else:
            while not game_over:

                self.painter.paint([snake])

                for event in pygame.event.get():
                    self.check_for_exit(event)
                    self.update_direction(event, snake)
                    actions_list = Button.pass_event_to_all_buttons(event)
                    if Button.stop_the_game in actions_list:
                        sys.exit()

                snake.update_position()
                self.board.check_if_apple_has_been_eaten(snake)
                self.board.check_if_snake_is_dead(snake)

                if not snake.alive:
                    game_over = True
                    pass

    @staticmethod
    def update_direction(event, snake):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                snake.set_direction("right")
            elif event.key == pygame.K_UP:
                snake.set_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.set_direction("down")

    @staticmethod
    def check_for_exit(event):
        if event.type == pygame.QUIT:
            sys.exit()

    def remove_dead_snakes(self):
        for i in range(len(self.snakes)):
            if not self.snakes[i].alive:
                self.dead_snakes.append(self.snakes[i])
        self.snakes = [x for x in self.snakes if x.alive]

    def play_one_turn_for_snake(self, snake):
        snake.set_direction()
        snake.update_position()
        self.board.check_if_apple_has_been_eaten(snake)
        self.board.check_if_snake_is_dead(snake)

    def save_best_snakes(self):
        parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(parent_folder)
        if parent_folder.split("/")[-1] != "snakegame" or parent_folder.split("/")[-2] != "snakegame":
            raise Exception("Trying to save brain to a wrong folder")
        folder = parent_folder + "/brains/" + self.perception
        if not os.path.exists(folder):
            os.makedirs(folder)

        files = os.listdir(folder)

        for i in range(self.number_of_snakes_to_save):
            brain = self.dead_snakes[i].brain
            filename = "length_" + str(self.dead_snakes[i].length) + "_score_" + str(self.dead_snakes[i].score)
            self.save_to_file(brain, folder, filename)

        number_of_snakes_to_keep = max(len(files), self.number_of_snakes_to_save)

        self.remove_worst_snakes(folder, number_of_snakes_to_keep)

    @staticmethod
    def save_to_file(brain, folder, filename):
        with open(folder + "/" + filename + ".pkl", "wb") as output:
            pickle.dump(brain, output, pickle.HIGHEST_PROTOCOL)

    def remove_worst_snakes(self, folder, number_of_snakes_to_keep):
        files = os.listdir(folder)
        number_of_snakes_to_remove = len(files) - number_of_snakes_to_keep
        if number_of_snakes_to_remove <= 0:
            return

        files_with_score = []

        for file in files:
            split_name = file.split("_")
            length = split_name[1]
            score = split_name[3]
            files_with_score.append((file, length, score))

        files_with_score.sort(key=lambda tup: (tup[1], tup[2]), reverse=True)

        files_to_remove = files_with_score[-number_of_snakes_to_remove:]

        for file in files_to_remove:
            os.remove(folder + "/" + file[0])

    @staticmethod
    def load_from_file(snake, folder):
        folder = "../brains/" + folder
        files = os.listdir(folder)
        with open(folder + "/" + files[0], "rb") as file:
            brain = pickle.load(file)
            snake.brain = brain
