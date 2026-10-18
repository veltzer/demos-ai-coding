"""HTTP server: the page, its assets, and the JSON move API.

The server keeps no state between requests. The browser sends the whole
board with every move, the server checks it, plays the move (and the
computer's reply) and sends back the new board and where the game stands.
"""

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import ai, game

STATIC = Path(__file__).parent / "static"
# Only these files are served: a fixed map, so no path from a request ever
# reaches the file system.
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/static/style.css": ("style.css", "text/css; charset=utf-8"),
    "/static/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
MODES = ("computer", "friend")
MAX_BODY = 1024


def handle_move(request: object) -> dict:
    """Answer one POST /api/move body. Raises IllegalMoveError on bad input."""
    if not isinstance(request, dict):
        raise game.IllegalMoveError("the body must be a JSON object")
    board = game.validate(request.get("board"))
    mode = request.get("mode", "computer")
    if mode not in MODES:
        raise game.IllegalMoveError(f"mode must be one of: {', '.join(MODES)}")
    level = request.get("level", "hard")
    if mode == "computer":
        if level not in ai.LEVELS:
            raise game.IllegalMoveError(f"level must be one of: {', '.join(ai.LEVELS)}")
        if game.turn(board) != "X":
            raise game.IllegalMoveError("against the computer you play X")
    board = game.play(board, request.get("cell"))
    computer_move = None
    if mode == "computer" and game.outcome(board).status == "playing":
        computer_move = ai.choose_move(board, level)
        board = game.play(board, computer_move)
    return describe(board) | {"computer_move": computer_move}


def describe(board: list[str]) -> dict:
    result = game.outcome(board)
    return {
        "board": board,
        "status": result.status,
        "winner": result.winner,
        "line": list(result.line) if result.line else None,
        "turn": game.turn(board) if result.status == "playing" else None,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "tictactoe"

    def do_GET(self) -> None:
        self.serve(head=False)

    def do_HEAD(self) -> None:
        self.serve(head=True)

    def do_POST(self) -> None:
        if self.path != "/api/move":
            self.reply_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        length = self.headers.get("Content-Length", "")
        if not length.isdigit():
            self.reply_json(HTTPStatus.LENGTH_REQUIRED, {"error": "Content-Length required"})
            return
        if int(length) > MAX_BODY:
            self.reply_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "body too large"})
            return
        try:
            request = json.loads(self.rfile.read(int(length)) or b"null")
            self.reply_json(HTTPStatus.OK, handle_move(request))
        except (ValueError, game.IllegalMoveError) as error:
            # json.JSONDecodeError and IllegalMoveError are both ValueErrors
            self.reply_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})

    def serve(self, *, head: bool) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self.reply(HTTPStatus.OK, b"ok", "text/plain; charset=utf-8", head=head)
        elif path in ASSETS:
            name, content_type = ASSETS[path]
            self.reply(HTTPStatus.OK, (STATIC / name).read_bytes(), content_type, head=head)
        elif path == "/api/move":
            self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
            self.send_header("Allow", "POST")
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.reply(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8", head=head)

    def reply_json(self, status: HTTPStatus, body: dict) -> None:
        self.reply(status, json.dumps(body).encode(), "application/json")

    def reply(
        self, status: HTTPStatus, body: bytes, content_type: str, *, head: bool = False
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head:
            self.wfile.write(body)


def make_server(host: str, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)
