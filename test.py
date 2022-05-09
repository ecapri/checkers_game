import unittest

import pygame

import gameEvents
from constants import FULL_WIDTH, HEIGHT, RED, GREY
from player import Player, MINIMAX, RANDOM
from pieces import Piece

# initialize screen
pygame.init()
window = pygame.display.set_mode((FULL_WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


class MyTestCase(unittest.TestCase):

    def test_king_movement(self):
        game = gameEvents.Game(window, False, Player(RED, True, MINIMAX, 3), Player(GREY, True, 0, RANDOM))
        # top of board
        game.turn = game.player1
        game.board.state = [[0, 0, 0, Piece(RED, 0, 3, True), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, Piece(GREY, 6, 1, False), 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        self.assertEqual(evaluated, 22, "Wrong number of evaluated boards for king.")
        left = game.board.state[1][2]
        right = game.board.state[1][4]
        if left != 0 or right != 0:
            result = True
        else:
            result = False
        self.assertEqual(result, True, "False move by king.")

        # bottom of board
        game.turn = game.player1
        game.board.state = [[0, 0, 0, Piece(GREY, 0, 3, True), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, Piece(GREY, 2, 5, True), 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, Piece(RED, 7, 4, True), 0, 0, 0]]
        evaluated = game.move_generator()
        self.assertEqual(evaluated, 62, "Wrong number of evaluated boards for king.")
        left = game.board.state[6][3]
        right = game.board.state[6][5]
        if left != 0 or right != 0:
            result = True
        else:
            result = False
        self.assertEqual(result, True, "False move by king.")

        # center of board
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(RED, 3, 3, True), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, Piece(GREY, 6, 1, False), 0, 0, 0, Piece(GREY, 6, 5, False), 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        self.assertEqual(evaluated, 84, "Wrong number of evaluated boards for king.")
        left = game.board.state[4][2]
        right = game.board.state[4][4]
        ul = game.board.state[2][2]
        ur = game.board.state[2][4]

        if left != 0 or right != 0 or ul != 0 or ur != 0:
            result = True
        else:
            result = False
        self.assertEqual(result, True, "False move by king.")

    def test_king_jumping(self):
        game = gameEvents.Game(window, False, Player(RED, True, MINIMAX, 3), Player(GREY, True, 0, RANDOM))
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, Piece(GREY, 2, 2, False), 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(RED, 3, 3, True), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        land = game.board.state[1][1]
        self.assertEqual(evaluated, 1, "Failed king jump evaluation")
        self.assertNotEqual(land, 0, "Wrong king jump")
        self.assertEqual(game.board.state[2][2], 0, "Failed to remove piece")

    def test_corner_pieces(self):
        game = gameEvents.Game(window, False, Player(RED, True, MINIMAX, 3), Player(GREY, True, 0, RANDOM))
        # top right
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, Piece(RED, 0, 7, False)],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(GREY, 3, 3, False), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        move = game.board.state[1][6]
        self.assertEqual(evaluated, 7, "Failed corner evaluation")
        self.assertNotEqual(move, 0)

        # bottom left
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(GREY, 3, 3, False), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [Piece(RED, 7, 0, True), 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        move = game.board.state[6][1]
        self.assertEqual(evaluated, 11, "Failed corner evaluation")
        self.assertNotEqual(move, 0)

    def test_multiple_jumps(self):
        game = gameEvents.Game(window, False, Player(RED, True, MINIMAX, 3), Player(GREY, True, 0, RANDOM))
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(RED, 3, 3, False), 0, 0, 0, 0],
                            [0, 0, Piece(GREY, 4, 2, False), 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, Piece(GREY, 6, 2, False), 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        move = game.board.state[7][3]
        self.assertEqual(evaluated, 3, "Failed double jump evaluation")
        self.assertNotEqual(move, 0, "Failed double jump")

    def test_king_priority(self):
        game = gameEvents.Game(window, False, Player(RED, True, MINIMAX, 3), Player(GREY, True, 0, RANDOM))
        game.turn = game.player1
        game.board.state = [[0, 0, 0, 0, 0, 0, 0, Piece(RED, 0, 7, False)],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, Piece(GREY, 3, 3, False), 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, Piece(RED, 6, 1, False), 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        evaluated = game.move_generator()
        move = game.board.state[6][1]
        self.assertEqual(evaluated, 27, "Failed king priority evaluation")
        self.assertNotEqual(move, 0, "Failed to make king priority")

    def test_correct_move_generation(self):
        game = gameEvents.Game(window, False, Player(GREY, True, MINIMAX, 3), Player(RED, True, 0, RANDOM))
        game.turn = game.player1
        game.board.state = [[0, Piece(RED, 0, 1), 0, 0, 0, 0, 0, Piece(RED, 0, 7)],
                            [Piece(RED, 1, 0), 0, Piece(RED, 1, 2), 0, 0, 0, Piece(RED, 1, 6), 0],
                            [0, Piece(RED, 2, 1), 0, 0, 0, 0, 0, 0],
                            [Piece(GREY, 3, 0), 0, 0, 0, 0, 0, Piece(RED, 3, 6), 0],
                            [0, Piece(GREY, 4, 1), 0, 0, 0, Piece(RED, 4, 5), 0, 0],
                            [Piece(RED, 5, 0), 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, Piece(GREY, 6, 5), 0, Piece(GREY, 6, 7)],
                            [Piece(GREY, 7, 0), 0, Piece(GREY, 7, 2), 0, Piece(GREY, 7, 4), 0, 0, 0]]
        evaluated = game.move_generator()
        self.assertNotEqual(game.board, None, "Failed move generation")
        self.assertEqual(evaluated, 163, "Failed move generation")


if __name__ == '__main__':
    unittest.main()
