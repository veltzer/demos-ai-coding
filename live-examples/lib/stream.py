#!/usr/bin/env python3
"""Render `claude -p --output-format stream-json --verbose` as a live,
audience-readable log: one line per tool call, the assistant's prose dimmed,
a green line whenever an edit ticks a "- [x]" box in a markdown file, and a
footer with time, turns, tokens and cost.

Usage: claude -p ... | stream.py [--stats FILE]
--stats writes {"seconds", "turns", "cost", "input_tokens", "output_tokens",
"result"} as JSON for the scoreboard; "result" is the final answer text. Tokens are summed over every model the session
used; input_tokens counts cached reads too, since the model still reads them.
"""

import json
import os
import re
import sys

DIM, BOLD, CYAN, GREEN, RESET = "\033[2m", "\033[1m", "\033[36m", "\033[32m", "\033[0m"
TICKED = re.compile(r"^\s*[-*]\s+\[[xX]\]\s+(.*)$", re.MULTILINE)
BOX = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+(.*?)\s*$")
WIDTH = 100


def short(text, width=WIDTH):
    text = " ".join(str(text).split()).replace(os.getcwd() + "/", "")
    return text if len(text) <= width else text[: width - 1] + "…"


def describe(tool, args):
    for key in ("file_path", "command", "pattern", "path", "url", "description"):
        if key in args:
            return short(args[key], WIDTH - len(tool) - 4)
    return short(json.dumps(args), WIDTH - len(tool) - 4)


def full_task(path, fragment):
    """An edit often holds only the start of a task line; find the whole line."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if fragment in line and (m := BOX.match(line)):
                    return m.group(1)
    except OSError:
        pass
    return fragment


def ticks(tool, args):
    """Tasks that an Edit newly checks off in a markdown file."""
    path = str(args.get("file_path", ""))
    if tool != "Edit" or not path.endswith(".md"):
        return []
    before = set(TICKED.findall(args.get("old_string", "")))
    return [full_task(path, t.strip()) for t in TICKED.findall(args.get("new_string", ""))
            if t not in before]


def main():
    stats_file = sys.argv[sys.argv.index("--stats") + 1] if "--stats" in sys.argv else None
    for raw in sys.stdin:
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "text" and block["text"].strip():
                    for line in block["text"].strip().splitlines():
                        print(f"  {DIM}{line}{RESET}")
                elif block.get("type") == "tool_use":
                    args = block.get("input", {})
                    print(f"  {CYAN}⏺ {block['name']}{RESET} {describe(block['name'], args)}")
                    for task in ticks(block["name"], args):
                        print(f"  {GREEN}{BOLD}  ✔ {short(task, WIDTH - 6)}{RESET}")
        elif kind == "result":
            seconds = event.get("duration_ms", 0) / 1000
            turns = event.get("num_turns", 0)
            cost = event.get("total_cost_usd", 0.0)
            usage = event.get("modelUsage", {}).values()
            tokens_in = sum(u.get("inputTokens", 0) + u.get("cacheReadInputTokens", 0)
                            + u.get("cacheCreationInputTokens", 0) for u in usage)
            tokens_out = sum(u.get("outputTokens", 0) for u in usage)
            print(f"  {BOLD}done in {seconds:.0f}s, {turns} turns, "
                  f"{tokens_in:,} tokens in, {tokens_out:,} out, ${cost:.2f}{RESET}")
            if stats_file:
                with open(stats_file, "w", encoding="utf-8") as f:
                    json.dump({"seconds": seconds, "turns": turns, "cost": cost,
                               "input_tokens": tokens_in, "output_tokens": tokens_out,
                               "result": event.get("result", "")}, f)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
