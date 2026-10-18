import pytest

from tictactoe import game, server

EMPTY = [""] * 9


def test_a_move_against_the_computer_gets_a_reply() -> None:
    answer = server.handle_move({"board": EMPTY, "cell": 0, "mode": "computer", "level": "hard"})
    assert answer["board"][0] == "X"
    assert answer["computer_move"] is not None
    assert answer["board"][answer["computer_move"]] == "O"
    assert (answer["status"], answer["turn"]) == ("playing", "X")


def test_a_move_against_a_friend_does_not() -> None:
    answer = server.handle_move({"board": EMPTY, "cell": 4, "mode": "friend"})
    assert answer["board"] == ["", "", "", "", "X", "", "", "", ""]
    assert (answer["computer_move"], answer["turn"]) == (None, "O")


def test_a_winning_move_reports_the_line() -> None:
    cells = ["X", "X", "", "O", "O", "", "", "", ""]
    answer = server.handle_move({"board": cells, "cell": 2, "mode": "computer"})
    assert answer["status"] == "won"
    assert (answer["winner"], answer["line"]) == ("X", [0, 1, 2])
    assert (answer["turn"], answer["computer_move"]) == (None, None)


def test_the_computer_can_win() -> None:
    cells = ["O", "O", "", "X", "", "", "X", "", ""]
    answer = server.handle_move({"board": cells, "cell": 8, "mode": "computer", "level": "hard"})
    assert (answer["status"], answer["winner"], answer["computer_move"]) == ("won", "O", 2)


@pytest.mark.parametrize(
    ("request_body", "message"),
    [
        ([], "JSON object"),
        ({"cell": 0}, "board"),
        ({"board": EMPTY, "cell": 0, "mode": "online"}, "mode"),
        ({"board": EMPTY, "cell": 0, "level": "impossible"}, "level"),
        ({"board": ["X", *[""] * 8], "cell": 1, "mode": "computer"}, "you play X"),
        ({"board": EMPTY, "cell": 9}, "cell"),
    ],
)
def test_bad_requests_are_rejected(request_body: object, message: str) -> None:
    with pytest.raises(game.IllegalMoveError, match=message):
        server.handle_move(request_body)
