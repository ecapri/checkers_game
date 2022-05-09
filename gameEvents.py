# handles events of the game
import random
from math import inf

import pygame

import boardState
from player import Player, RANDOM, MINIMAX
from constants import RED, GREY, HEIGHT, SIZE, BLUE, GREEN, FULL_WIDTH, BLACK, WHITE, BACK
from pieces import CROWN

BOT = pygame.image.load("botImage.jpg")
BOT = pygame.transform.scale(BOT, (75, 75))
PER = pygame.image.load("person.jpg")
PER = pygame.transform.scale(PER, (75, 75))


class Game(object):
    def __init__(self, window, menu=True, p1=None, p2=None):
        self.window = window
        self.tournament = False
        self.player1 = p1
        self.player2 = p2
        if menu:
            self.menu()
        self.selected = None
        self.prev_selected = None
        self.prev_move = None
        self.cur_moves = {}
        self.count = 1
        self.boards_evaluated = 0

        if self.player1.color == RED:
            self.turn = self.player1
        else:
            self.turn = self.player2

        self.board = boardState.Board()
        if self.tournament:
            for i in range(3):
                self.randomMove()

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
            if self.board.master == {}:
                if self.turn.color == RED:
                    self.board.red_pieces = 0
                else:
                    self.board.white_pieces = 0
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
        self.turn = self.changePlayer(self.turn)

    def changePlayer(self, player):
        if player.equals(self.player1):
            return self.player2
        else:
            return self.player1

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
        if self.count > 100:
            return "Draw"
        else:
            return self.board.winner()

    def move_generator(self):
        self.boards_evaluated = 0
        if self.turn.gen == RANDOM:
            return self.randomMove()
        else:
            return self.search_move()

    def randomMove(self):
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

    def search_move(self):
        print("Turn depth: " + str(self.turn.depth))
        self.board = self.minimax(self.board, self.turn, self.turn.depth, True)[1]
        print(self.boards_evaluated)
        self.nextTurn()
        return self.boards_evaluated

    def minimax(self, board, player, depth, maximum):
        print("depth:" + str(depth))
        if depth == 0 or board.winner() is not None:
            return board.score(self.turn.color), board
        elif maximum:
            cur_max = float(-inf)
            best_move = None
            boards = self.get_boards(board, player.color)
            for path in boards:
                path.jump = False
                self.boards_evaluated += 1
                next_player = self.changePlayer(player)
                value = self.minimax(path, next_player, depth - 1, False)[0]
                if value > cur_max:
                    cur_max = value
                    best_move = path
            return cur_max, best_move
        else:
            cur_min = float(inf)
            best_move = None
            boards = self.get_boards(board, player.color)
            for path in boards:
                path.jump = False
                self.boards_evaluated += 1
                next_player = self.changePlayer(player)
                value = self.minimax(path, next_player, depth - 1, True)[0]
                if value < cur_min:
                    cur_min = value
                    best_move = path
            return cur_min, best_move

    def get_boards(self, board, color):
        boards = []
        valid = board.getAllMoves(color)
        print(board.state)
        print(valid)
        for (row, col), moves in valid.items():
            for move, jumped in moves.items():
                temp = board.copy()
                new_board = self.simulate_move(temp, temp.getPiece(row, col), move, jumped)
                print(new_board.state)
                boards.append(new_board)
        return boards

    def simulate_move(self, board, piece, move, jumped):
        row, col = move
        board.move(piece, row, col)
        if jumped:
            board.remove(jumped)
        return board

    def menu(self):
        begin = False
        font = 'freesansbold.ttf'

        player1_color = RED
        player1_comp = False
        player1_gen = None
        player1_depth = 0
        player2_color = GREY
        player2_comp = True
        player2_gen = RANDOM
        player2_depth = 0

        tournament = ' OFF '

        while 1:
            if begin:
                self.player1 = Player(player1_color, player1_comp, player1_gen, player1_depth)
                self.player2 = Player(player2_color, player2_comp, player2_gen, player2_depth)
                return

            self.window.fill(BACK)

            # create title
            self.drawText('CHECKERS', font, 60, WHITE, BACK, FULL_WIDTH // 2, HEIGHT // 8)

            # create start button
            self.drawText(' Start ', font, 40, RED, WHITE, FULL_WIDTH // 2, 700)

            # players
            self.drawText(' Player 1 ', font, 40, WHITE, BACK, 250, 200)
            self.drawText(' Player 2 ', font, 40, WHITE, BACK, FULL_WIDTH - 250, 200)

            # Tournament start
            self.drawText(' Tournament Style: ', font, 35, WHITE, BACK, 350, 600)
            if self.tournament:
                self.drawText(tournament, font, 35, BLACK, GREEN, 600, 600)
            else:
                self.drawText(tournament, font, 35, BLACK, RED, 600, 600)

            # options
            if player1_color == RED:
                pygame.draw.rect(self.window, RED, (125, HEIGHT / 3.3, 75, 75))
            else:
                pygame.draw.rect(self.window, GREY, (125, HEIGHT / 3.3, 75, 75))

            if player2_color == RED:
                pygame.draw.rect(self.window, RED, (625, HEIGHT / 3.3, 75, 75))
            else:
                pygame.draw.rect(self.window, GREY, (625, HEIGHT / 3.3, 75, 75))

            if player1_comp:
                self.window.blit(BOT, (300, HEIGHT / 3.3))
                self.drawText(' Move Generator ', font, 35, BLUE, BACK, 250, 375)

                # move generator options
                if player1_gen == RANDOM:
                    self.drawText(' Random ', font, 30, BLACK, BLUE, 250, 425)
                else:
                    self.drawText(' Minimax ', font, 30, BLACK, BLUE, 250, 425)
                    s = 'Depth : ' + str(player1_depth)
                    self.drawText(s, font, 35, WHITE, BACK, 250, 500)
                    pygame.draw.polygon(self.window, WHITE, [(305, 475), (315, 460), (325, 475)], 2)
                    if player1_depth > 0:
                        pygame.draw.polygon(self.window, WHITE, [(305, 520), (315, 535), (325, 520)], 2)
            else:
                self.window.blit(PER, (300, HEIGHT / 3.3))

            if player2_comp:
                self.window.blit(BOT, (800, HEIGHT / 3.3))
                self.drawText(' Move Generator ', font, 35, BLUE, BACK, 750, 375)

                # move generator options
                if player2_gen == RANDOM:
                    self.drawText(' Random ', font, 30, BLACK, BLUE, 750, 425)
                else:
                    self.drawText(' Minimax ', font, 30, BLACK, BLUE, 750, 425)
                    s = 'Depth : ' + str(player2_depth)
                    self.drawText(s, font, 35, WHITE, BACK, 750, 500)
                    pygame.draw.polygon(self.window, WHITE, [(805, 475), (815, 460), (825, 475)], 2)
                    if player2_depth > 0:
                        pygame.draw.polygon(self.window, WHITE, [(805, 520), (815, 535), (825, 520)], 2)
            else:
                self.window.blit(PER, (800, HEIGHT / 3.3))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    # check for start button
                    if 450 < x < 550 and 675 < y < 725:
                        begin = True

                    elif (120 < x < 200 and 240 < y < 320) or (620 < x < 700 and 240 < y < 320):
                        if player1_color == RED:
                            player1_color = GREY
                            player2_color = RED

                        else:
                            player1_color = RED
                            player2_color = GREY

                    # player click
                    elif 300 < x < 380 and 240 < y < 320:
                        if not player1_comp:
                            player1_comp = True
                            player1_gen = RANDOM
                        else:
                            player1_comp = False
                            player1_gen = None

                    elif 800 < x < 880 and 240 < y < 320:
                        if not player2_comp:
                            player2_comp = True
                            player2_gen = RANDOM
                        else:
                            player2_comp = False
                            player1_gen = None

                    # move generator click
                    elif 200 < x < 300 and 410 < y < 440 and player1_comp:
                        if player1_gen == RANDOM:
                            player1_gen = MINIMAX
                        else:
                            player1_gen = RANDOM

                    elif 700 < x < 800 and 410 < y < 440 and player2_comp:
                        if player2_gen == RANDOM:
                            player2_gen = MINIMAX
                        else:
                            player2_gen = RANDOM

                    # increase/decrease depth
                    elif 305 < x < 325 and 460 < y < 475 and player1_gen == MINIMAX:
                        player1_depth += 1
                    elif 305 < x < 325 and 520 < y < 535 and player1_gen == MINIMAX and player1_depth > 0:
                        player1_depth -= 1

                    elif 805 < x < 825 and 460 < y < 475 and player2_gen == MINIMAX:
                        player2_depth += 1
                    elif 805 < x < 825 and 520 < y < 535 and player2_gen == MINIMAX and player2_depth > 0:
                        player2_depth -= 1

                    # change tournament style
                    elif 575 < x < 625 and 575 < y < 625:
                        if self.tournament:
                            self.tournament = False
                            tournament = ' OFF '
                        else:
                            self.tournament = True
                            tournament = ' ON '

            pygame.display.update()

    def drawText(self, text, font, size, color, background, x, y):
        f = pygame.font.Font(font, size)
        message = f.render(text, True, color, background)
        rect = message.get_rect()
        rect.center = (x, y)
        self.window.blit(message, rect)
