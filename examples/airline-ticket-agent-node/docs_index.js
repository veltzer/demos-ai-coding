#!/usr/bin/env node

/*
 * Index all the documents in ./docs into a LanceDB database in ./lancedb.
 *
 * Each markdown document is split into its "## " sections and every section
 * becomes one row: the filename, the section title, the section text and an
 * embedding vector. The embeddings are computed locally with the
 * all-MiniLM-L6-v2 model (downloaded once on the first run), so no API key
 * is needed for indexing.
 *
 * The modules you need to install to make this work are `@lancedb/lancedb`
 * and `@huggingface/transformers`.
 */

import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import * as lancedb from "@lancedb/lancedb";
import { pipeline } from "@huggingface/transformers";

const DOCS_DIR = "./docs";
const DB_DIR = "./lancedb";
const TABLE = "docs";
const EMBEDDING_MODEL = "Xenova/all-MiniLM-L6-v2";

// Split a markdown document into sections, one per "## " heading; whatever
// precedes the first "## " (the "# " title line, usually) is prepended to
// every section so each chunk keeps its document context.
function sectionsOf(markdown) {
  const parts = markdown.split(/^(?=## )/m);
  const preamble = parts[0].startsWith("## ") ? "" : parts.shift().trim();
  if (parts.length === 0) {
    return [{ title: "", text: preamble }];
  }
  return parts.map((part) => ({
    title: part.match(/^## (.*)/)[1].trim(),
    text: `${preamble}\n\n${part.trim()}`.trim(),
  }));
}

console.log(`loading embedding model ${EMBEDDING_MODEL}...`);
const embedder = await pipeline("feature-extraction", EMBEDDING_MODEL);

async function embed(text) {
  const output = await embedder(text, { pooling: "mean", normalize: true });
  return Array.from(output.data);
}

const rows = [];
for (const filename of readdirSync(DOCS_DIR).sort()) {
  const fullPath = path.join(DOCS_DIR, filename);
  const sections = sectionsOf(readFileSync(fullPath, "utf8"));
  for (const { title, text } of sections) {
    rows.push({ vector: await embed(text), filename, title, text });
  }
  console.log(`indexed ${fullPath}: ${sections.length} sections`);
}

const db = await lancedb.connect(DB_DIR);
await db.createTable(TABLE, rows, { mode: "overwrite" });
console.log(
  `wrote ${rows.length} sections into table "${TABLE}" in ${DB_DIR}`,
);
