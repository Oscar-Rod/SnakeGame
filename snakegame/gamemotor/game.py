import sys

import pygame

pygame.init()

width = 1200
height = 1200
red = (255, 0, 0)
white = (255, 255, 255)
square_size = 15

screen = pygame.display.set_mode((width, height))

game_over = False

while not game_over:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            sys.exit()

    pygame.draw.rect(screen, white, (400, 300, square_size, square_size))

    pygame.display.update()
