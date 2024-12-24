from flask import Flask, jsonify, request, render_template, redirect, url_for
from reversi import Reversi

app = Flask(__name__)
game = Reversi()
is_ai_game = True  # Global flag to determine game mode


@app.route('/')
def landing_page():
    return render_template('landing.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    global is_ai_game
    game_mode = request.form['game_mode']
    if game_mode == "friend":
        is_ai_game = False
    else:
        is_ai_game = True
        game.difficulty = request.form['difficulty']
    return redirect(url_for('index'))


@app.route('/game')
def index():
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def game_state():
    return jsonify({
        "board": game.board,
        "turn": game.current_turn,
    })



@app.route('/make_move', methods=['POST'])
def make_move():
    global is_ai_game
    data = request.json
    row, col = data['row'], data['col']

    # Player makes a move
    if not game.make_move(game.current_turn, row, col):
        return jsonify({"success": False, "message": "Invalid move"})

    print(f"Player ({game.current_turn}) moved: ({row}, {col})")
    
    # If AI mode and it's AI's turn, make the AI move automatically
    if is_ai_game:
        game.current_turn = 'W'  # Switch turn to AI
        ai_move = game.best_move('W')  # Get AI's best move
        if ai_move:
            game.make_move('W', ai_move[0], ai_move[1])  # Execute AI's move
            print(f"AI moved: {ai_move}")
            game.current_turn = 'B'  # Switch back to player
        else:
            # AI has no valid moves; skip its turn
            print("AI has no valid moves. Skipping AI's turn.")
            game.current_turn = 'B'

    else:
        # Friend mode: Switch turns between players
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'

    # Check if the next player has valid moves, else skip their turn
    if not game.valid_moves(game.current_turn):
        print(f"No valid moves for {game.current_turn}. Skipping turn.")
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'

    return jsonify({"success": True, "board": game.board, "turn": game.current_turn})

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global game
    game = Reversi()  # Reset the game state
    return jsonify({"success": True, "message": "Game restarted!"})

if __name__ == '__main__':
    app.run(debug=True)
