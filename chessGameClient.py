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
        image = pygame.image.load('./assets/'+filename)
        piece_images[symbol] = image
        piece_images[symbol.upper()] = image


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

while not board.is_game_over():
    # Draw the board
    draw_board(board)

    # Check whose turn it is
    if board.turn:
        # It's the player's turn, so handle the Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // 75
                row = mouse_y // 75
                index = 8 * row + col
                if selected_square is None:
                    piece = board.piece_at(index)
                    if piece and piece.color == chess.WHITE:
                        # Select the square
                        selected_square = index
                else:
                    # Make the move
                    move = chess.Move(selected_square, index)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                    else:
                        # It's the computer's turn, so use the chess engine to make a move
                        move = make_move(board)
                        board.push(move)
draw_board(board)
pygame.time.wait(3000)
pygame.quit()