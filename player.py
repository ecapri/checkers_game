# creates a player for the checkers game
from src.constants import RED

RANDOM = 0
MINIMAX = 1
MONTECARLO = 2


class Player(object):
    def __init__(self, color, computer, gen, depth=None, time=None):
        self.color = color
        self.computer = computer
        self.gen = gen
        self.depth = depth
        self.time = time

    def equals(self, player):
        if self.color == player.color and self.computer == player.computer:
            return True
        return False

    def status(self):
        if self.color == RED:
            string = "Color: Red \n"
        else:
            string = "Color: White \n"

        if self.computer:
            string = string + "Type: Computer \n"
        else:
            string = string + "Type: Player \n"

        if self.gen == RANDOM:
            string = string + "Move Generator: Random \n"
        elif self.gen == MINIMAX:
            string = string + "Move Generator: Minimax with depth " + str(self.depth) + "\n"
        else:
            string = string + "Move Generator: Monte Carlo Search with time of " + str(self.time) + "\n"
        return string



