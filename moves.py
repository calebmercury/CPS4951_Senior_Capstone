def inBounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def opponent(color):
    return "b" if color == "w" else "w"

def canCapture(piece):
    """You cannot capture the king; game ends by checkmate."""
    return piece is not None and piece.type != "K"

def getLegalMovesForSquare(board, square, color):
    piece = board.getPiece(square)
    if not piece or piece.color != color:
        return []

    pseudo = getPseudoMoves(board, square)
    legal = []

    for toSq in pseudo:
        testBoard = board.clone()
        testBoard.makeMove(square, toSq)
        if not inCheck(testBoard, color):
            legal.append(toSq)

    return legal

def inCheck(board, color):
    kingSq = board.findKing(color)
    if not kingSq:
        return False
    return isSquareAttacked(board, kingSq, opponent(color))

def hasAnyLegalMoves(board, color):
    """
    Return True if the given side has at least one legal move.
    Used for checkmate / stalemate detection.
    """
    for r in range(8):
        for c in range(8):
            piece = board.getPiece((r, c))
            if piece and piece.color == color:
                if getLegalMovesForSquare(board, (r, c), color):
                    return True
    return False

def isSquareAttacked(board, square, byColor):
    r0, c0 = square

    pawnDir = -1 if byColor == "w" else 1
    for dc in (-1, 1):
        # A pawn of color `byColor` sitting on (rr, cc) attacks (r0, c0).
        # White pawns move "up" (dir = -1) and attack one row *above* them,
        # so from the king's square we must look one row *behind* in terms of pawn movement.
        rr = r0 - pawnDir
        cc = c0 + dc
        if inBounds(rr, cc):
            p = board.getPiece((rr, cc))
            if p and p.color == byColor and p.type == "P":
                return True

    knightJumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knightJumps:
        rr, cc = r0 + dr, c0 + dc
        if inBounds(rr, cc):
            p = board.getPiece((rr, cc))
            if p and p.color == byColor and p.type == "N":
                return True

    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        rr, cc = r0 + dr, c0 + dc
        while inBounds(rr, cc):
            p = board.getPiece((rr, cc))
            if p:
                if p.color == byColor and (p.type == "B" or p.type == "Q"):
                    return True
                break
            rr += dr
            cc += dc

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        rr, cc = r0 + dr, c0 + dc
        while inBounds(rr, cc):
            p = board.getPiece((rr, cc))
            if p:
                if p.color == byColor and (p.type == "R" or p.type == "Q"):
                    return True
                break
            rr += dr
            cc += dc

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r0 + dr, c0 + dc
            if inBounds(rr, cc):
                p = board.getPiece((rr, cc))
                if p and p.color == byColor and p.type == "K":
                    return True

    return False

def getPseudoMoves(board, square):
    r, c = square
    piece = board.getPiece(square)
    if not piece:
        return []

    t = piece.type
    color = piece.color

    if t == "P":
        return pawnMoves(board, r, c, color)
    if t == "N":
        return knightMoves(board, r, c, color)
    if t == "B":
        return slideMoves(board, r, c, color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
    if t == "R":
        return slideMoves(board, r, c, color, [(-1, 0), (1, 0), (0, -1), (0, 1)])
    if t == "Q":
        return slideMoves(board, r, c, color, [(-1, -1), (-1, 1), (1, -1), (1, 1),
                                               (-1, 0), (1, 0), (0, -1), (0, 1)])
    if t == "K":
        return kingMoves(board, r, c, color)

    return []

def pawnMoves(board, r, c, color):
    moves = []
    dirr = -1 if color == "w" else 1
    startRow = 6 if color == "w" else 1

    # Forward moves
    one = (r + dirr, c)
    if inBounds(*one) and board.getPiece(one) is None:
        moves.append(one)
        two = (r + 2 * dirr, c)
        if r == startRow and inBounds(*two) and board.getPiece(two) is None:
            moves.append(two)

    # Diagonal captures (normal and en passant) — never capture the king
    for dc in (-1, 1):
        cap = (r + dirr, c + dc)
        if inBounds(*cap):
            p = board.getPiece(cap)
            # Normal capture (king is not a valid capture target)
            if p and p.color != color and canCapture(p):
                moves.append(cap)
            # En passant capture: destination square is empty but matches en passant target
            elif p is None and cap == board.enPassantTarget:
                # Check that there's an enemy pawn on the adjacent square (same row, different column)
                enemy_pawn_sq = (r, c + dc)
                enemy_pawn = board.getPiece(enemy_pawn_sq)
                if enemy_pawn and enemy_pawn.type == "P" and enemy_pawn.color != color:
                    moves.append(cap)

    return moves

def knightMoves(board, r, c, color):
    moves = []
    jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in jumps:
        rr, cc = r + dr, c + dc
        if not inBounds(rr, cc):
            continue
        p = board.getPiece((rr, cc))
        if p is None or (p.color != color and canCapture(p)):
            moves.append((rr, cc))
    return moves

def slideMoves(board, r, c, color, directions):
    moves = []
    for dr, dc in directions:
        rr, cc = r + dr, c + dc
        while inBounds(rr, cc):
            p = board.getPiece((rr, cc))
            if p is None:
                moves.append((rr, cc))
            else:
                if p.color != color and canCapture(p):
                    moves.append((rr, cc))
                break
            rr += dr
            cc += dc
    return moves

def kingMoves(board, r, c, color):
    moves = []
    # Normal king moves: one square in any direction.
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if not inBounds(rr, cc):
                continue
            p = board.getPiece((rr, cc))
            if p is None or (p.color != color and canCapture(p)):
                moves.append((rr, cc))

    # Castling moves (king-side and queen-side).
    king = board.getPiece((r, c))
    if not king or king.type != "K":
        return moves

    # King must be on its original square and must not have moved.
    start_row = 7 if color == "w" else 0
    if r == start_row and c == 4 and not king.hasMoved:
        # King cannot currently be in check.
        if not inCheck(board, color):
            enemy = opponent(color)

            # Kingside castling.
            rook_sq = (start_row, 7)
            rook = board.getPiece(rook_sq)
            if rook and rook.type == "R" and rook.color == color and not rook.hasMoved:
                path_clear = (
                    board.getPiece((start_row, 5)) is None and
                    board.getPiece((start_row, 6)) is None
                )
                if path_clear:
                    # Squares the king passes through (f-file and g-file) must not be attacked.
                    if (
                        not isSquareAttacked(board, (start_row, 5), enemy) and
                        not isSquareAttacked(board, (start_row, 6), enemy)
                    ):
                        moves.append((start_row, 6))

            # Queenside castling.
            rook_sq = (start_row, 0)
            rook = board.getPiece(rook_sq)
            if rook and rook.type == "R" and rook.color == color and not rook.hasMoved:
                path_clear = (
                    board.getPiece((start_row, 1)) is None and
                    board.getPiece((start_row, 2)) is None and
                    board.getPiece((start_row, 3)) is None
                )
                if path_clear:
                    # Squares the king passes through (d-file and c-file) must not be attacked.
                    if (
                        not isSquareAttacked(board, (start_row, 3), enemy) and
                        not isSquareAttacked(board, (start_row, 2), enemy)
                    ):
                        moves.append((start_row, 2))

    return moves
