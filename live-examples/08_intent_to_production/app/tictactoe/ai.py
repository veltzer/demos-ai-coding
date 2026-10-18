"""The computer player.

Hard plays perfectly (negamax over the whole game tree, which is small
enough to search every move), so it never loses. Easy wins when it sees a
winning move and otherwise plays at random, which a casual player can beat.
"""

import random
from functools import cache

from . import game

LEVELS = ("easy", "hard")
WIN = 10


def choose_move(board: list[str], level: str, rng: random.Random | None = None) -> int:
    """The cell the computer plays for whoever's turn it is on `board`."""
    if level not in LEVELS:
        raise game.IllegalMoveError(f"level must be one of: {', '.join(LEVELS)}")
    moves = game.legal_moves(board)
    if not moves:
        raise game.IllegalMoveError("the game is over")
    if level == "hard":
        return best_move(tuple(board))
    me = game.turn(board)
    for cell in moves:
        if game.outcome(game.play(board, cell)).winner == me:
            return cell
    return (rng or random).choice(moves)


@cache
def best_move(board: tuple[str, ...]) -> int:
    """The best cell for the player to move; the lowest cell among equals."""
    moves = game.legal_moves(list(board))
    return max(moves, key=lambda cell: (-value(tuple(game.play(list(board), cell))), -cell))


@cache
def value(board: tuple[str, ...]) -> int:
    """How good `board` is for the player to move: positive wins, 0 draws.

    A win is worth more the sooner it comes, so Hard wins quickly and loses
    (never, in practice) as late as possible.
    """
    result = game.outcome(list(board))
    if result.status == "won":
        return -(WIN - (9 - board.count(game.EMPTY)))
    if result.status == "draw":
        return 0
    return max(-value(tuple(game.play(list(board), c))) for c in game.legal_moves(list(board)))
