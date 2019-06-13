from snakegame.game.motor import Motor

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15

game_motor = Motor(100, show_screen=True, human_player=False, snake_initial_size=5, number_of_cells=20,
                   number_of_generations=5000, number_of_snakes=2000, mutation_rate=0.3)

game_motor.play_game()
