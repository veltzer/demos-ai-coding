#!/usr/bin/env python3
"""Render `claude -p --output-format stream-json --verbose` as a live,
audience-readable log: one line per tool call, the assistant's prose dimmed,
a green line whenever an edit ticks a "- [x]" box in a markdown file, a red
line when a tool call is refused (a hook block, a permission denial), and a
footer with time, turns, tokens and cost.

On a terminal, a status line under the log redraws every quarter second:
what the session is doing now (thinking, writing, preparing or running a
tool), how long it has run, and how long since its last sign of life, yellow
after a minute of silence and red after five. It needs claude's
--include-partial-messages to see thinking and typing as they happen.

Usage: claude -p ... | stream.py [--stats FILE]
--stats writes {"seconds", "turns", "cost", "input_tokens", "output_tokens",
"result", "commands", "session_id"} as JSON for the scoreboard; "result" is
the final answer text and "commands" every Bash command the session ran. Tokens are summed over every model the session
used; input_tokens counts cached reads too, since the model still reads them.
"""

import json
import os
import re
import sys
import threading
import time

DIM, BOLD, CYAN, GREEN, RED, RESET = "\033[2m", "\033[1m", "\033[36m", "\033[32m", "\033[31m", "\033[0m"
YELLOW, CLEAR_LINE = "\033[33m", "\r\033[K"
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
QUIET, STUCK = 60, 300
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


def clock(seconds):
    seconds = int(seconds)
    return f"{seconds // 60}m {seconds % 60:02d}s" if seconds >= 60 else f"{seconds}s"


class Status:
    """The live bottom line. Every print goes through emit() so the log
    scrolls above it and the line is redrawn underneath."""

    def __init__(self):
        self.live = sys.stdout.isatty()
        self.lock = threading.Lock()
        self.start = self.seen = time.monotonic()
        self.doing = "starting the session"
        self.chars = 0
        self.done = False

    def emit(self, line):
        with self.lock:
            if self.live:
                sys.stdout.write(CLEAR_LINE)
            print(line)
            self.draw()

    def update(self, doing=None):
        with self.lock:
            self.seen = time.monotonic()
            if doing is not None:
                self.doing, self.chars = doing, 0

    def stop(self):
        with self.lock:
            self.done = True
            if self.live:
                sys.stdout.write(CLEAR_LINE)
                sys.stdout.flush()

    def draw(self):
        if not self.live or self.done:
            sys.stdout.flush()
            return
        now = time.monotonic()
        idle = now - self.seen
        spin = SPINNER[int(now * 4) % len(SPINNER)]
        doing = self.doing + (f" ({self.chars:,} chars so far)" if self.chars else "")
        line = f"  {spin} {short(doing, 60)} · {clock(now - self.start)} in"
        if idle >= STUCK:
            line = (f"{RED}{BOLD}{line} · no sign of life for {clock(idle)}: "
                    f"may be stuck, Ctrl-C stops the demo{RESET}")
        elif idle >= QUIET:
            line = f"{YELLOW}{line} · quiet for {clock(idle)} (long thinking and slow commands are normal){RESET}"
        else:
            line = f"{DIM}{line} · last sign of life {clock(idle)} ago{RESET}"
        sys.stdout.write(CLEAR_LINE + line)
        sys.stdout.flush()

    def run(self):
        while not self.done:
            with self.lock:
                self.draw()
            time.sleep(0.25)


def partial(status, event):
    """A --include-partial-messages chunk: name what the model is producing."""
    inner = event.get("event", {})
    if inner.get("type") == "content_block_start":
        block = inner.get("content_block", {})
        status.update({"thinking": "thinking", "redacted_thinking": "thinking",
                       "text": "writing its answer"}.get(block.get("type"),
                       f"preparing a {block.get('name', 'tool')} call"))
    elif inner.get("type") == "content_block_delta":
        delta = inner.get("delta", {})
        status.update()
        status.chars += len(delta.get("partial_json", "") or delta.get("text", "")
                            or delta.get("thinking", ""))
    else:
        status.update()


def main():
    stats_file = sys.argv[sys.argv.index("--stats") + 1] if "--stats" in sys.argv else None
    commands = []
    status = Status()
    if status.live:
        threading.Thread(target=status.run, daemon=True).start()
    emit = status.emit
    for raw in sys.stdin:
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "stream_event":
            partial(status, event)
        elif kind == "assistant":
            status.update()
            for block in event["message"].get("content", []):
                if block.get("type") == "text" and block["text"].strip():
                    for line in block["text"].strip().splitlines():
                        emit(f"  {DIM}{line}{RESET}")
                elif block.get("type") == "tool_use":
                    args = block.get("input", {})
                    if block["name"] == "Bash":
                        commands.append(args.get("command", ""))
                    emit(f"  {CYAN}⏺ {block['name']}{RESET} {describe(block['name'], args)}")
                    status.update(f"running {block['name']}: {describe(block['name'], args)}")
                    for task in ticks(block["name"], args):
                        emit(f"  {GREEN}{BOLD}  ✔ {short(task, WIDTH - 6)}{RESET}")
        elif kind == "user":
            status.update("thinking")
            for block in event.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result" and block.get("is_error"):
                    content = block.get("content", "")
                    if isinstance(content, list):
                        content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
                    if "hook" in content.lower() or "denied" in content.lower() or "blocked" in content.lower():
                        emit(f"  {RED}{BOLD}  ✘ {short(content, WIDTH - 6)}{RESET}")
        elif kind == "result":
            seconds = event.get("duration_ms", 0) / 1000
            turns = event.get("num_turns", 0)
            cost = event.get("total_cost_usd", 0.0)
            usage = event.get("modelUsage", {}).values()
            tokens_in = sum(u.get("inputTokens", 0) + u.get("cacheReadInputTokens", 0)
                            + u.get("cacheCreationInputTokens", 0) for u in usage)
            tokens_out = sum(u.get("outputTokens", 0) for u in usage)
            status.stop()
            print(f"  {BOLD}done in {seconds:.0f}s, {turns} turns, "
                  f"{tokens_in:,} tokens in, {tokens_out:,} out, ${cost:.2f}{RESET}")
            if stats_file:
                with open(stats_file, "w", encoding="utf-8") as f:
                    json.dump({"seconds": seconds, "turns": turns, "cost": cost,
                               "input_tokens": tokens_in, "output_tokens": tokens_out,
                               "result": event.get("result", ""), "commands": commands,
                               "session_id": event.get("session_id", "")}, f)
        else:
            status.update()
    status.stop()


if __name__ == "__main__":
    main()
