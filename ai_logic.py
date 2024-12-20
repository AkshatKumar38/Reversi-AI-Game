import copy
import numpy as np
from game_logic import get_valid_moves, apply_move, evaluate_board

def astar_move(board, player, difficulty):
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return None

    def heuristic(board):
        return evaluate_board(board, player)

    best_move = None
    best_score = -float('inf')
    
    for move in valid_moves:
        temp_board = copy.deepcopy(board)
        apply_move(temp_board, move[0], move[1], player)
        score = heuristic(temp_board)
        if difficulty == 'medium':
            score += np.random.uniform(-5, 5)
        elif difficulty == 'easy':
            score += np.random.uniform(-10, 10)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move