from stockfish import Stockfish

class StockfishAI:
    
    def __init__(self, path="stockfish", skill_level=5):
        self.engine = Stockfish(
            path=path,
            parameters={
                "Threads": 2,
                "Minimum Thinking Time": 30,
                "Skill Level": skill_level
            }
        )

    def get_best_move(self, fen):
        self.engine.set_fen_position(fen)
        return self.engine.get_best_move()
