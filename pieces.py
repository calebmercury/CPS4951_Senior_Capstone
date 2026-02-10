class Piece:
    def __init__(self, pieceType, color):
        self.type = pieceType   # "P", "R", "N", "B", "Q", "K"
        self.color = color      # "w" or "b"

    def copy(self):
        return Piece(self.type, self.color)

    def image_key(self):
        return self.color + self.type   # e.g. "wK"
