import engine
from engine import Piece, attacks, isSquareValid, findDelta # add global board back after testing

# board pointer
board = engine.board

promotionPieces = ['q', 'r', 'b', 'n']

# formatter
def indexToAlgebraic(index):
    fileChar = chr(ord('a') + index % 16)
    rankChar = str((index // 16) + 1)
    return (fileChar + rankChar)

# eventually add special formatting for caputre moves, castling, etc
def createMove(fromSquare, toSquare): # returns e2e4 format string
    return (indexToAlgebraic(fromSquare) + indexToAlgebraic(toSquare))

# helper function for promotions
def addPawnMove(fromSquare, toSquare, moveList):
    targetRank = toSquare // 16
    base = createMove(fromSquare, toSquare)
    if targetRank == 0 or targetRank == 7:
        for p in promotionPieces:
            moveList.append(base + p)
    else: moveList.append(base)

def getPawnMoves(index, moveList):
    global board
    rank = index // 16
    isFirstMove = False
    # WHITE MOVES
    if board[index] == Piece.WP:
        if rank == 1:
            isFirstMove = True
        if board[index + 16] == Piece.EMPTY:
            addPawnMove(index, index + 16, moveList)
            if isFirstMove:
                if board[index + 32] == Piece.EMPTY:
                    move = createMove(index, index + 32)
                    moveList.append(move)
        for vec in [15, 17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.BP <= board[target] <= Piece.BK:
                    addPawnMove(index, target, moveList)
                elif target == engine.enPassantSquare:
                    move = createMove(index, target)
                    moveList.append(move)
    # BLACK MOVES
    elif board[index] == Piece.BP:
        if rank == 6:
            isFirstMove = True
        if board[index - 16] == Piece.EMPTY:
            addPawnMove(index, index - 16, moveList)
            if isFirstMove:
                if board[index - 32] == Piece.EMPTY:
                    move = createMove(index, index - 32)
                    moveList.append(move)
        for vec in [-15, -17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.WP <= board[target] <= Piece.WK:
                    addPawnMove(index, target, moveList)
                elif target == engine.enPassantSquare:
                    move = createMove(index, target)
                    moveList.append(move)

def getKnightMoves(index, moveList):
    global board
    if board[index] == Piece.WN:
        for vec in [33, 31, 18, 14, -33, -31, -18, -14]:
            target = index + vec
            if isSquareValid(target): # INVALID
                if Piece.BP <= board[target] <= Piece.BK or board[target] == Piece.EMPTY: # CAPTURES AND EMPTY
                    move = createMove(index, target)
                    moveList.append(move)
    elif board[index] == Piece.BN:
        for vec in [33, 31, 18, 14, -33, -31, -18, -14]:
            target = index + vec
            if isSquareValid(target): # INVALID
                if Piece.WP <= board[target] <= Piece.WK or board[target] == Piece.EMPTY: # CAPTURES AND EMPTY
                    move = createMove(index, target)
                    moveList.append(move)

def getKingMoves(index, moveList):
    global board
    if board[index] == Piece.WK:
        for vec in [1, 15, 16, 17, -1, -15, -16, -17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.BP <= board[target] <= Piece.BK or board[target] == Piece.EMPTY:
                    move = createMove(index, target)
                    moveList.append(move)
    elif board[index] == Piece.BK:
        for vec in [1, 15, 16, 17, -1, -15, -16, -17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.WP <= board[target] <= Piece.WK or board[target] == Piece.EMPTY:
                    move = createMove(index, target)
                    moveList.append(move)

def getBishopMoves(index, moveList):
    global board
    if board[index] == Piece.WB:
        for vec in [15, 17, -15, -17]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: # EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.BP <= board[current] <= Piece.BK: # CAPTURED
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.WP <= board[current] <= Piece.WK: # BLOCKED
                    break
    elif board[index] == Piece.BB:
        for vec in [15, 17, -15, -17]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: #EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.WP <= board[current] <= Piece.WK: # CAPTURED
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.BP <= board[current] <= Piece.BK: # BLOCKED
                    break

def getQueenMoves(index, moveList):
    global board
    if board[index] == Piece.WQ:
        for vec in [1, 15, 16, 17, -1, -15, -16, -17]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: # EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.BP <= board[current] <= Piece.BK: # CAPTURE
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.WP <= board[current] <= Piece.WK: # BLOCK
                    break
    elif board[index] == Piece.BQ:
        for vec in [1, 15, 16, 17, -1, -15, -16, -17]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: #EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.WP <= board[current] <= Piece.WK: # CAPTURE
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.BP <= board[current] <= Piece.BK: # BLOCK
                    break

def getRookMoves(index, moveList):
    global board
    if board[index] == Piece.WR:
        for vec in [1, 16, -1, -16]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: # EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.BP <= board[current] <= Piece.BK: # CAPTURES
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.WP <= board[current] <= Piece.WK: # BLOCKS
                    break
    elif board[index] == Piece.BR:
        for vec in [1, 16, -1, -16]:
            current = index + vec
            while True:
                if not isSquareValid(current): break # INVALID
                elif board[current] == Piece.EMPTY: # EMPTY
                    move = createMove(index, current)
                    moveList.append(move)
                    current += vec
                    continue
                elif Piece.WP <= board[current] <= Piece.WK: # CAPTURES
                    move = createMove(index, current)
                    moveList.append(move)
                    break
                elif Piece.BP <= board[current] <= Piece.BK: # BLOCKS
                    break

def getCastlingMoves(moveList):
    global board
    if engine.whiteToMove:
        if board[4] != Piece.WK: # e1
            return
        if engine.castlingRights.get("WK", False) and board[7] == Piece.WR: # h1
            if board[5] == Piece.EMPTY and board[6] == Piece.EMPTY: # f1, g1
                if not (engine.isSquareAttacked(4, False) or engine.isSquareAttacked(5, False) or engine.isSquareAttacked(6, False)): # e1, f1, g1
                    moveList.append("e1g1")
        if engine.castlingRights.get("WQ", False) and board[0] == Piece.WR: # a1
            if board[1] == Piece.EMPTY and board[2] == Piece.EMPTY and board[3] == Piece.EMPTY: # b1, c1, d1
                if not (engine.isSquareAttacked(2, False) or engine.isSquareAttacked(3, False) or engine.isSquareAttacked(4, False)): # c1, d1, e1
                    moveList.append("e1c1")
    else:
        if board[116] != Piece.BK: # e8
            return
        if engine.castlingRights.get("BK", False) and board[119] == Piece.BR: # h8
            if board[117] == Piece.EMPTY and board[118] == Piece.EMPTY: # f8, g8
                if not (engine.isSquareAttacked(116, True) or engine.isSquareAttacked(117, True) or engine.isSquareAttacked(118, True)): # e8, f8, g8
                    moveList.append("e8g8")
        if engine.castlingRights.get("BQ", False) and board[112] == Piece.BR: # a8
            if board[113] == Piece.EMPTY and board[114] == Piece.EMPTY and board[115] == Piece.EMPTY: # b8, c8, d8
                if not (engine.isSquareAttacked(114, True) or engine.isSquareAttacked(115, True) or engine.isSquareAttacked(116, True)): # c8, d8, e8
                    moveList.append("e8c8")

# pseudo-legals
def generateMoves():
    moveList = []
    for index in range(128):
        piece = board[index] # selected piece
        if not isSquareValid(index) or piece == Piece.EMPTY: continue
        isWhitePiece = (piece <= Piece.WK) # true if white, false if black
        if engine.whiteToMove != isWhitePiece: continue # break if not white move
        elif piece == Piece.BP or piece == Piece.WP:
            # PAWN
            getPawnMoves(index, moveList)
        elif piece == Piece.BN or piece == Piece.WN:
            # KNIGHT
            getKnightMoves(index, moveList)
        elif piece == Piece.BK or piece == Piece.WK:
            # KING
            getKingMoves(index, moveList)
        elif piece == Piece.BR or piece == Piece.WR:
            # ROOK
            getRookMoves(index, moveList)
        elif piece == Piece.BB or piece == Piece.WB:
            # BISHOP
            getBishopMoves(index, moveList)
        elif piece == Piece.BQ or piece == Piece.WQ:
            # QUEEN
            getQueenMoves(index, moveList)
    return moveList


# DEBUG
arr = generateMoves()
print(arr)
print(len(arr))