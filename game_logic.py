class GL:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3], self.board[4][4] = 'W', 'W'
        self.board[3][4], self.board[4][3] = 'B', 'B'
        self.current_turn = 'B'
        self.valid_moves_cache = {'B': set(), 'W': set()}
        self.update_valid_moves()

    def update_valid_moves(self):
        """Updates valid moves for both players."""
        self.valid_moves_cache['B'] = self.valid_moves('B')
        self.valid_moves_cache['W'] = self.valid_moves('W')

    def valid_moves(self, color):
        """Get all valid moves for the given color."""
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
        """Make a move for the given color at the specified position. Return True if successful, False otherwise."""
        if (row, col) not in self.valid_moves_cache[color]:
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
        
        self.update_valid_moves()  # Update valid moves after the move
        return True

    def is_game_over(self):
        black_score = sum(row.count('B') for row in self.board)
        white_score = sum(row.count('W') for row in self.board)
        
        # Game over if no valid moves for both players or if board is full
        if black_score + white_score == 64 or (not self.valid_moves('B') and not self.valid_moves('W')):
            return True
        return False


    def get_winner(self):
        """Determine the winner."""
        b_count = sum(row.count('B') for row in self.board)
        w_count = sum(row.count('W') for row in self.board)
        if b_count > w_count:
            return 'B'
        elif w_count > b_count:
            return 'W'
        return 'Draw'
