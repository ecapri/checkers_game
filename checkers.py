# Eric Capri 2/15/2022
# CS 405 - HW 2
# Implementation of MiniMax Search

import pygame
from constants import HEIGHT, FULL_WIDTH
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
            print(game.count)
            break

        if game.turn.computer:
            game.move_generator()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                row = y // 100
                col = x // 100
                if row > 7 or col > 7:
                    continue
                game.select(row, col)

        game.update()


if __name__ == '__main__':
    main()
