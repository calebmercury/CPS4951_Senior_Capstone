import pygame
from board import Board
from moves import getLegalMovesForSquare, inCheck, hasAnyLegalMoves

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
        self.gameOver = False
        self.winner = None  # "w", "b", or None
        self.stalemate = False

    def handleEvent(self, event):
        if self.gameOver:
            # Only allow reset when the game is over.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.board.reset()
                self.turnColor = "w"
                self.selectedSquare = None
                self.legalMoves = []
                self.gameOver = False
                self.winner = None
                self.stalemate = False
            return

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
                self.gameOver = False
                self.winner = None
                self.stalemate = False

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
            # After a successful move, check for checkmate / stalemate
            current = self.turnColor  # side to move
            in_check = inCheck(self.board, current)
            if not hasAnyLegalMoves(self.board, current):
                if in_check:
                    # Checkmate: the side to move has no legal moves and is in check
                    self.gameOver = True
                    self.winner = "b" if current == "w" else "w"
                    self.stalemate = False
                else:
                    # Stalemate: no legal moves but not in check
                    self.gameOver = True
                    self.winner = None
                    self.stalemate = True
            return

        if piece and piece.color == self.turnColor:
            self.selectedSquare = square
            self.legalMoves = getLegalMovesForSquare(self.board, square, self.turnColor)
        else:
            self.selectedSquare = None
            self.legalMoves = []

    def update(self, dt):
        pass

    def draw(self, screen):
        self.board.draw(screen, self.squareSize, self.font, self.selectedSquare, self.legalMoves)

        if self.gameOver:
            if self.stalemate:
                info = "Stalemate. (R to reset)"
            elif self.winner == "w":
                info = "Checkmate! White wins. (R to reset)"
            elif self.winner == "b":
                info = "Checkmate! Black wins. (R to reset)"
            else:
                info = "Game over. (R to reset)"
        else:
            checkText = ""
            if inCheck(self.board, self.turnColor):
                checkText = "CHECK"
            info = f"Turn: {'White' if self.turnColor == 'w' else 'Black'}  (R to reset)  {checkText}"
        textSurf = self.smallFont.render(info, True, (240, 240, 240))
        overlay = pygame.Surface((self.windowSize, 28), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        screen.blit(textSurf, (10, 6))
