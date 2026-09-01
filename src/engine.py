# ENGINE LOGIC

board = [0] * 128
attacks = [0] * 257
whiteToMove = True
castlingRights = {}
enPassantSquare = -1 # none available

class Piece:
    OFFBOARD = -1
    EMPTY = 0
    WP = 1
    WN = 2
    WB = 3
    WR = 4
    WQ = 5
    WK = 6
    BP = 7
    BN = 8
    BB = 9
    BR = 10
    BQ = 11
    BK = 12


def initBoard():
    global whiteToMove, castlingRights
    chessBoard = [
        Piece.WR, Piece.WN, Piece.WB, Piece.WQ, Piece.WK, Piece.WB, Piece.WN, Piece.WR,
        Piece.WP, Piece.WP, Piece.WP, Piece.WP, Piece.WP, Piece.WP, Piece.WP, Piece.WP,
        Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
        Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
        Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
        Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
        Piece.BP, Piece.BP, Piece.BP, Piece.BP, Piece.BP, Piece.BP, Piece.BP, Piece.BP,
        Piece.BR, Piece.BN, Piece.BB, Piece.BQ, Piece.BK, Piece.BB, Piece.BN, Piece.BR
    ]
    board.clear()
    for i in range(0, 64, 8): # adds buffer board
        board.extend(chessBoard[i : i + 8])
        board.extend([Piece.OFFBOARD] * 8)
    whiteToMove = True
    enPassantSquare = -1
    castlingRights = {
        "WK": True,
        "WQ": True,
        "BK": True,
        "BQ": True
    }

def loadFEN(fen):
    global board, whiteToMove, castlingRights, enPassantSquare
    parts = fen.split()
    if len(parts) != 6:
        return # invalid fen

    position, turn, castling, enPassant, halfMove, fullMove = parts

    pieceMap = {
        'P': Piece.WP,
        'N': Piece.WN,
        'B': Piece.WB,
        'R': Piece.WR,
        'Q': Piece.WQ,
        'K': Piece.WK,
        'p': Piece.BP,
        'n': Piece.BN,
        'b': Piece.BB,
        'r': Piece.BR,
        'q': Piece.BQ,
        'k': Piece.BK
    }

    board.clear()

    # fen uses 8 to 1, so must invert ranks to match
    ranks = position.split('/')
    moveStack.clear()

    if len(ranks) != 8:
        raise ValueError("Invalid FEN: expected 8 ranks")

    for rank in reversed(ranks):
        for char in rank:
            if char.isdigit():
                board.extend([Piece.EMPTY] * int(char))
            elif char in pieceMap:
                board.append(pieceMap[char])
            else:
                raise ValueError(f"Invalid FEN character: {char}")

        # buffer board
        board.extend([Piece.OFFBOARD] * 8)

    # sets side
    if turn == 'w':
        whiteToMove = True
    elif turn == 'b':
        whiteToMove = False
    else:
        raise ValueError("Invalid FEN side to move")

    # castling rights
    castlingRights = {
        "WK": "K" in castling,
        "WQ": "Q" in castling,
        "BK": "k" in castling,
        "BQ": "q" in castling
    }

    # en passant target square
    if enPassant == '-':
        enPassantSquare = -1
    else:
        enPassantSquare = algebraicToIndex(enPassant)

    return halfMove, fullMove

