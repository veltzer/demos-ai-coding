#!/usr/bin/env python3
"""Show a prompt to the audience as a readable box instead of a quoted
command line.

Usage: prompt_box.py <title> <prompt-file> [note...]
The prompt is wrapped to the terminal width. A long prompt shows its first
and last lines with a count of what was skipped, since instructions and
questions usually come at the end. Each note is a dim line under the title.
"""

import shutil
import sys
import textwrap

BOLD, DIM, CYAN, RESET = "\033[1m", "\033[2m", "\033[36m", "\033[0m"
HEAD, TAIL = 8, 12


def wrap(text, width):
    lines = []
    for line in text.rstrip("\n").splitlines():
        indent = line[:len(line) - len(line.lstrip())]
        lines.extend(textwrap.wrap(line, width, subsequent_indent=indent) or [""])
    return lines


def main():
    title, path, notes = sys.argv[1], sys.argv[2], sys.argv[3:]
    with open(path, encoding="utf-8") as f:
        text = f.read()
    width = max(40, min(shutil.get_terminal_size((100, 24)).columns, 104) - 6)
    lines = wrap(text, width)
    if len(lines) > HEAD + TAIL + 3:
        skipped = len(lines) - HEAD - TAIL
        lines = [*lines[:HEAD], f"{DIM}⋮  {skipped:,} more lines ({len(text):,} characters in all)  ⋮{RESET}",
                 *lines[-TAIL:]]
    bar = "─" * (width + 2)
    print(f"\n  {CYAN}┌─{RESET} {BOLD}{title}{RESET}")
    for note in notes:
        print(f"  {CYAN}│{RESET}  {DIM}{note}{RESET}")
    print(f"  {CYAN}│{RESET}")
    for line in lines:
        print(f"  {CYAN}│{RESET}  {BOLD}{line}{RESET}")
    print(f"  {CYAN}└{bar}{RESET}\n")


if __name__ == "__main__":
    main()
