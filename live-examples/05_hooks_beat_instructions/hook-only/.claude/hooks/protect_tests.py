#!/usr/bin/env python3
"""PreToolUse hook: nothing may change files under tests/.

Exit code 2 blocks the tool call and hands the message on stderr back to
the model. If DEMO_HOOK_LOG is set, every block is also appended there, so
the demo can count them.
"""

import json
import os
import re
import sys
from pathlib import Path

MESSAGE = ("Blocked by hook: tests/ belongs to the QA team and cannot be changed. "
           "Finish the code change and list the test changes QA should make in your final message.")
# A path under tests/ (needs the slash, so "discover -s tests" is not a match).
TESTS_PATH = re.compile(r"(^|[\s'\"=/(])tests/")
# Shell operations that write, move or delete the files named in the same segment.
WRITE_OPS = re.compile(r"(\bsed\s+-i|\bperl\s+-i|\btee\b|\bmv\b|\bcp\b|\brm\b|\btruncate\b|"
                       r"\btouch\b|\bgit\s+(checkout|restore)\b|(^|[^0-9&])>)")
# Python writing a file, anywhere in the command (heredocs, -c).
PY_WRITE = re.compile(r"open\([^)]*['\"][wax]b?['\"]|\.write_text\(|\.write_bytes\(")


def bash_writes_tests(command):
    if not TESTS_PATH.search(command):
        return False
    if PY_WRITE.search(command):
        return True
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        if TESTS_PATH.search(segment) and WRITE_OPS.search(segment):
            return True
    return False


def touches_tests(event):
    project = Path(event.get("cwd") or os.getcwd()).resolve()
    tests = project / "tests"
    args = event.get("tool_input", {})
    if event.get("tool_name") == "Bash":
        return bash_writes_tests(args.get("command", ""))
    path = args.get("file_path") or args.get("notebook_path")
    if not path:
        return False
    target = (project / path).resolve()
    return target == tests or tests in target.parents


def main():
    event = json.load(sys.stdin)
    if not touches_tests(event):
        return 0
    if log := os.environ.get("DEMO_HOOK_LOG"):
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tool": event.get("tool_name"), "input": event.get("tool_input")}) + "\n")
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
