async function updateBoard() {
    const response = await fetch('/game_state');
    const data = await response.json();
    const board = document.getElementById('board');
    board.innerHTML = ''; // Clear previous grid

    for (let y = 0; y < 8; y++) {
        const row = document.createElement('tr');
        for (let x = 0; x < 8; x++) {
            const cell = document.createElement('td');
            cell.dataset.row = y;
            cell.dataset.col = x;
            
            // Add piece based on game state
            const cellValue = data.board[y][x];
            if (cellValue === 'B') {
                cell.classList.add('occupied-b');
            } else if (cellValue === 'W') {
                cell.classList.add('occupied-w');
            }

            // Add the highlight if the cell is a valid move
            if (data.valid_moves.includes(`${y},${x}`)) {
                cell.classList.add('valid-move');
            }
            // Add click event for making moves
            cell.onclick = () => makeMove(y, x);
            row.appendChild(cell);
        }
        board.appendChild(row);
    }

    // Update turn and score
    document.getElementById('turn').textContent = `Turn: ${data.turn}`;
    document.getElementById('black-score').textContent = `Black: ${data.blackScore}`;
    document.getElementById('white-score').textContent = `White: ${data.whiteScore}`;
    if (data.gameOver) {
        const winner = data.winner ? (data.winner === 'B' ? "Black" : "White") : "Draw";
        alert(`Game Over! Winner: ${winner}`);
    }
}

async function makeMove(row, col) {
    const response = await fetch('/make_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col })
    });
    const data = await response.json();
    if (data.success) {
        updateBoard();
    } else {
        alert(data.message);
    }
}

function isValidMove(row, col, board, turn) {
    const directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)];
    const opponent = turn === 'B' ? 'W' : 'B';
    if (board[row][col] !== ' ') return false;

    // Check each direction for a valid move
    for (let [dy, dx] of directions) {
        let y = row + dy, x = col + dx;
        let flipped = false;
        while (y >= 0 && y < 8 && x >= 0 && x < 8 && board[y][x] === opponent) {
            y += dy;
            x += dx;
            flipped = true;
        }
        if (flipped && y >= 0 && y < 8 && x >= 0 && x < 8 && board[y][x] === turn) {
            return true;
        }
    }
    return false;
}


async function restartGame() {
    if (confirm('Are you sure you want to restart the game?')) {
        const response = await fetch('/restart_game', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            updateBoard();
        } else {
            alert("Failed to restart the game.");
        }
    }
}

window.onload = updateBoard;
