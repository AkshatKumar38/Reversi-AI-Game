async function updateBoard() {
    const response = await fetch('/game_state');
    const data = await response.json();
    const board = document.getElementById('board');
    board.innerHTML = '';
    for (let y = 0; y < 8; y++) {
        const row = document.createElement('tr');
        for (let x = 0; x < 8; x++) {
            const cell = document.createElement('td');
            cell.textContent = data.board[y][x] === ' ' ? '' : data.board[y][x];
            cell.dataset.player = data.board[y][x] === ' ' ? '' : data.board[y][x];
            cell.dataset.row = y;
            cell.dataset.col = x;
            cell.onclick = () => makeMove(y, x);
            row.appendChild(cell);
        }
        board.appendChild(row);
    }
    document.getElementById('turn').textContent = `Turn: ${data.turn}`;
    document.getElementById('black-score').textContent = `Black: ${data.blackScore}`;
    document.getElementById('white-score').textContent = `White: ${data.whiteScore}`;
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
