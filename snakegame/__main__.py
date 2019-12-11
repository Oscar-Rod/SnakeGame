import argparse

from snakegame import play

parser = argparse.ArgumentParser()

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15

snake_vision = "snakevision"
board_state = "boardstate"

show_screen = True
human_player = False
training = True
perception = board_state

snake_initial_size = 5
number_of_cells = 25

speed = 100
number_of_snakes_to_save = 10
number_of_generations = 150
number_of_snakes = 300
mutation_rate = 0.3

parser.add_argument("--resolution", type=tuple, default=(1500, 1000))
parser.add_argument("--perception", type=str, default=snake_vision)
parser.add_argument("--show_screen", type=bool, default=show_screen)
parser.add_argument("--human_player", type=bool, default=human_player)
parser.add_argument("--training", type=bool, default=training)

parser.add_argument("--snake_initial_size", type=int, default=snake_initial_size)
parser.add_argument("--number_of_cells", type=int, default=number_of_cells)
parser.add_argument("--speed", type=int, default=speed)
parser.add_argument("--number_of_snakes_to_save", type=int, default=number_of_snakes_to_save)
parser.add_argument("--number_of_generations", type=int, default=number_of_generations)
parser.add_argument("--number_of_snakes", type=int, default=number_of_snakes)

parser.add_argument("--mutation_rate", type=float, default=mutation_rate)

args = parser.parse_args()

if __name__ == '__main__':
    play.run(args.resolution, args.speed, args.show_screen, args.human_player, args.training,
             args.number_of_snakes_to_save,
             args.snake_initial_size, args.number_of_cells, args.number_of_generations, args.number_of_snakes,
             args.mutation_rate, args.perception)
