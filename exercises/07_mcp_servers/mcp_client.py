#!/usr/bin/env python

"""MCP client that asks the calculator server to add two numbers.

Start the server first with `python mcp_server.py`, then run
`python mcp_client.py 3 4.5`. The client connects to
http://127.0.0.1:8001/mcp over the streamable-http transport, calls the
server's `add` tool with the two numbers, and prints the sum.
"""

import argparse
import asyncio
import sys

import httpx2
from mcp import Client

SERVER_URL = "http://127.0.0.1:8001/mcp"


async def add(a: float, b: float) -> str:
    """Call the server's add tool and return its text result."""
    async with Client(SERVER_URL) as client:
        result = await client.call_tool("add", {"a": a, "b": b})
    if result.is_error:
        raise RuntimeError(f"server returned an error: {result.content}")
    return "".join(
        block.text for block in result.content if block.type == "text"
    )


def main() -> None:
    """Parse the two numbers, send them to the server, print the sum."""
    parser = argparse.ArgumentParser(
        description="Add two numbers using the calculator MCP server"
    )
    parser.add_argument("a", type=float, help="first number")
    parser.add_argument("b", type=float, help="second number")
    args = parser.parse_args()

    try:
        total = asyncio.run(add(args.a, args.b))
    except* httpx2.ConnectError:
        sys.exit(
            f"cannot reach the MCP server at {SERVER_URL}; "
            "start it first with `python mcp_server.py`"
        )
    print(f"{args.a} + {args.b} = {total}")


if __name__ == "__main__":
    main()
