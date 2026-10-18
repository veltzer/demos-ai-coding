#!/usr/bin/env python3
"""Render a markdown plan with checkboxes as a coloured checklist with a
progress bar per phase and overall.

Usage: checklist.py plan.md [--summary]
--summary prints only "<done> <total>" (for scripts).
Phases are "## ..." headings; tasks are "- [ ]" / "- [x]" lines.
"""

import re
import sys

DIM, BOLD, GREEN, YELLOW, RESET = "\033[2m", "\033[1m", "\033[32m", "\033[33m", "\033[0m"
BOX = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$")


def parse(path):
    phases, current = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                current = (line[3:].strip(), [])
                phases.append(current)
            elif (m := BOX.match(line)) and current:
                current[1].append((m.group(1) != " ", m.group(2).strip()))
    return [p for p in phases if p[1]]


def bar(done, total, width=30):
    filled = round(width * done / total) if total else 0
    return f"{GREEN}{'█' * filled}{DIM}{'░' * (width - filled)}{RESET}"


def main():
    phases = parse(sys.argv[1])
    done = sum(ok for _, tasks in phases for ok, _ in tasks)
    total = sum(len(tasks) for _, tasks in phases)
    if "--summary" in sys.argv:
        print(done, total)
        return
    first_open = next((i for i, (_, tasks) in enumerate(phases)
                       if not all(ok for ok, _ in tasks)), None)
    for i, (title, tasks) in enumerate(phases):
        n = sum(ok for ok, _ in tasks)
        colour = GREEN if n == len(tasks) else YELLOW if i == first_open else DIM
        print(f"  {colour}{BOLD}{title}{RESET}  {DIM}{n}/{len(tasks)}{RESET}")
        for ok, text in tasks:
            print(f"     {GREEN}✔{RESET} {text}" if ok else f"     {DIM}☐ {text}{RESET}")
    print(f"\n  {bar(done, total)}  {BOLD}{done}/{total}{RESET} tasks"
          f"  ({100 * done // total if total else 0}%)")


if __name__ == "__main__":
    main()
