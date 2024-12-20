from flask import Flask, render_template, jsonify, request
from game_logic import initialize_board, is_valid_move, apply_move, get_valid_moves
from ai_logic import astar_move
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize', methods=['GET'])
def initialize():
    board = initialize_board().tolist()
    return jsonify({'board': board, 'scores': {'player': 2, 'ai': 2}})

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    board = np.array(data['board'])
    player = data['player']
    row, col = data['move']
    difficulty = data['difficulty']

    if is_valid_move(board, row, col, player):
        apply_move(board, row, col, player)
        ai_move = astar_move(board, -player, difficulty)
        if ai_move:
            apply_move(board, ai_move[0], ai_move[1], -player)
        
        # Calculate scores
        player_score = np.sum(board == 1)
        ai_score = np.sum(board == -1)

        # Check for game end
        valid_moves_player = get_valid_moves(board, player)
        valid_moves_ai = get_valid_moves(board, -player)
        game_over = not valid_moves_player and not valid_moves_ai

        result = None
        if game_over:
            if player_score > ai_score:
                result = "Player Wins!"
            elif ai_score > player_score:
                result = "AI Wins!"
            else:
                result = "It's a Draw!"

        return jsonify({
            'board': board.tolist(),
            'ai_move': ai_move,
            'scores': {'player': player_score, 'ai': ai_score},
            'game_over': game_over,
            'result': result
        })

    return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)