# Eric Capri 2/15/2022
# CS 405 - HW 2
# Implementation of MiniMax Search
from datetime import datetime

import pygame
from src.constants import HEIGHT, FULL_WIDTH
from src import gameEvents


def main():
    # initialize screen
    pygame.init()
    window = pygame.display.set_mode((FULL_WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')

    # initialize state
    game = gameEvents.Game(window)
    log = open("game.log", 'a')
    log.write("CHECKERS GAME LOG: " + str(datetime.now()) + "\n")
    log.write("Player 1: \n")
    log.write(game.player1.status())
    log.write("Player 2: \n")
    log.write(game.player2.status())

    # event loop
    while 1:
        log.write("Turn: " + str(game.count) + "\n")
        log.write("Initial State: \n")
        log.write(game.board.print())
        if game.gameOver() is not None:
            print(game.gameOver())
            print(game.count)
            log.write("Winner: " + game.gameOver() + "\n")
            log.write("Turn Count: " + str(game.count) + "\n")
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
        log.write("Next State: \n")
        log.write(game.board.print())

    log.write("END OF GAME: " + str(datetime.now()) + "\n")
    log.close()


if __name__ == '__main__':
    main()
