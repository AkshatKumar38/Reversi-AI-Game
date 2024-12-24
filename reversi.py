import copy
class Reversi:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3], self.board[4][4] = 'W', 'W'
        self.board[3][4], self.board[4][3] = 'B', 'B'
        self.current_turn = 'B'
        self.difficulty = 'Medium'

    def valid_moves(self, color):
        """
        Get all valid moves for the given color.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'W' if color == 'B' else 'B'
        moves = set()

        for row in range(8):
            for col in range(8):
                if self.board[row][col] == color:
                    for dy, dx in directions:
                        y, x = row + dy, col + dx
                        flipped = False
                        while 0 <= y < 8 and 0 <= x < 8 and self.board[y][x] == opponent:
                            y += dy
                            x += dx
                            flipped = True
                        if flipped and 0 <= y < 8 and 0 <= x < 8 and self.board[y][x] == ' ':
                            moves.add((y, x))
        return moves

    def make_move(self, color, row, col):
        """
        Make a move for the given color at the specified position. Return True if successful, False otherwise.
        """
        if (row, col) not in self.valid_moves(color):
            return False

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'W' if color == 'B' else 'B'
        self.board[row][col] = color

        for dy, dx in directions:
            y, x = row + dy, col + dx
            cells_to_flip = []
            while 0 <= y < 8 and 0 <= x < 8 and self.board[y][x] == opponent:
                cells_to_flip.append((y, x))
                y += dy
                x += dx
            if 0 <= y < 8 and 0 <= x < 8 and self.board[y][x] == color:
                for fy, fx in cells_to_flip:
                    self.board[fy][fx] = color
        return True

    def heuristic(self, color):
        """
        Simple heuristic: count the number of pieces of the given color.
        """
        return sum(row.count(color) for row in self.board)

    def best_move(self, color):
        """
        Find the best move for the AI using a minimax approach.
        """
        valid_moves = self.valid_moves(color)
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
            return game.heuristic(color)

        opponent = 'W' if color == 'B' else 'B'
        if maximizing:
            best_score = float('-inf')
            for move in game.valid_moves(color):
                temp_game = game.simulate_move(color, move[0], move[1])
                score = self.minimax(temp_game, depth - 1, False, opponent)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in game.valid_moves(opponent):
                temp_game = game.simulate_move(opponent, move[0], move[1])
                score = self.minimax(temp_game, depth - 1, True, color)
                best_score = min(best_score, score)
            return best_score

    def simulate_move(self, color, row, col):
        """
        Simulate a move and return a new game state.
        """
        new_game = Reversi()
        new_game.board = [row[:] for row in self.board]
        new_game.current_turn = self.current_turn
        new_game.make_move(color, row, col)
        return new_game

    def is_game_over(self):
        """
        Check if the game is over (no valid moves for either player).
        """
        return not self.valid_moves('B') and not self.valid_moves('W')

    def get_winner(self):
        """
        Determine the winner based on the number of pieces on the board.
        """
        b_count = sum(row.count('B') for row in self.board)
        w_count = sum(row.count('W') for row in self.board)
        if b_count > w_count:
            return 'B'
        elif w_count > b_count:
            return 'W'
        return 'Draw'
