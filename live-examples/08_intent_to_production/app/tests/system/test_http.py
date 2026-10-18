"""The real server, started as production starts it, tested over HTTP."""

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def url() -> Iterator[str]:
    process = subprocess.Popen(
        [sys.executable, "-m", "tictactoe", "--port", "0"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert process.stdout is not None
        base = process.stdout.readline().split(" on ", 1)[1].strip().rstrip("/")
        deadline = time.monotonic() + 5
        while True:
            try:
                urllib.request.urlopen(f"{base}/health", timeout=1).close()
                break
            except OSError:
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.05)
        yield base
    finally:
        process.terminate()
        process.wait(timeout=5)


def get(url: str) -> tuple[int, str, str]:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status, response.headers["Content-Type"], response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.headers["Content-Type"], error.read().decode()


def post(url: str, body: object) -> tuple[int, dict]:
    data = json.dumps(body).encode()
    request = urllib.request.Request(url, data, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def test_health(url: str) -> None:
    assert get(f"{url}/health")[::2] == (200, "ok")


@pytest.mark.parametrize(
    ("path", "content_type"),
    [("/", "text/html"), ("/static/style.css", "text/css"), ("/static/app.js", "text/javascript")],
)
def test_page_and_assets(url: str, path: str, content_type: str) -> None:
    status, kind, _ = get(url + path)
    assert status == 200
    assert kind.startswith(content_type)


@pytest.mark.parametrize("path", ["/nope", "/static/../server.py", "/static/%2e%2e/game.py"])
def test_nothing_else_is_served(url: str, path: str) -> None:
    assert get(url + path)[0] == 404


def test_a_whole_game_against_hard_ends_without_a_win_for_x(url: str) -> None:
    board, status = [""] * 9, "playing"
    while status == "playing":
        cell = board.index("")
        code, answer = post(f"{url}/api/move", {"board": board, "cell": cell, "level": "hard"})
        assert code == 200
        board, status = answer["board"], answer["status"]
    assert answer["winner"] != "X"


def test_a_whole_game_between_friends(url: str) -> None:
    board = [""] * 9
    for cell in (0, 3, 1, 4, 2):
        code, answer = post(f"{url}/api/move", {"board": board, "cell": cell, "mode": "friend"})
        assert code == 200
        board = answer["board"]
    assert (answer["status"], answer["winner"], answer["line"]) == ("won", "X", [0, 1, 2])


def test_bad_moves_are_400s(url: str) -> None:
    code, answer = post(f"{url}/api/move", {"board": [""] * 9, "cell": 42})
    assert code == 400
    assert "cell" in answer["error"]


def test_oversized_bodies_are_refused(url: str) -> None:
    code, _ = post(f"{url}/api/move", {"padding": "x" * 5000})
    assert code == 413
