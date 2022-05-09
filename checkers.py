# Eric Capri 2/1/2022
# CS 405 - HW 1
# Implementation of Randomized Checkers Bot

import pygame
from constants import WIDTH, HEIGHT, GREY, FULL_WIDTH, FULL_HEIGHT
import gameEvents


def main():
    # initialize screen
    pygame.init()
    window = pygame.display.set_mode((FULL_WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')

    # initialize state
    game = gameEvents.Game(window)

    # event loop
    while 1:
        if game.gameOver() is not None:
            print(game.gameOver())
            break

        if game.turn.computer:
            game.randomBot()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                row = y // 100
                col = x // 100
                game.select(row, col)

        game.update()


if __name__ == '__main__':
    main()
