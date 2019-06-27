from snakegame.game.motor import Motor


def run(speed, show_screen, human_player, training, number_of_snakes_to_save, snake_initial_size, number_of_cells,
        number_of_generations, number_of_snakes, mutation_rate, perception):
    game_motor = Motor(speed, show_screen=show_screen, human_player=human_player, training=training,
                       number_of_snakes_to_save=number_of_snakes_to_save, snake_initial_size=snake_initial_size,
                       number_of_cells=number_of_cells, number_of_generations=number_of_generations,
                       number_of_snakes=number_of_snakes, mutation_rate=mutation_rate, perception=perception)

    game_motor.play_game()


if __name__ == '__main__':
    run()
