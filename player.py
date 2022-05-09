# creates a player for the checkers game

import pygame
from constants import WHITE


class Player(object):
    def __init__(self, color, computer):
        self.color = color
        self.computer = computer

    def equals(self, player):
        if self.color == player.color and self.computer == player.computer:
            return True
        return False

