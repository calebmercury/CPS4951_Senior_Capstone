import pygame
import threading
from board import Board
from moves import getLegalMovesForSquare, inCheck, hasAnyLegalMoves
from stockfish_ai import StockfishAI

class Game:
    def __init__(self, windowSize, skill_level=5, player_color = "w"):
        self.windowSize = windowSize
        self.squareSize = windowSize // 8
        self.board = Board()
        self.player_color = player_color
        self.turnColor = 'w'
        self.selectedSquare = None
        self.legalMoves = []
        self.font = pygame.font.SysFont(None, self.squareSize // 2)
        self.smallFont = pygame.font.SysFont(None, 22)
        self.gameOver = False
        self.winner = None  # "w", "b", or None
        self.stalemate = False
        self.ai = StockfishAI(skill_level=skill_level)
        self.aiColor = "w" if player_color == "b" else "b"  # AI plays black
        self.aiThinking = False
        self.pendingAiMove = None


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
                self.turnColor = self.aiColor
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
        if self.pendingAiMove is not None:
            fromSq, toSq = self.pendingAiMove
            self.pendingAiMove = None
            self.board.makeMove(fromSq, toSq)
            self.turnColor = self.player_color if self.turnColor == self.aiColor else self.aiColor
            self.aiThinking = False

        if self.turnColor == self.aiColor and not self.aiThinking:
            self.aiThinking = True
            fen = self.board_to_fen()

            def think():
                move = self.ai.get_best_move(fen)
                if move:
                    self.pendingAiMove = self.algebraic_to_square(move)
                else:
                    self.aiThinking = False

            threading.Thread(target=think, daemon=True).start()

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

        score_diff = self.board.scoreWhite - self.board.scoreBlack
        if score_diff > 0:
            score_str = f"White +{score_diff}"
        elif score_diff < 0:
            score_str = f"Black +{-score_diff}"
        else:
            score_str = "Equal"
        score_info = f"White: {self.board.scoreWhite}  Black: {self.board.scoreBlack}  ({score_str})"

        overlay = pygame.Surface((self.windowSize, 28), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        textSurf = self.smallFont.render(info, True, (240, 240, 240))
        screen.blit(textSurf, (10, 6))

        scoreSurf = self.smallFont.render(score_info, True, (240, 240, 240))
        score_x = self.windowSize - scoreSurf.get_width() - 10
        screen.blit(scoreSurf, (score_x, 6))
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
