from snakegame.game.motor import Motor
from snakegame.game.snake import Snake

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
square_size = 15


game_motor = Motor(cell_size=square_size, frames_per_second=60)

game_motor.play_game()
