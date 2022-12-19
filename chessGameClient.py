import sys

import chess
import chess.engine
import pygame

# Initialize Pygame
pygame.init()

# Set up the Pygame window
window_size = (600, 600)
window = pygame.display.set_mode(window_size)

# Load the images for the chess pieces
piece_images = {}
for color in ("black", "white"):
    for symbol in ("p", "n", "b", "r", "q", "k"):
        filename = f"{color}_{symbol}.png"
        image = pygame.image.load('./assets/' + filename)
        piece_images[symbol] = image
        if color == "black":
            piece_images[symbol.upper()] = image

print("Welcome to Chess!")
print('piece_images', piece_images)


# Define a function to draw the board and pieces on the Pygame window
def draw_board(board):
    # Clear the window
    window.fill((255, 255, 255))

    # Draw the squares
    for i in range(8):
        for j in range(8):
            x = i * 75
            y = j * 75
            color = (240, 240, 240) if (i + j) % 2 == 0 else (80, 80, 80)
            pygame.draw.rect(window, color, (x, y, 75, 75))

    # Draw the pieces
    for i in range(8):
        for j in range(8):
            x = i * 75
            y = j * 75
            symbol = board.piece_at(8 * j + i)
            if symbol:
                image = piece_images[symbol.symbol()]
                window.blit(image, (x, y))

    # Update the window
    pygame.display.update()


def make_move(board):
    engine = chess.engine.SimpleEngine.popen_uci(
        "./engines/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
    result = engine.play(board, chess.engine.Limit(time=0.1))
    finalMove = result.move
    engine.quit()
    return finalMove


# Initialize a board
board = chess.Board()

# Initialize variables for tracking the player's move
selected_square = None

dict1 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

while not board.is_game_over():
    # Draw the board
    draw_board(board)

    # Check whose turn it is
    if board.turn:
        # It's the player's turn, so get the move from the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the player clicked on a piece
                x, y = event.pos
                column = x // 75
                row = y // 75
                square = column + 8 * row
                piece = board.piece_at(square)
                # print(square)
                if piece and piece.color == chess.BLACK:
                    selected_square = square
                    print(f'Player selects {dict1[column + 1]}{row + 1}')
                else:
                    selected_square = None
                    print('Player selects empty square')
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if the player released the mouse button on a valid destination square
                x, y = event.pos
                column = x // 75
                row = y // 75
                square = column + 8 * row
                if selected_square is not None and square != selected_square:
                    print(f'Player selects {dict1[column + 1]}{row + 1}')
                    move = chess.Move(selected_square, square)
                    if board.is_legal(chess.Move.from_uci(str(move))):  # move is not legal most of the time
                        board.push(move)
                        selected_square = None
                        print(f'Player plays {move}')
                    else:
                        print('Move is illegal')



    else:

        # It's the bot's turn, so get the move from the bot

        # finalMove = make_move(board)
        #
        # print(f'Bot plays {finalMove}')
        #
        # board.push(finalMove)
        print('Bot plays')
        board.push(chess.Move.from_uci(input('Enter move: ')))

# Print the final board position
print(board)
