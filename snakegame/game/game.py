from snakegame.game.motor import Motor

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15

game_motor = Motor(90, is_training=True)

game_motor.play_game()
