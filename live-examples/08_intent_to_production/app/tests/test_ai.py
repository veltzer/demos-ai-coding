import random

import pytest

from tictactoe import ai, game


def every_game_against(level: str, computer: str) -> list[list[str]]:
    """Every finished game the computer plays as `computer` against every
    possible sequence of opponent moves."""
    finished, todo = [], [game.new_board()]
    while todo:
        cells = todo.pop()
        if game.outcome(cells).status != "playing":
            finished.append(cells)
        elif game.turn(cells) == computer:
            todo.append(game.play(cells, ai.choose_move(cells, level)))
        else:
            todo.extend(game.play(cells, move) for move in game.legal_moves(cells))
    return finished


@pytest.mark.parametrize("computer", game.MARKS)
def test_hard_never_loses(computer: str) -> None:
    games = every_game_against("hard", computer)
    assert len(games) > 50, "the search should cover many games"
    assert all(game.outcome(g).winner in (computer, None) for g in games)


def test_hard_takes_a_win_when_there_is_one() -> None:
    assert ai.choose_move(["O", "O", "", "X", "X", "", "X", "", ""], "hard") == 2


def test_hard_blocks() -> None:
    assert ai.choose_move(["X", "X", "", "", "O", "", "", "", ""], "hard") == 2


def test_easy_takes_a_win_when_there_is_one() -> None:
    assert ai.choose_move(["O", "O", "", "X", "X", "", "X", "", ""], "easy") == 2


def test_easy_can_be_beaten() -> None:
    games = every_game_against("easy", "O")
    assert any(game.outcome(g).winner == "X" for g in games)


def test_easy_only_plays_legal_moves() -> None:
    rng = random.Random(7)
    for _ in range(200):
        cells = game.new_board()
        while game.outcome(cells).status == "playing":
            cells = game.play(cells, ai.choose_move(cells, "easy", rng))


def test_unknown_level_is_rejected() -> None:
    with pytest.raises(game.IllegalMoveError, match="level"):
        ai.choose_move(game.new_board(), "impossible")


def test_no_move_when_the_game_is_over() -> None:
    with pytest.raises(game.IllegalMoveError, match="over"):
        ai.choose_move(["X", "X", "X", "O", "O", "", "", "", ""], "hard")
