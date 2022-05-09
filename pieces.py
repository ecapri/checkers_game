# creates checkers piece; tracks color and position

import pygame
from constants import SIZE, RED, WHITE

CROWN = pygame.image.load("crownImage.png")
CROWN = pygame.transform.scale(CROWN, (75, 75))


class Piece(object):
    def __init__(self, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.x = 0
        self.y = 0
        self.king = False

        if self.color == RED:
            self.direction = 1
        else:
            self.direction = -1

        self.setPosition()

    def equals(self, pos):
        row, col = pos
        if self.col == col and self.row == row:
            return True
        return False

    # used in order to draw pieces
    def setPosition(self):
        self.x = self.col * SIZE + SIZE // 2
        self.y = self.row * SIZE + SIZE // 2

    def makeKing(self):
        self.king = True

    def draw(self, window):
        radius = (SIZE - 20) // 2
        pygame.draw.circle(window, WHITE, (self.x, self.y), radius + 2)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        if self.king:
            window.blit(CROWN, (self.x - (CROWN.get_width() // 2), self.y - (CROWN.get_height() // 2)))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.setPosition()

    def __repr__(self):
        if self.color == RED:
            return "r"
        else:
            return "b"
