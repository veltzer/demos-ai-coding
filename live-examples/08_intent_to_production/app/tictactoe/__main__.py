"""python3 -m tictactoe [--host HOST] [--port PORT]"""

import argparse

from .server import make_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="python3 -m tictactoe", description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="address to listen on")
    parser.add_argument("--port", type=int, default=8000, help="port; 0 picks a free one")
    args = parser.parse_args()
    server = make_server(args.host, args.port)
    host, port = server.server_address[:2]
    print(f"tictactoe on http://{host}:{port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
