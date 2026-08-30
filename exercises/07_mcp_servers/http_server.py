#!/usr/bin/env python

"""HTTP MCP server exposing two arithmetic tools: add and subtract.

Run with `python server.py`; the server speaks the MCP streamable-http
transport at http://127.0.0.1:8000/mcp. Pass --debug to log every MCP
request, notification, and response.
"""

import argparse
import logging
from typing import Any

from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import MCPServer
from mcp.shared.exceptions import MCPError
from pydantic import BaseModel, ValidationError

logger = logging.getLogger("calculator")

server = MCPServer(
    name="calculator",
    instructions="Simple arithmetic: add or subtract two numbers.",
)


async def log_messages(
    ctx: ServerRequestContext[Any, Any], call_next: CallNext
) -> HandlerResult:
    """Middleware that logs every inbound message and its result or error."""
    kind = "notification" if ctx.request_id is None else f"request {ctx.request_id}"
    logger.debug("-> %s %s params=%s", kind, ctx.method, ctx.params)
    try:
        result = await call_next(ctx)
    except (MCPError, ValidationError) as exc:
        logger.debug("<- %s %s error=%r", kind, ctx.method, exc)
        raise
    dumped = (
        result.model_dump(mode="json", exclude_none=True)
        if isinstance(result, BaseModel)
        else result
    )
    logger.debug("<- %s %s result=%s", kind, ctx.method, dumped)
    return result


@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return a + b


@server.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the difference."""
    return a - b


def main() -> None:
    """Parse the command line and run the server."""
    parser = argparse.ArgumentParser(description="Calculator MCP server")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="log every MCP request and response",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    if args.debug:
        logger.setLevel(logging.DEBUG)
        server.middleware.append(log_messages)

    server.run(transport="streamable-http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
