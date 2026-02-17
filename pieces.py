class Piece:
    def __init__(self, pieceType, color, hasMoved=False):
        self.type = pieceType   # "P", "R", "N", "B", "Q", "K"
        self.color = color      # "w" or "b"
        # Track whether the piece has moved at least once (for castling rules).
        self.hasMoved = hasMoved

    def copy(self):
        # Preserve movement history when cloning the board.
        return Piece(self.type, self.color, self.hasMoved)

    def image_key(self):
        return self.color + self.type   # e.g. "wK"
