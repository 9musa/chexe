# ENGINE LOGIC

board = [0] * 128
attacks = [0] * 257
whiteToMove = True
castlingRights = {}

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
    global board, whiteToMove, castlingRights
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

def generateAttacks():
    global attacks
    return attacks