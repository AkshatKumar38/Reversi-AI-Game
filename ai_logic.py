from game_logic import GL

class AIL:
    def __init__(self, game_instance, difficulty='Medium'):
        self.game = game_instance  # GL instance for state
        self.difficulty = difficulty

    def heuristic(self, color):
        """
        Simple heuristic: count the number of pieces of the given color.
        """
        return sum(row.count(color) for row in self.game.board)

    def best_move(self, color):
        """
        Find the best move for the AI using a minimax approach.
        """
        valid_moves = self.game.valid_moves(color)
        if not valid_moves:
            return None

        best_score = float('-inf')
        best_move = None
        opponent = 'W' if color == 'B' else 'B'
        depth = {'Easy': 1, 'Medium': 3, 'Hard': 5}[self.difficulty]

        for move in valid_moves:
            temp_game = self.simulate_move(color, move[0], move[1])
            score = self.minimax(temp_game, depth - 1, False, opponent)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, game, depth, maximizing, color):
        """
        Minimax algorithm with depth limit and heuristic evaluation.
        """
        if depth == 0 or not game.valid_moves(color):
            return self.heuristic(color)

        opponent = 'W' if color == 'B' else 'B'
        if maximizing:
            best_score = float('-inf')
            for move in game.valid_moves(color):
                temp_game = self.simulate_move(color, move[0], move[1])
                score = self.minimax(temp_game, depth - 1, False, opponent)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in game.valid_moves(opponent):
                temp_game = self.simulate_move(opponent, move[0], move[1])
                score = self.minimax(temp_game, depth - 1, True, color)
                best_score = min(best_score, score)
            return best_score

    def simulate_move(self, color, row, col):
        """
        Simulate a move and return a new game state.
        """
        new_game = GL()  # Create a fresh game instance to simulate the move
        new_game.board = [r[:] for r in self.game.board]  # Make a deep copy of the board
        new_game.current_turn = color  # Set the turn to the simulated player's color
        new_game.make_move(color, row, col)  # Apply the simulated move
        return new_game
