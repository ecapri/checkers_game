# handles events of the game
import random

import pygame

import boardState
import player
from constants import RED, GREY, HEIGHT, SIZE, BLUE, GREEN, FULL_WIDTH, BLACK, WHITE
from pieces import CROWN


class Game(object):
    def __init__(self, window):
        self.window = window
        self.menu()
        self.selected = None
        self.prev_selected = None
        self.prev_move = None
        self.board = boardState.Board()
        self.cur_moves = {}
        self.board.master = {}
        self.count = 1

        if self.player1.color == RED:
            self.turn = self.player1
        else:
            self.turn = self.player2

    def update(self):
        self.board.draw(self.window)
        self.drawMoves(self.cur_moves)
        self.drawPrev()
        self.turnStatus()
        pygame.display.update()

    def reset(self):
        self.turn = RED
        self.selected = None
        self.board = boardState.Board()
        self.cur_moves = {}
        self.board.master = {}
        # self.menu()

    # select the space at row, col: if piece selected, and another select: move
    def select(self, row, col):
        if self.selected:
            if not self.validMove(row, col):  # reset if not valid move
                self.selected = None
                self.select(row, col)

        piece = self.board.getPiece(row, col)
        if piece != 0 and piece.color == self.turn.color:
            self.selected = piece
            self.board.getAllMoves(self.turn.color)
            if (row, col) in self.board.master:
                self.cur_moves = self.board.master[(row, col)]
            else:
                self.cur_moves = {}

    def validMove(self, row, col):
        piece = self.board.getPiece(row, col)
        if piece == 0 and (row, col) in self.cur_moves:
            self.prev_move = (row, col)
            self.prev_selected = (self.selected.x, self.selected.y)
            self.board.move(self.selected, row, col)
            jumped = self.cur_moves[(row, col)]
            if jumped:
                self.board.remove(jumped)
            self.nextTurn()
        else:
            return False
        return True

    def drawMoves(self, moves):
        for move in moves:
            row, col = move
            square = (col * SIZE + SIZE // 4, row * SIZE + SIZE // 4, SIZE // 2, SIZE // 2)
            pygame.draw.rect(self.window, BLUE, square)
        if self.selected != 0 and self.selected is not None:
            self.drawSelected(self.selected)

    def drawSelected(self, piece):
        radius = (SIZE - 20) // 2
        pygame.draw.circle(self.window, GREEN, (piece.x, piece.y), radius)
        if piece.king:
            self.window.blit(CROWN, (piece.x - (CROWN.get_width() // 2), piece.y - (CROWN.get_height() // 2)))

    def drawPrev(self):
        if self.prev_move is None or self.prev_selected is None:
            return
        row, col = self.prev_move
        x = col * SIZE + SIZE // 2
        y = row * SIZE + SIZE // 2
        x1, y1 = self.prev_selected
        pygame.draw.line(self.window, GREEN, (x1, y1), (x, y), 2)

    def nextTurn(self):
        self.cur_moves = {}
        self.board.master = {}
        self.count += 1
        self.selected = None
        self.board.jump = False
        self.board.prev = False
        if self.turn.equals(self.player1):
            self.turn = self.player2
        else:
            self.turn = self.player1

    def menu(self):
        begin = False
        font = 'freesansbold.ttf'

        player1_color = RED
        player1_comp = False
        p1_color = ' Red '
        p1_status = ' Person '
        player2_color = GREY
        player2_comp = True
        p2_color = ' White '
        p2_status = ' Computer '

        while 1:
            if begin:
                self.player1 = player.Player(player1_color, player1_comp)
                self.player2 = player.Player(player2_color, player2_comp)
                return

            self.window.fill(BLUE)

            # create title
            self.drawText('CHECKERS', font, 60, BLACK, BLUE, FULL_WIDTH // 2, HEIGHT // 8)

            # create start button
            self.drawText(' Start ', font, 40, RED, WHITE, FULL_WIDTH // 2, HEIGHT / 1.5)

            # players
            self.drawText('Player 1: ', font, 40, BLACK, BLUE, FULL_WIDTH // 6, HEIGHT / 3)
            self.drawText('Player 2: ', font, 40, BLACK, BLUE, FULL_WIDTH // 6, HEIGHT // 2)

            # options
            self.drawText(p1_color, font, 40, RED, GREY, FULL_WIDTH / 2.5, HEIGHT / 3)
            self.drawText(p2_color, font, 40, RED, GREY, FULL_WIDTH / 2.5, HEIGHT / 2)
            self.drawText(p1_status, font, 40, RED, GREY, FULL_WIDTH / 1.5, HEIGHT / 3)
            self.drawText(p2_status, font, 40, RED, GREY, FULL_WIDTH / 1.5, HEIGHT / 2)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    # check for start button
                    if 450 < x < 550 and 500 < y < 550:
                        begin = True

                    # change color
                    elif (350 < x < 450 and 210 < y < 310) or (350 < x < 450 and 350 < y < 450):
                        if player1_color == RED:
                            p1_color = ' White '
                            p2_color = ' Red '
                            player1_color = GREY
                            player2_color = RED

                        else:
                            p1_color = ' Red '
                            p2_color = ' White '
                            player1_color = RED
                            player2_color = GREY

                    elif 590 < x < 741 and 210 < y < 310:
                        if not player1_comp:
                            p1_status = ' Computer '
                            player1_comp = True
                        else:
                            p1_status = ' Person '
                            player1_comp = False

                    elif 590 < x < 741 and 350 < y < 450:
                        if not player2_comp:
                            p2_status = ' Computer '
                            player2_comp = True
                        else:
                            p2_status = ' Person '
                            player2_comp = False

            pygame.display.update()

    def drawText(self, text, font, size, color, background, x, y):
        f = pygame.font.Font(font, size)
        message = f.render(text, True, color, background)
        rect = message.get_rect()
        rect.center = (x, y)
        self.window.blit(message, rect)

    def turnStatus(self):
        font = 'freesansbold.ttf'
        if self.turn.color == RED:
            self.drawText(" Red's Turn!", font, 30, BLUE, BLACK, 900, 100)
        else:
            self.drawText(" White's Turn!", font, 30, BLUE, BLACK, 900, 100)

        self.drawText(' Turn: ', font, 20, BLUE, BLACK, 875, 200)
        self.drawText(str(self.count), font, 20, BLUE, BLACK, 960, 200)

        self.drawText(' Red Pieces: ', font, 20, RED, BLACK, 875, 300)
        self.drawText(str(self.board.red_pieces), font, 20, RED, BLACK, 960, 300)

        self.drawText(' Red Kings: ', font, 20, RED, BLACK, 875, 400)
        self.drawText(str(self.board.red_kings), font, 20, RED, BLACK, 960, 400)

        self.drawText(' White Pieces: ', font, 20, WHITE, BLACK, 875, 500)
        self.drawText(str(self.board.white_pieces), font, 20, WHITE, BLACK, 960, 500)

        self.drawText(' White Kings: ', font, 20, WHITE, BLACK, 875, 600)
        self.drawText(str(self.board.white_kings), font, 20, WHITE, BLACK, 960, 600)

        return

    def gameOver(self):
        if self.board.red_pieces <= 0:
            return "Grey"
        elif self.board.white_pieces <= 0:
            return "Red"
        else:
            return None

    def randomBot(self):
        self.board.getAllMoves(self.turn.color)
        available = self.board.master
        if not available:
            if self.turn.color == RED:
                self.board.red_pieces = 0
            else:
                self.board.white_pieces = 0
        while 1:
            piece = random.choice(list(available))
            moves = self.board.master[piece]
            if moves == {}:
                available.pop(piece)
                continue
            else:
                r, c = piece
                self.selected = self.board.getPiece(r, c)
                self.cur_moves = moves
                row, col = random.choice(list(moves))
                break
        self.validMove(row, col)