# formatter
def indexToAlgebraic(index):
    fileChar = chr(ord('a') + index % 16)
    rankChar = str((index // 16) + 1)
    return (fileChar + rankChar)

def algebraicToIndex(squareStr):
    file = ord(squareStr[0]) - ord('a')
    rank = int(squareStr[1]) - 1
    return rank * 16 + file

def pieceToChar(piece):
    symbols = {
        Piece.OFFBOARD: "--",
        Piece.EMPTY: "OO",
        Piece.WP: "WP",
        Piece.WN: "WN",
        Piece.WB: "WB",
        Piece.WR: "WR",
        Piece.WQ: "WQ",
        Piece.WK: "WK",
        Piece.BP: "BP",
        Piece.BN: "BN",
        Piece.BB: "BB",
        Piece.BR: "BR",
        Piece.BQ: "BQ",
        Piece.BK: "BK"
    }
    return symbols[piece]

def isSquareValid(square):
    return ((square & 0x88)) == 0

# If you subtract the index of square A from the index of square B, 1 means A is one square left of B, 16 means A is directly below B
def findDelta(fromSquare, toSquare):
    fromIndex = fromSquare
    toIndex = toSquare
    delta = (toIndex - fromIndex) + 0x80 # maximum neg jump = 9, max pos jump = 247
    return delta

# bit flags
atkKnight = 1
atkKing = 2
atkBishop = 4
atkRook = 8
atkWhitePawn = 16
atkBlackPawn = 32

# piece vectors
knightVecs = [33, 31, 18, 14, -33, -31, -18, -14]
kingVecs = [1, 15, 16, 17, -1, -15, -16, -17]
bishopVecs = [15, 17, -15, -17]
rookVecs = [1, 16, -1, -16]
whitePawnVecs = [15, 17]
blackPawnVecs = [-15, -17]

def generateAttacks():
    global attacks
    attacks = [0] * 257
    for v in knightVecs:
        attacks[v + 0x80] |= atkKnight
    for v in kingVecs:
        attacks[v + 0x80] |= atkKing
    for v in whitePawnVecs:
        attacks[v + 0x80] |= atkWhitePawn
    for v in blackPawnVecs:
        attacks[v + 0x80] |= atkBlackPawn
    for v in bishopVecs:
        for step in range(1, 8):
            attacks[(v * step) + 0x80] |= atkBishop
    for v in rookVecs:
        for step in range(1, 8):
            attacks[(v * step) + 0x80] |= atkRook
    return attacks

def getDirection(fromSquare, toSquare):
    fileStep = (toSquare % 16 > fromSquare % 16) - (toSquare % 16 < fromSquare % 16)
    rankStep = (toSquare // 16 > fromSquare // 16) - (toSquare // 16 < fromSquare // 16)
    return rankStep * 16 + fileStep

# clear path check
def rayIsClear(fromSquare, toSquare):
    vec = getDirection(fromSquare, toSquare)
    current = fromSquare + vec
    while current != toSquare:
        if board[current] != Piece.EMPTY:
            return False
        current += vec
    return True

# scans every square to look for attackers, slow
def isSquareAttacked(square, byWhite):
    for fromSquare in range(128):
        if not isSquareValid(fromSquare): continue
        piece = board[fromSquare]
        if piece == Piece.EMPTY:
            continue
        isWhitePiece = (piece <= Piece.WK)
        if isWhitePiece != byWhite: continue
        flags = attacks[findDelta(fromSquare, square)]

        if piece in [Piece.WN, Piece.BN]:
            if flags & atkKnight:
                return True
        elif piece in [Piece.WK, Piece.BK]:
            if flags & atkKing:
                return True
        if piece == Piece.WP:
            if flags & atkWhitePawn:
                return True
        if piece == Piece.BP:
            if flags & atkBlackPawn:
                return True
        elif piece in [Piece.WB, Piece.BB]:
            if flags & atkBishop and rayIsClear(fromSquare, square):
                return True
        elif piece in [Piece.WR, Piece.BR]:
            if flags & atkRook and rayIsClear(fromSquare, square):
                return True
        elif piece in [Piece.WQ, Piece.BQ]:
            if flags & (atkBishop | atkRook) and rayIsClear(fromSquare, square):
                return True
    return False

def findKingSquare(isWhite):
    target = Piece.WK if isWhite else Piece.BK
    for square in range(128):
        if isSquareValid(square) and board[square] == target:
            return square
    return -1 # no king on board, error

def isKingInCheck(isWhite):
    kingSquare = findKingSquare(isWhite)
    return isSquareAttacked(kingSquare, not isWhite)

# algebraic move as parameter
def makeMove(moveStr):
    global whiteToMove, enPassantSquare

    fromSquare = algebraicToIndex(moveStr[0:2])
    toSquare = algebraicToIndex(moveStr[2:4])
    promo = moveStr[4] if len(moveStr) == 5 else None

    movingPiece = board[fromSquare]
    caputredPiece = board[toSquare]

    isEnPassant = (movingPiece in (Piece.WP, Piece.BP) and toSquare == enPassantSquare and caputredPiece == Piece.EMPTY)
    epSquare = epCapturedPiece = None
    if isEnPassant:
        epSquare = toSquare - 16 if movingPiece == Piece.WP else toSquare + 16
        epCapturedPiece = board[epSquare]

    isCastle = movingPiece in (Piece.WK, Piece.BK) and abs(toSquare - fromSquare) == 2
    rookFrom = rookTo = None
    if isCastle:
        rookFrom, rookTo = {
            6: (7, 5), 2: (0, 3), 118: (119, 117), 114: (112, 115) # g1 to h1 or f1, c1 to a1 or d1, g8 to h8 or f8, c8 to a8 or d8
        }[toSquare]

    if promo:
        isWhite = movingPiece == Piece.WP
        promoPiece = {'q': Piece.WQ, 'r': Piece.WR, 'b': Piece.WB, 'n': Piece.WN}[promo]
        if not isWhite:
            promoPiece += 6 # shifts white piece to equivalent black piece
        placedPiece = promoPiece
    else:
        placedPiece = movingPiece

    # saves everything needed to undo
    moveStack.append({
        "fromSquare": fromSquare, "toSquare": toSquare,
        "movingPiece": movingPiece, "caputredPiece": caputredPiece,
        "isEnPassant": isEnPassant, "epSquare": epSquare, "epCapturedPiece": epCapturedPiece,
        "isCastle": isCastle, "rookFrom": rookFrom, "rookTo": rookTo,
        "prevCastlingRights": dict(castlingRights),
        "prevEnPassantSquare": enPassantSquare,
        "prevWhiteToMove": whiteToMove,
    })

    if isEnPassant:
        board[epSquare] = Piece.EMPTY
    board[toSquare] = placedPiece
    board[fromSquare] = Piece.EMPTY
    if isCastle:
        board[rookTo] = board[rookFrom]
        board[rookFrom] = Piece.EMPTY

    if movingPiece == Piece.WK:
        castlingRights["WK"] = False
        castlingRights["WQ"] = False
    elif movingPiece == Piece.BK:
        castlingRights["BK"] = False
        castlingRights["BQ"] = False
    if fromSquare == 0 or toSquare == 0:
        castlingRights["WQ"] = False
    if fromSquare == 7 or toSquare == 7:
        castlingRights["WK"] = False
    if fromSquare == 112 or toSquare == 112:
        castlingRights["BQ"] = False
    if fromSquare == 119 or toSquare == 119:
        castlingRights["BK"] = False

    # en passant for one move right and double push
    if movingPiece in (Piece.WP, Piece.BP) and abs(toSquare - fromSquare) == 32:
        enPassantSquare = (fromSquare + toSquare) // 2
    else:
        enPassantSquare = -1
 
    whiteToMove = not whiteToMove

def unmakeMove():
    global whiteToMove, enPassantSquare
 
    record = moveStack.pop()
    fromSquare, toSquare = record["fromSquare"], record["toSquare"]
 
    board[fromSquare] = record["movingPiece"] # undoes promotion, restores the pawn
    board[toSquare] = record["capturedPiece"]
 
    if record["isEnPassant"]:
        board[record["epSquare"]] = record["epCapturedPiece"]
 
    if record["isCastle"]:
        board[record["rookFrom"]] = board[record["rookTo"]]
        board[record["rookTo"]] = Piece.EMPTY
 
    castlingRights.clear()
    castlingRights.update(record["prevCastlingRights"])
    enPassantSquare = record["prevEnPassantSquare"]
    whiteToMove = record["prevWhiteToMove"]