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

        HUD_H     = 42
        GOLD      = (210, 175, 90)
        OFF_WHITE = (232, 232, 222)
        MUTED     = (130, 130, 138)
        RED       = (210, 65, 65)

        overlay = pygame.Surface((self.windowSize, HUD_H), pygame.SRCALPHA)
        overlay.fill((10, 10, 14, 220))
        screen.blit(overlay, (0, 0))

        # Thin gold bottom border on the HUD
        pygame.draw.line(screen, (60, 50, 15),
                         (0, HUD_H - 1), (self.windowSize, HUD_H - 1))

        hud_font  = pygame.font.SysFont("Arial", 16, bold=True)
        hud_small = pygame.font.SysFont("Arial", 14)

        cy = HUD_H // 2  # vertical center of HUD

        # ── Left: turn indicator ──────────────────────────────────────
        dot_fill   = (235, 232, 220) if self.turnColor == "w" else (30, 30, 36)
        dot_border = (180, 150, 60)  if self.turnColor == "w" else (100, 100, 115)
        pygame.draw.circle(screen, dot_fill,   (18, cy), 9)
        pygame.draw.circle(screen, dot_border, (18, cy), 9, 1)

        turn_label = "White's Turn" if self.turnColor == "w" else "Black's Turn"
        turn_surf  = hud_font.render(turn_label, True, OFF_WHITE)
        screen.blit(turn_surf, (34, cy - turn_surf.get_height() // 2))

        # ── Center: status ────────────────────────────────────────────
        if self.gameOver:
            if self.stalemate:
                center_text  = "STALEMATE  —  R to reset"
                center_color = MUTED
            else:
                winner = "WHITE" if self.winner == "w" else "BLACK"
                center_text  = f"CHECKMATE  —  {winner} WINS  —  R to reset"
                center_color = GOLD
        elif self.aiThinking:
            center_text  = "AI THINKING..."
            center_color = MUTED
        elif inCheck(self.board, self.turnColor):
            center_text  = "CHECK"
            center_color = RED
        else:
            center_text  = ""
            center_color = OFF_WHITE

        if center_text:
            c_surf = hud_font.render(center_text, True, center_color)
            screen.blit(c_surf, (self.windowSize // 2 - c_surf.get_width() // 2,
                                  cy - c_surf.get_height() // 2))

        # ── Right: material score ─────────────────────────────────────
        score_diff = self.board.scoreWhite - self.board.scoreBlack
        if score_diff > 0:
            adv_text  = f"White  +{score_diff}"
            adv_color = (215, 210, 190)
        elif score_diff < 0:
            adv_text  = f"Black  +{-score_diff}"
            adv_color = (155, 150, 165)
        else:
            adv_text  = "Equal"
            adv_color = MUTED

        adv_surf = hud_font.render(adv_text, True, adv_color)
        screen.blit(adv_surf, (self.windowSize - adv_surf.get_width() - 14,
                                cy - adv_surf.get_height() // 2))
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
