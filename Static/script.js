document.addEventListener("DOMContentLoaded", () => {
    const boardContainer = document.getElementById("game-board");
    const initializeButton = document.getElementById("initialize-btn");
    const difficultySelect = document.getElementById("difficulty");

    let currentBoard = [];
    let currentPlayer = 1;

    const renderBoard = (board) => {
        boardContainer.innerHTML = "";
        board.forEach((row, rowIndex) => {
            row.forEach((cell, colIndex) => {
                const cellDiv = document.createElement("div");
                cellDiv.classList.add("cell");
                if (cell === 1) cellDiv.classList.add("player-1");
                if (cell === -1) cellDiv.classList.add("player--1");
                cellDiv.dataset.row = rowIndex;
                cellDiv.dataset.col = colIndex;
                cellDiv.addEventListener("click", () => makeMove(rowIndex, colIndex));
                boardContainer.appendChild(cellDiv);
            });
        });
    };

    const initializeGame = async () => {
        const response = await fetch("/initialize");
        const data = await response.json();
        currentBoard = data.board;
        currentPlayer = 1;
        renderBoard(currentBoard);
    };

    const makeMove = async (row, col) => {
        const difficulty = difficultySelect.value;
        const response = await fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: currentBoard, player: currentPlayer, move: [row, col], difficulty }),
        });
        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else {
            currentBoard = data.board;
            renderBoard(currentBoard);
        }
    };

    initializeButton.addEventListener("click", initializeGame);

    initializeGame();
});
