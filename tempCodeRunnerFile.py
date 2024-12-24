

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def game_state():
    return jsonify({"board": game.board, "turn": game.current_turn})

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row, col = data['row'], data['col']
    if game.make_move(game.current_turn, row, col):
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'
        return jsonify({"success": True, "board": game.board})
    return jsonify({"success": False, "message": "Invalid move"})

@app.route('/ai_move', methods=['GET'])
def ai_move():
    move = game.best_move(game.current_turn)
    if move:
        game.make_move(game.current_turn, move[0], move[1])
        game.current_turn = 'W' if game.current_turn == 'B' else 'B'
        return jsonify({"success": True, "move": move, "board": game.board})
    return jsonify({"success": False, "message": "No valid moves"})
