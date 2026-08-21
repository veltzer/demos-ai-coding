#!/usr/bin/env node

/*
 * Stage 2: loop asking the user for questions and issuing them to anthropic.
 *
 * Each question is an independent request -- no conversation history is kept,
 * so follow-up questions do not work yet.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import readline from "node:readline";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-opus-5";

const apiKey = execFileSync("pass", ["show", "keys/claude.ai"], {
  encoding: "utf8",
}).trimEnd();
const client = new Anthropic({ apiKey });

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: "\n> ",
});
rl.on("SIGINT", () => rl.close());

console.log("Ask me anything. Press Ctrl-D to stop.");
rl.prompt();

// The async iterator yields one line per question and ends on Ctrl-D (EOF).
for await (const line of rl) {
  const question = line.trim();
  if (question) {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 16000,
      messages: [{ role: "user", content: question }],
    });
    for (const block of response.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
  }
  rl.prompt();
}
console.log();
