#!/usr/bin/env python3
"""A deliberately small RAG retriever: BM25 over markdown sections.

No embeddings, no vector database, no dependencies: retrieval is the idea,
the fancy index is an implementation detail.
"""

import inspect
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

DIM, BOLD, CYAN, RESET = "\033[2m", "\033[1m", "\033[36m", "\033[0m"
WORD = re.compile(r"[a-z0-9][a-z0-9_.:-]*[a-z0-9]|[a-z0-9]")
TOP_K = 5

PREAMBLE = "You are answering questions about the internal systems of Quillstack, a software company."
INSTRUCTIONS = """Answer every question below, each on one line in the form "Q<n>: <answer>".
Be brief. If the information is not available to you, answer "Q<n>: UNKNOWN"."""

COMMANDS = {
    "search": "search <corpus-dir> <query...>   show the top chunks for a query",
    "prompt": "prompt <corpus-dir> <questions.json> <none|rag|full> <out-file>   build a prompt",
    "stats": "stats <corpus-dir>   documents, chunks and size of the corpus",
}


def tokens(text):
    return WORD.findall(text.lower())


def chunks(corpus):
    """One chunk per "## " section, prefixed with its document's title."""
    out = []
    for path in sorted(Path(corpus).rglob("*.md")):
        text = path.read_text()
        title = text.splitlines()[0].lstrip("# ").strip()
        rel = path.relative_to(corpus)
        for section in re.split(r"(?m)^(?=## )", text)[1:]:
            heading = section.splitlines()[0].lstrip("# ").strip()
            out.append({"source": f"{rel}#{heading}", "text": f"{title}\n{section.strip()}"})
    return out


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs = [tokens(d["text"]) for d in docs]
        self.k1, self.b = k1, b
        self.avg = sum(map(len, self.docs)) / len(self.docs)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in self.docs]

    def scores(self, query):
        q = tokens(query)
        for tf, d in zip(self.tf, self.docs, strict=True):
            norm = self.k1 * (1 - self.b + self.b * len(d) / self.avg)
            yield sum(self.idf.get(t, 0) * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in q if t in tf)


def search(corpus_chunks, index, query, k=TOP_K):
    ranked = sorted(zip(index.scores(query), corpus_chunks, strict=True), key=lambda x: -x[0])
    return [(score, c) for score, c in ranked[:k] if score > 0]


def cmd_search(corpus, *query):
    cs = chunks(corpus)
    for score, c in search(cs, BM25(cs), " ".join(query)):
        first = c["text"].splitlines()
        preview = " ".join(first[2:])[:110] if len(first) > 2 else ""
        print(f"  {CYAN}{score:5.1f}{RESET}  {BOLD}{c['source']}{RESET}\n         {DIM}{preview}…{RESET}")


def cmd_prompt(corpus, questions_file, mode, out_file):
    questions = json.loads(Path(questions_file).read_text())
    parts = [PREAMBLE]
    if mode == "full":
        parts.append("Here is the company's entire internal wiki:")
        for path in sorted(Path(corpus).rglob("*.md")):
            parts.append(f"=== {path.relative_to(corpus)} ===\n{path.read_text()}")
    elif mode == "rag":
        cs = chunks(corpus)
        index = BM25(cs)
        parts.append("For each question, these are the most relevant excerpts from the internal wiki:")
        for i, q in enumerate(questions, 1):
            found = search(cs, index, q["q"])
            parts.append(f"--- excerpts for Q{i} ---\n" +
                         "\n\n".join(f"[{c['source']}]\n{c['text']}" for _, c in found))
    elif mode != "none":
        sys.exit(f"unknown mode {mode!r}: use none, rag or full")
    parts.append(INSTRUCTIONS)
    parts.append("\n".join(f"Q{i}: {q['q']}" for i, q in enumerate(questions, 1)))
    text = "\n\n".join(parts) + "\n"
    Path(out_file).write_text(text)
    print(f"{mode}: {len(text):,} characters (~{len(text) // 4:,} tokens)")


def cmd_stats(corpus):
    cs = chunks(corpus)
    size = sum(p.stat().st_size for p in Path(corpus).rglob("*.md"))
    docs = sum(1 for _ in Path(corpus).rglob("*.md"))
    print(f"{docs} documents, {len(cs)} chunks, {size:,} characters (~{size // 4:,} tokens)")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        if len(sys.argv) >= 2 and sys.argv[1] not in ("-h", "--help"):
            print(f"unknown command: {sys.argv[1]}\n")
        print("usage: rag.py <command> ...\n\ncommands:")
        for usage in COMMANDS.values():
            print(f"  {usage}")
        return 0 if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help") else 2
    command, args = sys.argv[1], sys.argv[2:]
    func = {"search": cmd_search, "prompt": cmd_prompt, "stats": cmd_stats}[command]
    try:
        inspect.signature(func).bind(*args)
    except TypeError:
        print(f"usage: rag.py {COMMANDS[command]}")
        return 2
    func(*args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
