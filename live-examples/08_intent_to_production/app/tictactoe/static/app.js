// The browser side: draws the board, sends each move to the server and
// shows what it answers. The rules live on the server (tictactoe/game.py).
"use strict";

const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const modeEl = document.getElementById("mode");
const levelEl = document.getElementById("level");
const levelLabel = document.getElementById("level-label");
const score = { X: 0, O: 0, draw: 0 };

let state = null; // the server's last answer
let busy = false; // a move is on its way to the server
let focused = 0; // the cell that holds the board's single tab stop

const cells = Array.from({ length: 9 }, (_, i) => {
  const cell = document.createElement("button");
  cell.type = "button";
  cell.className = "cell";
  cell.addEventListener("click", () => move(i));
  cell.addEventListener("keydown", (event) => onKey(event, i));
  cell.addEventListener("focus", () => { focused = i; });
  boardEl.appendChild(cell);
  return cell;
});

function newGame() {
  state = { board: Array(9).fill(""), status: "playing", winner: null, line: null, turn: "X" };
  levelLabel.hidden = modeEl.value !== "computer";
  render();
}

async function move(cell) {
  if (busy || state.status !== "playing" || state.board[cell]) return;
  busy = true;
  try {
    const response = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board: state.board, cell, mode: modeEl.value, level: levelEl.value }),
    });
    const answer = await response.json();
    if (!response.ok) throw new Error(answer.error || response.statusText);
    state = answer;
    if (state.status === "won") score[state.winner] += 1;
    if (state.status === "draw") score.draw += 1;
  } catch (error) {
    statusEl.textContent = `Something went wrong: ${error.message}`;
    return;
  } finally {
    busy = false;
  }
  render();
}

function render() {
  const winning = new Set(state.line || []);
  cells.forEach((cell, i) => {
    const mark = state.board[i];
    cell.textContent = mark;
    cell.className = `cell ${mark.toLowerCase()} ${winning.has(i) ? "win" : ""}`;
    // aria-disabled, not disabled: a disabled button cannot keep the focus
    cell.setAttribute("aria-disabled", String(state.status !== "playing" || Boolean(mark)));
    cell.tabIndex = i === focused ? 0 : -1;
    const row = Math.floor(i / 3) + 1;
    const col = (i % 3) + 1;
    const what = mark || "empty";
    cell.setAttribute("aria-label", `Row ${row}, column ${col}, ${what}${winning.has(i) ? ", winning" : ""}`);
  });
  statusEl.textContent = describe();
  document.getElementById("score-x").textContent = score.X;
  document.getElementById("score-o").textContent = score.O;
  document.getElementById("score-draw").textContent = score.draw;
}

function describe() {
  const vsComputer = modeEl.value === "computer";
  if (state.status === "won") {
    if (!vsComputer) return `${state.winner} wins!`;
    return state.winner === "X" ? "You win!" : "The computer wins.";
  }
  if (state.status === "draw") return "It's a draw.";
  if (vsComputer) return "Your turn (X)";
  return `${state.turn} to play`;
}

const STEPS = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -3, ArrowDown: 3 };

function onKey(event, i) {
  let next = null;
  if (event.key in STEPS) {
    const step = STEPS[event.key];
    const target = i + step;
    const sameRow = Math.floor(target / 3) === Math.floor(i / 3);
    if (target >= 0 && target < 9 && (Math.abs(step) === 3 || sameRow)) next = target;
  } else if (event.key === "Home") {
    next = 0;
  } else if (event.key === "End") {
    next = 8;
  } else {
    return; // Enter and Space click the button by themselves
  }
  event.preventDefault();
  if (next !== null) {
    focused = next;
    render();
    cells[next].focus();
  }
}

document.getElementById("new-game").addEventListener("click", newGame);
modeEl.addEventListener("change", newGame);
levelEl.addEventListener("change", newGame);
newGame();
