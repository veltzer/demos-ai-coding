#!/usr/bin/env node

/*
 * Search the LanceDB database built by index_docs.js.
 *
 * Usage: ./search_docs.js <question...>
 * Example: ./search_docs.js how heavy can my suitcase be
 *
 * The question is embedded with the same model used for indexing and the
 * closest sections are printed, best match first.
 */

import * as lancedb from "@lancedb/lancedb";
import { pipeline } from "@huggingface/transformers";

const DB_DIR = "./lancedb";
const TABLE = "docs";
const EMBEDDING_MODEL = "Xenova/all-MiniLM-L6-v2";
const LIMIT = 3;

const question = process.argv.slice(2).join(" ").trim();
if (!question) {
  console.error("usage: search_docs.js <question...>");
  process.exit(1);
}

const embedder = await pipeline("feature-extraction", EMBEDDING_MODEL);
const output = await embedder(question, { pooling: "mean", normalize: true });
const vector = Array.from(output.data);

const db = await lancedb.connect(DB_DIR);
const table = await db.openTable(TABLE);
const hits = await table.search(vector).limit(LIMIT).toArray();

for (const hit of hits) {
  console.log(
    `=== ${hit.filename} / ${hit.title} (distance ${hit._distance.toFixed(3)}) ===`,
  );
  console.log(hit.text);
  console.log();
}
