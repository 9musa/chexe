## Identifiers
- board
- attacks
- whiteToMove - True if whites turn, False otherwise
- castlingRights - boolean dictionary that tracks castling rights: WK, WQ, BK, BQ
- enPassantSquare - index of square with a possible en passant, -1 if none
- moveStack - tracks moves so they can be made and unmade in order

- Piece - class used for better readability

## Board Representation

Chexe uses the 0x88 board representation model, which essentially creates a 16x8 array which includes the 8x8 chess board, along with another 8x8 buffer. Since the total row width is exactly 16 bits, the math becomes easier. The lower 4 bits represent the file, and the upper 4 bits represent the rank. To be on the valid, playable board, the lower 4 bits must be between 0000 and 0111. We can check this conveniently using the (targetSquare & 0x88) check, which is where this model gets it's name from.

## Functions
- initBoard - maps chessBoard, a pre set chess board, to the board array, and extends board to add the 8x8 buffer board, initialises whiteToMove, castlingRights and enPassantSquare
- loadFEN - maps a fen string to the board array
- algebraicToIndex and indexToAlgebraic - format helpers
- pieceToChar - no idea why I made this, maybe for some old print board function
- isSquareValid - quick 0x88 check
- findDelta - calculates numeric distance between two squares in the array, biased with an addition of 0x80(128) to remove negative deltas
