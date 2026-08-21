#!/usr/bin/env node

/*
 * Stage 1: issue one hardcoded prompt to anthropic and print the answer.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-opus-5";

const QUERY = `
What is the capitol of France and how many residents are there?
Make your answer just a string and number with a comma in the middle
`;

const apiKey = execFileSync("pass", ["show", "keys/claude.ai"], {
  encoding: "utf8",
}).trimEnd();
const client = new Anthropic({ apiKey });

const response = await client.messages.create({
  model: MODEL,
  max_tokens: 16000,
  messages: [{ role: "user", content: QUERY }],
});

// response.content is a list of blocks (thinking, text, ...) -- only the text
// blocks have a .text attribute, so filter rather than indexing [0].
for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
