# creates a player for the checkers game

RANDOM = 0
MINIMAX = 1


class Player(object):
    def __init__(self, color, computer, gen, depth):
        self.color = color
        self.computer = computer
        self.gen = gen
        self.depth = depth

    def equals(self, player):
        if self.color == player.color and self.computer == player.computer:
            return True
        return False

