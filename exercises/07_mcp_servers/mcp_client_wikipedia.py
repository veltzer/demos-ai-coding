#!/usr/bin/env python

"""MCP client that asks for a search term and reads it up on Wikipedia.

Start the server first with `python mcp_server_wikipedia.py`, then run
`python mcp_client_wikipedia.py`. The client asks what to search for,
calls the server's `search` tool, lists the matching articles, asks which
one to read, fetches it with the `get_article` tool and prints it.
The search term may also be given on the command line.
"""

import argparse
import asyncio
import sys
from typing import Any

import httpx2
from mcp import Client

SERVER_URL = "http://127.0.0.1:8002/mcp"


async def call(client: Client, tool: str, arguments: dict[str, Any]) -> Any:
    """Call a tool and return its structured result, raising on a tool error."""
    result = await client.call_tool(tool, arguments)
    if result.is_error:
        message = "".join(
            block.text for block in result.content if block.type == "text"
        )
        raise RuntimeError(message)
    return result.structured_content


def choose(count: int) -> int:
    """Ask which of `count` results to read; Enter picks the first."""
    while True:
        answer = input(f"Read which article [1-{count}, Enter for 1]? ").strip()
        if not answer:
            return 0
        if answer.isdigit() and 1 <= int(answer) <= count:
            return int(answer) - 1
        print(f"please type a number from 1 to {count}")


async def lookup(query: str, limit: int, max_chars: int) -> None:
    """Search Wikipedia through the server and print the chosen article."""
    async with Client(SERVER_URL) as client:
        found = await call(client, "search", {"query": query, "limit": limit})
        hits = found["result"]
        if not hits:
            print(f"no Wikipedia articles match {query!r}")
            return
        for number, hit in enumerate(hits, 1):
            print(f"{number}. {hit['title']}\n   {hit['snippet']}")
        title = hits[choose(len(hits))]["title"]
        article = await call(client, "get_article", {"title": title})

    text = article["text"]
    if max_chars and len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + " ..."
    print(f"\n{article['title']}\n{article['url']}\n\n{text}")


def main() -> None:
    """Ask for a search term, send it to the server, print the article."""
    parser = argparse.ArgumentParser(
        description="Search and read Wikipedia using the Wikipedia MCP server"
    )
    parser.add_argument(
        "query", nargs="*", help="what to search for (asked for when omitted)"
    )
    parser.add_argument(
        "--limit", type=int, default=5, help="how many results to list"
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=2000,
        help="cut the article after this many characters (0 for all of it)",
    )
    args = parser.parse_args()

    query = " ".join(args.query) or input("Search Wikipedia for: ").strip()
    if not query:
        sys.exit("nothing to search for")

    try:
        asyncio.run(lookup(query, args.limit, args.max_chars))
    except* httpx2.ConnectError:
        sys.exit(
            f"cannot reach the MCP server at {SERVER_URL}; "
            "start it first with `python mcp_server_wikipedia.py`"
        )
    except* RuntimeError as group:
        sys.exit(f"server returned an error: {group.exceptions[0]}")


if __name__ == "__main__":
    main()
