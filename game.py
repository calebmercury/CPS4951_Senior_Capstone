import pygame
from board import Board
from moves import getLegalMovesForSquare, inCheck

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
