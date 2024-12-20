import numpy as np

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

def initialize_board():
    board = np.zeros((8, 8), dtype=int)
    board[3][3] = board[4][4] = 1
    board[3][4] = board[4][3] = -1
    return board

def is_valid_move(board, row, col, player):
    if board[row][col] != 0:
        return False
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == -player:
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == 0:
                    break
                if board[r][c] == player:
                    return True
                r += dr
                c += dc
    return False

def get_valid_moves(board, player):
    moves = []
    for r in range(8):
        for c in range(8):
            if is_valid_move(board, r, c, player):
                moves.append((r, c))
    return moves

def apply_move(board, row, col, player):
    board[row][col] = player
    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == 0:
                break
            if board[r][c] == player:
                for pr, pc in pieces_to_flip:
                    board[pr][pc] = player
                break
            pieces_to_flip.append((r, c))
            r += dr
            c += dc

def evaluate_board(board, player):
    return np.sum(board == player) - np.sum(board == -player)