from stockfish import Stockfish

class StockfishAI:
    def __init__(self, path="/opt/homebrew/bin/stockfish"):
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