"""The rules of tic-tac-toe.

A board is a list of 9 cells, row by row, each "X", "O" or "" (empty).
X always moves first, so whose turn it is follows from the board itself.
"""

from dataclasses import dataclass

EMPTY = ""
SIZE = 9
MARKS = ("X", "O")
LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class IllegalMoveError(ValueError):
    """A move or a board that the rules do not allow."""


@dataclass(frozen=True)
class Outcome:
    """Where a game stands: "playing", "won" or "draw"."""

    status: str
    winner: str | None = None
    line: tuple[int, int, int] | None = None


def new_board() -> list[str]:
    return [EMPTY] * SIZE


def winning_line(board: list[str]) -> tuple[str, tuple[int, int, int]] | None:
    for line in LINES:
        a, b, c = (board[i] for i in line)
        if a and a == b == c:
            return a, line
    return None


def outcome(board: list[str]) -> Outcome:
    if found := winning_line(board):
        return Outcome("won", found[0], found[1])
    if all(board):
        return Outcome("draw")
    return Outcome("playing")


def turn(board: list[str]) -> str:
    """The mark that moves next."""
    return "X" if board.count("X") == board.count("O") else "O"


def legal_moves(board: list[str]) -> list[int]:
    if outcome(board).status != "playing":
        return []
    return [i for i, cell in enumerate(board) if not cell]


def validate(board: object) -> list[str]:
    """Check a board that came from outside and return it as a clean list."""
    if not isinstance(board, list) or len(board) != SIZE:
        raise IllegalMoveError("board must be a list of 9 cells")
    if any(cell not in (*MARKS, EMPTY) for cell in board):
        raise IllegalMoveError('cells must be "X", "O" or ""')
    x, o = board.count("X"), board.count("O")
    if x - o not in (0, 1):
        raise IllegalMoveError("X moves first and the players alternate")
    return list(board)


def play(board: list[str], cell: object) -> list[str]:
    """The board after the player to move takes `cell`. Does not change `board`."""
    # bool is a subclass of int, but true is not a square
    if not isinstance(cell, int) or isinstance(cell, bool) or not 0 <= cell < SIZE:
        raise IllegalMoveError("cell must be a whole number from 0 to 8")
    if outcome(board).status != "playing":
        raise IllegalMoveError("the game is over")
    if board[cell]:
        raise IllegalMoveError("that square is taken")
    after = list(board)
    after[cell] = turn(board)
    return after
