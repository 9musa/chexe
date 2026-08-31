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
    castlingRights = {
        "WK": True,
        "WQ": True,
        "BK": True,
        "BQ": True
    }

""" def printBoard():
    for col in range(0, 64, 8):
        for row in range(0, 8):
            print(pieceToChar(board[col+row]), end=" ")
        print("") """

def pieceToChar(Piece):
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
    return symbols[Piece]

""" def squareToIndex(index):

    return index """

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
    return isSquareAttacked(kingSquare)
