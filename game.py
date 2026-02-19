import pygame
from board import Board
from moves import getLegalMovesForSquare, inCheck
from stockfish_ai import StockfishAI

class Game:
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.squareSize = windowSize // 8
        self.board = Board()
        self.turnColor = "w"
        self.selectedSquare = None
        self.legalMoves = []
        self.font = pygame.font.SysFont(None, self.squareSize // 2)
        self.smallFont = pygame.font.SysFont(None, 22)
        self.ai = StockfishAI()
        self.aiColor = "b"   # AI plays black
        self.aiThinking = False


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            col = mx // self.squareSize
            row = my // self.squareSize
            if 0 <= row < 8 and 0 <= col < 8:
                self.onClickSquare((row, col))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.board.reset()
                self.turnColor = "w"
                self.selectedSquare = None
                self.legalMoves = []

    def onClickSquare(self, square):
        piece = self.board.getPiece(square)

        if self.selectedSquare is None:
            if piece and piece.color == self.turnColor:
                self.selectedSquare = square
                self.legalMoves = getLegalMovesForSquare(self.board, square, self.turnColor)
            return

        if square == self.selectedSquare:
            self.selectedSquare = None
            self.legalMoves = []
            return

        if square in self.legalMoves:
            self.board.makeMove(self.selectedSquare, square)
            self.turnColor = "b" if self.turnColor == "w" else "w"
            self.selectedSquare = None
            self.legalMoves = []
            return

        if piece and piece.color == self.turnColor:
            self.selectedSquare = square
            self.legalMoves = getLegalMovesForSquare(self.board, square, self.turnColor)
        else:
            self.selectedSquare = None
            self.legalMoves = []

    def update(self, dt):
        if self.turnColor == self.aiColor and not self.aiThinking:
            self.aiThinking = True

            fen = self.board_to_fen()
            move = self.ai.get_best_move(fen)

            if move:
                fromSq, toSq = self.algebraic_to_square(move)
                self.board.makeMove(fromSq, toSq)

                self.turnColor = "w"

            self.aiThinking = False

        pass

    def draw(self, screen):
        self.board.draw(screen, self.squareSize, self.font, self.selectedSquare, self.legalMoves)

        checkText = ""
        if inCheck(self.board, self.turnColor):
            checkText = "CHECK"

        info = f"Turn: {'White' if self.turnColor == 'w' else 'Black'}  (R to reset)  {checkText}"
        textSurf = self.smallFont.render(info, True, (240, 240, 240))
        overlay = pygame.Surface((self.windowSize, 28), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        screen.blit(textSurf, (10, 6))
    #converts piece notation to FEN so stockfish can read it
    def board_to_fen(self):
        fen = ""
        for r in range(8):
            empty = 0
            for c in range(8):
                piece = self.board.getPiece((r, c))
                if piece is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    char = piece.type
                    fen += char.upper() if piece.color == "w" else char.lower()
            if empty > 0:
                fen += str(empty)
            if r != 7:
                fen += "/"

        fen += " "
        fen += "w" if self.turnColor == "w" else "b"
        fen += " - - 0 1"
        return fen
    #converts coordinates to current board format
    def algebraic_to_square(self, move):
        # "e2e4" → ((6,4), (4,4))
        from_file = ord(move[0]) - ord('a')
        from_rank = 8 - int(move[1])
        to_file = ord(move[2]) - ord('a')
        to_rank = 8 - int(move[3])

        return (from_rank, from_file), (to_rank, to_file)

