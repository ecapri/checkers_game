# board object: handles board state (pieces left, kings, etc)
import copy

import pygame
from src.constants import SIZE, RED, BLACK, GREY, ROW, COL
from src import pieces


class Board(object):
    def __init__(self):
        self.state = []
        self.red_pieces = 12
        self.white_pieces = 12
        self.red_kings = 0
        self.white_kings = 0
        self.jumps = {}
        self.master = {}
        self.jump = False
        self.prev = False
        self.initialState()

    # draws the squares for the background
    def baseBoard(self, window):
        self.state = self.state
        window.fill(BLACK)
        for row in range(ROW):
            for col in range(row % 2, ROW, 2):  # need to alternate start position for checkered pattern
                square = (row * SIZE, col * SIZE, SIZE, SIZE)
                pygame.draw.rect(window, RED, square)

    # creates start state of board with pieces
    def initialState(self):
        for row in range(ROW):
            self.state.append([])
            for col in range(COL):
                if col % 2 != row % 2:  # need to alternate
                    if row < 3:
                        self.state[row].append(pieces.Piece(RED, row, col))  # red at top
                    elif row > 4:
                        self.state[row].append(pieces.Piece(GREY, row, col))  # black/white at bottom
                    else:
                        self.state[row].append(0)
                else:
                    self.state[row].append(0)

    def draw(self, window):
        self.baseBoard(window)
        for row in range(ROW):
            for col in range(COL):
                square = self.state[row][col]
                if square == 0:
                    continue
                else:
                    square.draw(window)

    # need to update state, check kings
    def move(self, piece, row, col):
        # update  board state by swapping elements
        self.state[row][col] = piece
        self.state[piece.row][piece.col] = 0

        # set new location
        piece.move(row, col)

        # handle kings
        if not piece.king:
            if piece.color == GREY and row == 0:
                piece.makeKing()
                self.white_kings += 1
            elif piece.color == RED and row == 7:
                piece.makeKing()
                self.red_kings += 1

    def remove(self, jumped):
        for piece in jumped:
            if piece.color == RED:
                self.red_pieces -= 1
                if piece.king:
                    self.red_kings -= 1
            else:
                self.white_pieces -= 1
                if piece.king:
                    self.white_kings -= 1

            self.state[piece.row][piece.col] = 0

    def getPiece(self, row, col):
        return self.state[row][col]

    def allPieces(self, color):
        p = []
        for row in range(ROW):
            for col in range(COL):
                space = self.state[row][col]
                if space != 0 and space.color == color:
                    p.append(space)
        return p

    def getAllMoves(self, color):
        self.master = {}
        p = self.allPieces(color)
        for piece in p:
            row = piece.row
            col = piece.col
            self.master[(row, col)] = self.generateMoves(piece)
        return self.master

    def generateMoves(self, piece):
        moves = {}
        self.jumps = {}
        if not self._checkJump(piece.row, piece.col, piece.color, piece.direction, piece.king) and not self.jump:
            moves = self._checkMove(piece.row, piece.col, piece.direction, piece.king)

        if not self.prev and self.jump:
            self.master = {}
            self.prev = True

        moves.update(self.jumps)
        return moves

    def _checkJump(self, row, col, color, direction, king, jumped=[]):
        result = False
        left = col - 1
        right = col + 1
        r = row + direction

        if king:
            if self._kingJump(row, col, color, ''):
                result = True
                return result

        # check left jump
        if self.inBounds(r, left):
            cur = self.getPiece(r, left)
            if cur != 0 and cur.color != color:
                r += direction
                left -= 1
                if self.inBounds(r, left):
                    land = self.getPiece(r, left)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(r, left)] = [cur] + jumped
                        self._checkJump(r, left, color, direction, king, [cur] + jumped)

        # check right jump
        if self.inBounds(r, right):
            r = row + direction
            cur = self.getPiece(r, right)
            if cur != 0 and cur.color != color:
                r += direction
                right += 1
                if self.inBounds(r, right):
                    land = self.getPiece(r, right)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(r, right)] = [cur] + jumped
                        self._checkJump(r, right, color, direction, king, [cur] + jumped)
        return result

    def _kingJump(self, row, col, color, direction, jumped=[]):
        result = False
        up = row - 1
        down = row + 1
        left = col - 1
        right = col + 1

        # check upper left jump, make sure not to check direction came from
        if self.inBounds(up, left) and direction != 'se':
            cur = self.getPiece(up, left)
            if cur != 0 and cur.color != color:
                up -= 1
                left -= 1
                if self.inBounds(up, left):
                    land = self.getPiece(up, left)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(up, left)] = [cur] + jumped
                        self._kingJump(up, left, color, 'nw', [cur] + jumped)

        # check lower left jump
        if self.inBounds(down, left) and direction != 'ne':
            left = col - 1
            cur = self.getPiece(down, left)
            if cur != 0 and cur.color != color:
                down += 1
                left -= 1
                if self.inBounds(down, left):
                    land = self.getPiece(down, left)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(down, left)] = [cur] + jumped
                        self._kingJump(down, left, color, 'sw', [cur] + jumped)

        # check upper right jump
        if self.inBounds(up, right) and direction != 'sw':
            up = row - 1
            cur = self.getPiece(up, right)
            if cur != 0 and cur.color != color:
                up -= 1
                right += 1
                if self.inBounds(up, right):
                    land = self.getPiece(up, right)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(up, right)] = [cur] + jumped
                        self._kingJump(up, right, color, 'ne', [cur] + jumped)

        # check lower right jump
        if self.inBounds(down, right) and direction != 'nw':
            down = row + 1
            right = col + 1
            cur = self.getPiece(down, right)
            if cur != 0 and cur.color != color:
                down += 1
                right += 1
                if self.inBounds(down, right):
                    land = self.getPiece(down, right)
                    if land == 0:
                        result = True
                        self.jump = True
                        self.jumps[(down, right)] = [cur] + jumped
                        self._kingJump(down, right, color, 'se', [cur] + jumped)

        return result

    def _checkMove(self, row, col, direction, king):
        moves = {}
        r = row + direction
        left = col - 1
        right = col + 1

        if self.inBounds(r, left):
            cur = self.getPiece(r, left)
            if cur == 0:
                moves[(r, left)] = []

        if self.inBounds(r, right):
            cur = self.getPiece(r, right)
            if cur == 0:
                moves[(r, right)] = []

        if king:
            r = row - direction
            if self.inBounds(r, left):
                cur = self.getPiece(r, left)
                if cur == 0:
                    moves[(r, left)] = []
            if self.inBounds(r, right):
                cur = self.getPiece(r, right)
                if cur == 0:
                    moves[(r, right)] = []

        return moves

    def inBounds(self, row, col):
        if row > 7 or row < 0 or col > 7 or col < 0:
            return False
        return True

    def score(self, color):
        if color == RED:
            return (self.red_pieces - self.white_pieces) + (self.red_kings * 1.5 - self.white_kings * 1.5)
        else:
            return (self.white_pieces - self.red_pieces) + (self.white_kings * 1.5 - self.red_kings * 1.5)

    def winner(self):
        if self.red_pieces <= 0:
            return GREY
        elif self.white_pieces <= 0:
            return RED
        else:
            return None

    def copy(self):
        board = copy.deepcopy(self)
        for row in range(ROW):
            for col in range(COL):
                board.state[row][col] = copy.deepcopy(self.state[row][col])
        return board

    def print(self):
        string = ""
        for row in range(ROW):
            string = string + "\n"
            for col in range(COL):
                string = string + str(self.state[row][col])
        return string
