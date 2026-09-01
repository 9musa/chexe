import sys
import random
import engine
import moves
 
engine.generateAttacks()
 
 
def send(message):
    print(message, flush=True) # flush required to elimate python delay
 
 
def handleUCI():
    send("id name Chexe")
    send("id author Verelous Labs")
    send("uciok")
 
 
def handleIsReady():
    send("readyok")
 
 
def handleNewGame():
    engine.initBoard()
 
 
def handleGo(command):
    # picks a random legal move, no eval algorithm yet
    legalMoves = moves.getLegalMoves()
    if not legalMoves:
        return # no legal moves (checkmate/stalemate)
    chosenMove = random.choice(legalMoves)
    send(f"bestmove {chosenMove}")
 
 
def handlePosition(command):
    parts = command.split()
 
    if len(parts) < 2:
        return
 
    # position startpos
    if parts[1] == "startpos":
        fen = (
            "rnbqkbnr/"
            "pppppppp/"
            "8/8/8/8/"
            "PPPPPPPP/"
            "RNBQKBNR "
            "w KQkq - 0 1"
        )
 
        engine.loadFEN(fen)
 
        # check whether moves were supplied
        try:
            movesIndex = parts.index("moves")
        except ValueError:
            movesIndex = -1
 
        if movesIndex != -1:
            for move in parts[movesIndex + 1:]:
                makeUCIMove(move)
 
    # position fen
    elif parts[1] == "fen":
        try:
            movesIndex = parts.index("moves")
            fenParts = parts[2:movesIndex]
        except ValueError:
            movesIndex = -1
            fenParts = parts[2:]
 
        if len(fenParts) != 6:
            return
 
        fen = " ".join(fenParts)
        engine.loadFEN(fen)
 
        if movesIndex != -1:
            for move in parts[movesIndex + 1:]:
                makeUCIMove(move)
 
 
def makeUCIMove(move):
    engine.makeMove(move)
 
 
def main():
    # game loop
    while True:
        try:
            line = input()
        except EOFError:
            break
 
        line = line.strip()
        if not line:
            continue
 
        command = line.split()[0]
 
        if command == "uci":
            handleUCI()
        elif command == "isready":
            handleIsReady()
        elif command == "ucinewgame":
            handleNewGame()
        elif command == "position":
            handlePosition(line)
        elif command == "go":
            handleGo(line)
        elif command == "stop":
            pass # no eval functions
        elif command == "quit":
            break
 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEngine terminated by user.", file=sys.stderr) # text routed to stderr channel, ignored by gui
        sys.exit(0)