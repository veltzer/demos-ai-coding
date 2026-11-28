#!/usr/bin/env python

"""HTTP MCP server that searches Wikipedia and retrieves its articles.

Run with `python mcp_server_wikipedia.py`; the server speaks the MCP
streamable-http transport at http://127.0.0.1:8002/mcp and exposes two
tools:

- search(query, limit): the titles and snippets of matching articles
- get_article(title): the plain-text body of one article

Both call the public MediaWiki Action API of English Wikipedia, which
needs no key. Pass --debug to log every outgoing Wikipedia request.
"""

import argparse
import html
import logging
import re

import httpx2
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel

logger = logging.getLogger("wikipedia")

API_URL = "https://en.wikipedia.org/w/api.php"
# Wikimedia's robot policy (https://w.wiki/4wJS) answers 403 unless the
# User-Agent names the client and carries a URL or contact address.
USER_AGENT = (
    "WikipediaMCPDemo/0.1 (https://modelcontextprotocol.io; MCP teaching example)"
)
TAG_RE = re.compile(r"<[^>]+>")

server = MCPServer(
    name="wikipedia",
    instructions=(
        "Search English Wikipedia with `search`, then read a result "
        "with `get_article`, passing the title exactly as returned."
    ),
)


class SearchHit(BaseModel):
    """One search result: the article title and a short plain-text snippet."""

    title: str
    snippet: str


class Article(BaseModel):
    """A retrieved article: its canonical title, URL and plain-text body."""

    title: str
    url: str
    text: str


async def query_api(params: dict[str, str]) -> dict[str, object]:
    """Send one query to the MediaWiki Action API and return the JSON body."""
    full = {"action": "query", "format": "json", "formatversion": "2", **params}
    logger.debug("GET %s %s", API_URL, full)
    async with httpx2.AsyncClient(
        headers={"User-Agent": USER_AGENT}, timeout=20
    ) as client:
        response = await client.get(API_URL, params=full)
    response.raise_for_status()
    body: dict[str, object] = response.json()
    return body


@server.tool()
async def search(query: str, limit: int = 5) -> list[SearchHit]:
    """Search English Wikipedia and return up to `limit` matching articles."""
    limit = max(1, min(limit, 20))
    body = await query_api(
        {"list": "search", "srsearch": query, "srlimit": str(limit)}
    )
    found = body.get("query", {})
    hits = found.get("search", []) if isinstance(found, dict) else []
    return [
        SearchHit(
            title=hit["title"],
            snippet=html.unescape(TAG_RE.sub("", hit["snippet"])),
        )
        for hit in hits
    ]


@server.tool()
async def get_article(title: str) -> Article:
    """Retrieve the plain-text body of the Wikipedia article with this title."""
    body = await query_api(
        {
            "prop": "extracts|info",
            "explaintext": "1",
            "inprop": "url",
            "redirects": "1",
            "titles": title,
        }
    )
    found = body.get("query", {})
    pages = found.get("pages", []) if isinstance(found, dict) else []
    if not pages or pages[0].get("missing"):
        raise ToolError(f"no Wikipedia article titled {title!r}")
    page = pages[0]
    return Article(
        title=page["title"],
        url=page["fullurl"],
        text=page.get("extract", ""),
    )


def main() -> None:
    """Parse the command line and run the server."""
    parser = argparse.ArgumentParser(description="Wikipedia MCP server")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="log every request sent to Wikipedia",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    if args.debug:
        logger.setLevel(logging.DEBUG)

    server.run(transport="streamable-http", host="127.0.0.1", port=8002)


if __name__ == "__main__":
    main()
