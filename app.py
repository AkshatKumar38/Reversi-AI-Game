from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from game_logic import GL
from ai_logic import AIL
import copy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure you have a secret key for sessions

game = GL()
ai = AIL(game)
is_ai_game = True  # Global flag to determine game mode

def reset_game():
    global game, ai
    # Clear the session data
    session.clear()
    
    # Re-initialize the game and AI objects
    game = GL()
    ai = AIL(game)

def display_board(board_state):
    board = board_state['board']
    print("  0 1 2 3 4 5 6 7")
    print(" +----------------+")
    for i, row in enumerate(board):
        row_str = f"{i}|{' '.join(row)}|"
        print(row_str)
    print(" +----------------+")
    print(f"Current Turn: {board_state['current_turn']}")

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
    reset_game()
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def game_state():
    black_score = sum(row.count('B') for row in game.board)
    white_score = sum(row.count('W') for row in game.board)
    valid_moves = list(map(lambda move: f"{move[0]},{move[1]}", game.valid_moves(game.current_turn)))

    # Debugging: Log game status
    game_over = not game.valid_moves('B') and not game.valid_moves('W')  # Check if both players have no valid moves
    winner = 'D'

    if game_over:
        if black_score > white_score:
            winner = 'B'  # Black wins
        elif white_score > black_score:
            winner = 'W'  # White wins
        else:
            winner = 'D'  # Draw

    # Log game over status
    print(f"Game Over: {game_over}, Winner: {winner}")

    return jsonify({
        "board": game.board,
        "turn": game.current_turn,
        "blackScore": black_score,
        "whiteScore": white_score,
        "valid_moves": valid_moves,
        "gameOver": game_over,
        "winner": winner
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    global is_ai_game
    data = request.json
    row, col = data['row'], data['col']
    
    # Save current game state to session before making the move
    session['previous_game_state'] = {
    'board': copy.deepcopy(game.board),
    'current_turn': game.current_turn,
    'valid_moves_cache': {k: list(v) for k, v in game.valid_moves_cache.items()}  # Convert set to list
    }
    # display_board(session.get('previous_game_state'))
    
    # Player makes a move
    if not game.make_move(game.current_turn, row, col):
        return jsonify({"success": False, "message": "Invalid move"})
    
    # Handle AI mode
    if is_ai_game:
        game.current_turn = 'W'  # AI's turn
        ai_move = ai.best_move('W')  # Use AIL to find the best move
        if ai_move:
            game.make_move('W', ai_move[0], ai_move[1])  # AI executes move
            game.current_turn = 'B'  # Switch back to player
        else:
            # Skip AI's turn if no valid moves
            game.current_turn = 'B'
    else:
        # Player vs Player mode: Alternate turns
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'

    # Check if the next player has valid moves, else skip their turn
    if not game.valid_moves(game.current_turn):
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'
    
    # Return the updated game state
    return jsonify({
        "success": True,
        "board": game.board,
        "turn": game.current_turn
    })
    
@app.route('/game_over')
def game_over():
    # Get the game state (including winner)
    black_score = sum(row.count('B') for row in game.board)
    white_score = sum(row.count('W') for row in game.board)

    game_over = not game.valid_moves('B') and not game.valid_moves('W')
    winner = 'Game Not Completed'

    if game_over:
        if black_score > white_score:
            winner = 'B'  # Black wins
        elif white_score > black_score:
            winner = 'W'  # White wins
        else:
            winner = 'D'  # Draw
    # Pass winner and scores to the template
    return render_template('end_screen.html', winner=winner, black_score=black_score, white_score=white_score)

@app.route('/undo_move', methods=['POST'])
def undo_move():
    if 'previous_game_state' not in session:
        return jsonify({"success": False, "message": "You can only Undo Once"})

    saved_state = session['previous_game_state']
    game.board = saved_state['board']
    game.current_turn = saved_state['current_turn']
    game.valid_moves_cache = {k: set(v) for k, v in saved_state['valid_moves_cache'].items()}  # Convert list back to set

    # print("Restored State:", saved_state)
    del session['previous_game_state']
    return jsonify({"success": True, "board": game.board, "turn": game.current_turn})

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global game, ai
    session['previous_game_state'] = {
        'board': copy.deepcopy(game.board),
        'current_turn': game.current_turn,
        'valid_moves_cache': {k: list(v) for k, v in game.valid_moves_cache.items()}  # Convert sets to lists
    }
    reset_game()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True) 