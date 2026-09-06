#!/usr/bin/env python

"""
Index the flight documents in docs/ into a persistent Chroma collection.

Each document is split on its `##` headings so that a query returns a focused
passage rather than a whole file. Re-running the script rebuilds the collection
from scratch.

The module you need to install to make this work is `chromadb`
"""

import pathlib
import re

import chromadb

DOCS_DIR = pathlib.Path(__file__).parent / "docs"
DB_DIR = pathlib.Path(__file__).parent / "chroma_db"
COLLECTION = "flights"


def chunks_of(path):
    """Split a markdown file into (section title, text) pairs on `##` headings."""
    text = path.read_text(encoding="utf-8")
    title = re.match(r"#\s+(.*)", text)
    title = title.group(1) if title else path.stem
    # Drop everything before the first `##` -- that is the document title line.
    sections = re.split(r"^##\s+", text, flags=re.MULTILINE)[1:]
    for section in sections:
        heading, _, body = section.partition("\n")
        body = body.strip()
        if body:
            yield heading.strip(), f"{title} -- {heading.strip()}\n\n{body}"


def main():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    # Rebuild from scratch so re-running never duplicates or leaves stale text.
    if COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    collection = client.create_collection(COLLECTION)

    ids, documents, metadatas = [], [], []
    for path in sorted(DOCS_DIR.glob("*.md")):
        for number, (heading, chunk) in enumerate(chunks_of(path)):
            ids.append(f"{path.stem}:{number}")
            documents.append(chunk)
            metadatas.append({"source": path.name, "section": heading})

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    files = len({m["source"] for m in metadatas})
    print(f"Indexed {len(ids)} sections from {files} documents into '{COLLECTION}'.")
    print(f"Database: {DB_DIR}")


if __name__ == "__main__":
    main()
