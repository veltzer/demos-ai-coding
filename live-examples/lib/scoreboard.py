#!/usr/bin/env python3
"""Print a scoreboard of claude runs from the --stats files stream.py writes.

Usage: scoreboard.py ROW... where ROW is "label|score|stats.json[,stats.json...]".
Several stats files in one row are summed. An empty label prints a rule.
"""

import json
import sys

BOLD, RESET = "\033[1m", "\033[0m"
FIELDS = ("seconds", "input_tokens", "output_tokens", "cost")


def load(paths):
    total = dict.fromkeys(FIELDS, 0)
    for path in filter(None, paths.split(",")):
        try:
            with open(path, encoding="utf-8") as f:
                stats = json.load(f)
        except (OSError, ValueError):
            continue
        for field in FIELDS:
            total[field] += stats.get(field, 0)
    return total


def main():
    header = f"  {'':<24}{'score':>7}{'AI time':>9}{'tokens in':>12}{'tokens out':>12}{'cost':>8}"
    print(BOLD + header + RESET)
    for spec in sys.argv[1:]:
        label, score, paths = spec.split("|")
        if not label:
            print("  " + "─" * (len(header) - 2))
            continue
        t = load(paths)
        line = (f"  {label:<24}{score:>7}{t['seconds']:>8.0f}s{t['input_tokens']:>12,}"
                f"{t['output_tokens']:>12,}{'$' + format(t['cost'], '.2f'):>8}")
        print(BOLD + line + RESET if "total" in label else line)


if __name__ == "__main__":
    main()
