#!/usr/bin/env python3
"""Score the three answer sets against the known answers.

Usage: score.py <questions.json> <label>=<stats.json> ...
Prints a question-by-mode table and, per mode, correct / wrong / unknown.
Writes "<stats.json minus .json>.score" with "<correct>/<total>" for the scoreboard.
"""

import json
import re
import sys
from pathlib import Path

DIM, BOLD, GREEN, RED, YELLOW, RESET = "\033[2m", "\033[1m", "\033[32m", "\033[31m", "\033[33m", "\033[0m"
LOOK = {"correct": (GREEN, "✔ right"), "wrong": (RED, "✘ wrong"), "unknown": (YELLOW, "? unknown")}


def answers(stats_file):
    text = json.loads(Path(stats_file).read_text()).get("result", "")
    return {int(m.group(1)): m.group(2).strip()
            for m in re.finditer(r"(?m)^\W*Q(\d+)\W*[:.)]\s*(.*)$", text)}


def grade(question, answer):
    if not answer or "UNKNOWN" in answer.upper():
        return "correct" if question["expect"] == ["UNKNOWN"] else "unknown"
    if question["expect"] == ["UNKNOWN"]:
        return "wrong"
    ok = all(e.lower() in answer.lower() for e in question["expect"])
    return "correct" if ok else "wrong"


def main():
    questions = json.loads(Path(sys.argv[1]).read_text())
    modes = [arg.split("=", 1) for arg in sys.argv[2:]]
    got = {label: answers(path) for label, path in modes}
    width = 16
    print(f"  {BOLD}{'':<4}{'question':<62}" + "".join(f"{label:<{width}}" for label, _ in modes) + RESET)
    totals = {label: {"correct": 0, "wrong": 0, "unknown": 0} for label, _ in modes}
    for i, q in enumerate(questions, 1):
        row = f"  Q{i:<3}{q['q'][:60]:<62}"
        for label, _ in modes:
            g = grade(q, got[label].get(i, ""))
            totals[label][g] += 1
            colour, text = LOOK[g]
            row += f"{colour}{text:<{width}}{RESET}"
        print(row)
        if q.get("note"):
            print(f"      {DIM}{q['note']}{RESET}")
    print()
    for label, path in modes:
        t = totals[label]
        print(f"  {BOLD}{label:<14}{RESET} {GREEN}{t['correct']} right{RESET}, "
              f"{RED}{t['wrong']} wrong{RESET}, {YELLOW}{t['unknown']} unknown{RESET}")
        Path(path).with_suffix(".score").write_text(f"{t['correct']}/{len(questions)}\n")


if __name__ == "__main__":
    main()
