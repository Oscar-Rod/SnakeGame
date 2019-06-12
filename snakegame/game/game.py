from snakegame.game.motor import Motor

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15

game_motor = Motor(100, True, snake_initial_size=5, number_of_cells=20, is_training=True, number_of_generations=1000,
                   number_of_snakes=1000, mutation_rate=0.1)

game_motor.play_game()
