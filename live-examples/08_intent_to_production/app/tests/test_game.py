import pytest

from tictactoe import game


def board(text: str) -> list[str]:
    """A board from 9 characters, row by row: "X", "O" or "." for empty."""
    return ["" if c == "." else c for c in text.replace(" ", "")]


def test_new_board_is_empty_and_x_moves_first() -> None:
    assert game.new_board() == [""] * 9
    assert game.turn(game.new_board()) == "X"


def test_turns_alternate() -> None:
    assert game.turn(board("X.. ... ...")) == "O"
    assert game.turn(board("XO. ... ...")) == "X"


@pytest.mark.parametrize("line", game.LINES)
def test_every_line_wins(line: tuple[int, int, int]) -> None:
    cells = game.new_board()
    for i in line:
        cells[i] = "O"
    result = game.outcome(cells)
    assert (result.status, result.winner, result.line) == ("won", "O", line)


def test_full_board_without_a_line_is_a_draw() -> None:
    assert game.outcome(board("XOX XOO OXX")).status == "draw"


def test_a_win_on_the_last_move_is_a_win_not_a_draw() -> None:
    assert game.outcome(board("XOX OXO OXX")).status == "won"


def test_play_takes_the_square_for_the_player_to_move() -> None:
    before = board("X.. ... ...")
    after = game.play(before, 4)
    assert after == board("X.. .O. ...")
    assert before == board("X.. ... ..."), "play must not change its input"


@pytest.mark.parametrize("cell", [-1, 9, "4", 4.0, True, None])
def test_play_rejects_cells_that_are_not_squares(cell: object) -> None:
    with pytest.raises(game.IllegalMoveError):
        game.play(game.new_board(), cell)


def test_play_rejects_a_taken_square() -> None:
    with pytest.raises(game.IllegalMoveError, match="taken"):
        game.play(board("X.. ... ..."), 0)


def test_play_rejects_moves_after_the_game_is_over() -> None:
    with pytest.raises(game.IllegalMoveError, match="over"):
        game.play(board("XXX OO. ..."), 8)


def test_no_legal_moves_once_won() -> None:
    assert game.legal_moves(board("XXX OO. ...")) == []


@pytest.mark.parametrize(
    "bad",
    [None, "X........", [""] * 8, ["x"] + [""] * 8, board("OO. ... ..."), board("XXX ... ...")],
)
def test_validate_rejects_impossible_boards(bad: object) -> None:
    with pytest.raises(game.IllegalMoveError):
        game.validate(bad)
