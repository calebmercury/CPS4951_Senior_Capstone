def inBounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def opponent(color):
    return "b" if color == "w" else "w"

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

def isSquareAttacked(board, square, byColor):
    r0, c0 = square

    pawnDir = -1 if byColor == "w" else 1
    for dc in (-1, 1):
        rr = r0 + pawnDir
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

    one = (r + dirr, c)
    if inBounds(*one) and board.getPiece(one) is None:
        moves.append(one)
        two = (r + 2 * dirr, c)
        if r == startRow and inBounds(*two) and board.getPiece(two) is None:
            moves.append(two)

    for dc in (-1, 1):
        cap = (r + dirr, c + dc)
        if inBounds(*cap):
            p = board.getPiece(cap)
            if p and p.color != color:
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
        if p is None or p.color != color:
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
                if p.color != color:
                    moves.append((rr, cc))
                break
            rr += dr
            cc += dc
    return moves

def kingMoves(board, r, c, color):
    moves = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if not inBounds(rr, cc):
                continue
            p = board.getPiece((rr, cc))
            if p is None or p.color != color:
                moves.append((rr, cc))
    return moves
