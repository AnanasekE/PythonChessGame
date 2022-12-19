import sys

import chess.engine
import pygame


def get_square_at_pixel(pos):
    x, y = pos
    square_size = screen_size[0] // 8
    rank = y // square_size
    file = x // square_size
    return chess.square(file, rank)


# Initialize Pygame
pygame.init()

# Set the window size and title
screen_size = (640, 640)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chess")

# Set the background color to white
bg_color = (255, 255, 255)

# Load the chess board image and scale it to the window size
board_image = pygame.image.load("./assets/chessboard.png")
board_image = pygame.transform.scale(board_image, screen_size)

# Initialize the chess board and set the player as white
board = chess.Board()
player_color = chess.WHITE

# Initialize the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the chess board on the screen
    screen.blit(board_image, (0, 0))
    pygame.display.flip()

    # If it's the player's turn, get their move
    if board.turn == player_color:
        # Wait for the player to make a move
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if the player has clicked on a piece to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the square that the player clicked on
                square = get_square_at_pixel(event.pos)
                # If the player clicked on a piece, select it
                if board.piece_at(square):
                    selected_piece = square
                # If the player clicked on an empty square, try to move the selected piece to it
                elif selected_piece:
                    # Get the move that the player is trying to make
                    move = chess.Move(selected_piece, square)
                    # If the move is legal, apply it to the board and reset the selected piece
                    if move in board.legal_moves:
                        board.push(move)
                        selected_piece = None

        # Deselect the piece if the player clicked on an empty square
        selected_piece = None

    # If it's the bot's turn, get the bot's move
    else:
        # Get the best move from the Stockfish engine
        result = engine.play(board, chess.engine.Limit(time=0.1))
        # Apply the move to the board
        board.push(result.move)
