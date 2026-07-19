from engine import Piece, attacks, isSquareValid, findDelta # add global board back after testing

# TEST BOARD
board = [ # (A - H)
    # Rank 1
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 2
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 3
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 4
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 5
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WQ, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 6
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 7
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,

    # Rank 8
    Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY,
    Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD, Piece.OFFBOARD,
]

# formatter
def indexToAlgebraic(index):
    fileChar = chr(ord('a') + index % 16)
    rankChar = str((index // 16) + 1)
    return (fileChar + rankChar)

# eventually add caputre moves, castling, etc
def createMove(fromSquare, toSquare): # returns e2e4 format string
    return (indexToAlgebraic(fromSquare) + indexToAlgebraic(toSquare))

# add promotions and en passant
def getPawnMoves(index, moveList):
    global board
    rank = index // 16
    isFirstMove = False
    # WHITE MOVES
    if board[index] == Piece.WP:
        if rank == 1:
            isFirstMove = True
        if board[index + 16] == Piece.EMPTY:
            move = createMove(index, index + 16)
            moveList.append(move)
            if isFirstMove:
                if board[index + 32] == Piece.EMPTY:
                    move = createMove(index, index + 32)
                    moveList.append(move)
        for vec in [15, 17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.BP <= board[target] <= Piece.BK:
                    move = createMove(index, target)
                    moveList.append(move)
    # BLACK MOVES
    elif board[index] == Piece.BP:
        if rank == 6:
            isFirstMove = True
        if board[index - 16] == Piece.EMPTY:
            move = createMove(index, index - 16)
            moveList.append(move)
            if isFirstMove:
                if board[index - 32] == Piece.EMPTY:
                    move = createMove(index, index - 32)
                    moveList.append(move)
        for vec in [-15, -17]:
            target = index + vec
            if isSquareValid(target):
                if Piece.WP <= board[target] <= Piece.WK:
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

# eventually need to add checks for whiteToMove, if true generate white moves, if false generate blackmoves
def generateMoves():
    global board
    moveList = []
    for index in range(128):
        piece = board[index]
        if not isSquareValid(index) or piece == Piece.EMPTY: continue
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