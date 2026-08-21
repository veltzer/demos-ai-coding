#!/usr/bin/env python

"""
Search the indexed flight documents.

Usage: python search_docs.py "how much luggage can I bring"

The module you need to install to make this work is `chromadb`
"""

import pathlib
import sys

import chromadb

DB_DIR = pathlib.Path(__file__).parent / "chroma_db"
COLLECTION = "flights"
RESULTS = 3


def search(query, n_results=RESULTS):
    """Return the closest indexed sections to the query."""
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection(COLLECTION)
    found = collection.query(query_texts=[query], n_results=n_results)
    return zip(found["documents"][0], found["metadatas"][0], found["distances"][0])


def main():
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <query>")
    query = " ".join(sys.argv[1:])
    print(f"Query: {query}\n")
    for document, metadata, distance in search(query):
        print(f"[{distance:.3f}] {metadata['source']} -- {metadata['section']}")
        body = document.split("\n\n", 1)[1]
        print(f"    {body[:200].replace(chr(10), ' ')}...\n")


if __name__ == "__main__":
    main()
