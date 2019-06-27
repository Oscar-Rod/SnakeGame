from snakegame.game.motor import Motor

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15

snake_vision = "snakevision"
board_state = "boardstate"

show_screen = False
human_player = False
training = True
perception = board_state

number_of_snakes_to_save = 10
number_of_generations = 100
number_of_snakes = 300
mutation_rate = 0.3

game_motor = Motor(100, show_screen=show_screen, human_player=human_player, training=training,
                   number_of_snakes_to_save=number_of_snakes_to_save, snake_initial_size=5, number_of_cells=20,
                   number_of_generations=number_of_generations, number_of_snakes=number_of_snakes,
                   mutation_rate=mutation_rate, perception=perception)

game_motor.play_game()
