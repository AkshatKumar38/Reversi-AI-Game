from flask import Flask, jsonify, request, render_template, redirect, url_for
from game_logic import GL
from ai_logic import AIL

app = Flask(__name__)
game = GL()
ai = AIL(game)
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

@app.route('/game_status', methods=['GET'])
def game_status():
    if game.is_game_over():
        winner = game.get_winner()
        return jsonify({"game_over": True, "winner": winner})
    return jsonify({"game_over": False})

@app.route('/game_state', methods=['GET'])
def game_state():
    black_score = sum(row.count('B') for row in game.board)
    white_score = sum(row.count('W') for row in game.board)
    valid_moves = list(map(lambda move: f"{move[0]},{move[1]}", game.valid_moves(game.current_turn)))
    return jsonify({
        "board": game.board,
        "turn": game.current_turn,
        "blackScore": black_score,
        "whiteScore": white_score,
        "valid_moves": valid_moves
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    global is_ai_game
    data = request.json
    row, col = data['row'], data['col']

    # Player makes a move
    if not game.make_move(game.current_turn, row, col):
        return jsonify({"success": False, "message": "Invalid move"})
    
    # Handle AI mode
    if is_ai_game:
        game.current_turn = 'W'  # AI's turn
        ai_move = ai.best_move('W')  # Use AIL to find the best move
        if ai_move:
            game.make_move('W', ai_move[0], ai_move[1])  # AI executes move
            print(f"AI moved: {ai_move}")
            game.current_turn = 'B'  # Switch back to player
        else:
            # Skip AI's turn if no valid moves
            print("AI has no valid moves. Skipping AI's turn.")
            game.current_turn = 'B'
    else:
        # Player vs Player mode: Alternate turns
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'

    # Check if the next player has valid moves, else skip their turn
    if not game.valid_moves(game.current_turn):
        print(f"No valid moves for {game.current_turn}. Skipping turn.")
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'

    # Return the updated game state
    return jsonify({
        "success": True,
        "board": game.board,
        "turn": game.current_turn
    })

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global game
    game = GL()  # Reset the game state
    return jsonify({"success": True, "message": "Game restarted!"})

if __name__ == '__main__':
    app.run(debug=True)
