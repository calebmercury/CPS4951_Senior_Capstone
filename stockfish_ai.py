from stockfish import Stockfish

class StockfishAI:
    if difficulty == "easy": 
        n = 1
    elif difficulty == "medium":
        n = 5
    elif difficulty == "hard":
        n= 10
    def __init__(self, path="stockfish"):
        self.engine = Stockfish(
            path=path,
            parameters={
                "Threads": 2,
                "Minimum Thinking Time": 30,
                "Skill Level": 10
            }
        )

    def get_best_move(self, fen):
        self.engine.set_fen_position(fen)
        return self.engine.get_best_move()
