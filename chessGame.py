import chess
import chess.engine


def make_move(board):
    engine = chess.engine.SimpleEngine.popen_uci(
        "./engines/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
    result = engine.play(board, chess.engine.Limit(time=0.1))
    finalMove = result.move
    engine.quit()
    return finalMove


# Initialize a board
board = chess.Board()

while not board.is_game_over():
    # Print the current board position
    print(board)

    # Check whose turn it is
    if board.turn:
        # It's the player's turn, so get the move from the user
        moveFrom = input("Enter the square of the piece you want to move: ")
        moveTo = input("Enter the square you want to move the piece to: ")
        move = moveFrom + moveTo

        if move[0] + move[1] == move[2] + move[3]:
            print("Invalid move, try again")
            continue
        # Validate the move and make it on the board
        if board.is_legal(chess.Move.from_uci(move)):
            board.push(chess.Move.from_uci(move))
        else:
            print("Invalid move, try again")
    else:
        # It's the bot's turn, so calculate the best move
        move = make_move(board)
        print("---------------")
        print(f"Bot plays {move}")
        print("---------------")
        board.push(move)

# Print the final board position
print(board)
