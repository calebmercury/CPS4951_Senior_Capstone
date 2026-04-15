import pygame
import os
from pieces import Piece
import main



PIECE_IMAGES = {}

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.enPassantTarget = None  # Square that can be captured en passant (the square the pawn passed over)
        self.reset()

    def reset(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.enPassantTarget = None

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
        newBoard.enPassantTarget = self.enPassantTarget  # Copy en passant state
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
        
        # Handle en passant capture: if moving to the en passant target square
        # (check BEFORE clearing enPassantTarget)
        if piece and piece.type == "P" and toSq == self.enPassantTarget:
            # Remove the pawn that was passed over.
            # The captured pawn is on the same file as the destination square,
            # one rank behind the destination from the mover's perspective:
            # - If a white pawn captures en passant, it moves up the board (row decreases),
            #   and the black pawn is one row *below* the destination.
            # - If a black pawn captures en passant, it moves down the board (row increases),
            #   and the white pawn is one row *above* the destination.
            to_r, to_c = toSq
            if piece.color == "w":
                captured_pawn_sq = (to_r + 1, to_c)
            else:
                captured_pawn_sq = (to_r - 1, to_c)
            self.setPiece(captured_pawn_sq, None)
        
        # Clear en passant target at the start of each move (it only lasts one turn)
        # Save the old value first to check for double-step moves
        old_en_passant = self.enPassantTarget
        self.enPassantTarget = None
        
        self.setPiece(toSq, piece)
        self.setPiece(fromSq, None)

        if piece:
            # Mark the piece as having moved (used for castling rights).
            piece.hasMoved = True

            # Handle pawn double-step: set en passant target square
            if piece.type == "P":
                from_r, from_c = fromSq
                to_r, to_c = toSq
                # Check if this is a double-step move (pawn moves 2 squares forward)
                if abs(from_r - to_r) == 2:
                    # Set en passant target to the square the pawn passed over (between start and end)
                    self.enPassantTarget = ((from_r + to_r) // 2, to_c)
                
                # Handle pawn promotion.
                if (piece.color == "w" and to_r == 0) or (piece.color == "b" and to_r == 7):
                    piece.type = "Q"

            # Handle castling: king moves two squares horizontally from its starting file.
            if piece.type == "K":
                from_r, from_c = fromSq
                to_r, to_c = toSq
                if from_r == to_r and abs(from_c - to_c) == 2:
                    # Kingside vs queenside based on destination column.
                    if to_c > from_c:
                        # Kingside castling.
                        rook_from = (from_r, 7)
                        rook_to = (from_r, 5)
                    else:
                        # Queenside castling.
                        rook_from = (from_r, 0)
                        rook_to = (from_r, 3)

                    rook = self.getPiece(rook_from)
                    if rook and rook.type == "R" and rook.color == piece.color:
                        self.setPiece(rook_to, rook)
                        self.setPiece(rook_from, None)
                        rook.hasMoved = True

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
