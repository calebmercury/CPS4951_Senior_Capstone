import pygame
import os
from pieces import Piece



PIECE_IMAGES = {}

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.reset()

    def reset(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

        for c in range(8):
            self.grid[6][c] = Piece("P", "w")
            self.grid[1][c] = Piece("P", "b")

        order = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for c, t in enumerate(order):
            self.grid[7][c] = Piece(t, "w")
            self.grid[0][c] = Piece(t, "b")

    def clone(self):
        newBoard = Board()
        newBoard.grid = [[None for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                newBoard.grid[r][c] = None if p is None else p.copy()
        return newBoard

    def getPiece(self, square):
        r, c = square
        return self.grid[r][c]

    def setPiece(self, square, piece):
        r, c = square
        self.grid[r][c] = piece

    def makeMove(self, fromSq, toSq):
        piece = self.getPiece(fromSq)
        self.setPiece(toSq, piece)
        self.setPiece(fromSq, None)

        if piece and piece.type == "P":
            r, c = toSq
            if (piece.color == "w" and r == 0) or (piece.color == "b" and r == 7):
                piece.type = "Q"

    def findKing(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and p.type == "K":
                    return (r, c)
        return None

    def draw(self, screen, squareSize, font, selectedSquare, legalMoves):
        light = (238, 238, 210)
        dark = (118, 150, 86)

        for r in range(8):
            for c in range(8):
                isLight = (r + c) % 2 == 0
                color = light if isLight else dark
                rect = pygame.Rect(c * squareSize, r * squareSize, squareSize, squareSize)
                pygame.draw.rect(screen, color, rect)

        if selectedSquare:
            r, c = selectedSquare
            rect = pygame.Rect(c * squareSize, r * squareSize, squareSize, squareSize)
            pygame.draw.rect(screen, (220, 200, 60), rect, 4)

        for (r, c) in legalMoves:
            center = (c * squareSize + squareSize // 2, r * squareSize + squareSize // 2)
            pygame.draw.circle(screen, (30, 30, 30), center, squareSize // 7)

        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if not piece:
                    continue

                key = piece.image_key()
                image = PIECE_IMAGES.get(key)

                if image:
                    # Center the piece in the square
                    piece_size = image.get_width()
                    offset = (squareSize - piece_size) // 2
                    screen.blit(image, (c * squareSize + offset, r * squareSize + offset))


def load_piece_images(squareSize):
    pieces = ["P", "R", "N", "B", "Q", "K"]
    colors = ["w", "b"]

    # Make pieces 85% of square size for better centering
    pieceSize = int(squareSize * 0.85)

    for color in colors:
        for piece in pieces:
            key = color + piece
            path = os.path.join("pieces-basic-png", key + ".png")

            image = pygame.image.load(path).convert_alpha()
            PIECE_IMAGES[key] = pygame.transform.smoothscale(
                image, (pieceSize, pieceSize)
            )
