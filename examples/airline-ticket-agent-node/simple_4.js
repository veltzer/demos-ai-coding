#!/usr/bin/env node

/*
 * Stage 3: same question loop, but scoped to airline ticket sales.
 *
 * A system prompt tells the model to only answer questions that are at least
 * somewhat related to airline ticket sales, and to politely refuse anything
 * else. Each question is still an independent request -- no history is kept.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import readline from "node:readline";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-opus-5";

const SYSTEM = `
You are an airline ticket sales agent. Only answer questions that are at
least somewhat related to airline ticket sales: flights, fares, bookings,
schedules, baggage, seating, airports, airlines, travel documents and the
like. If the question is about anything else, do not answer it; instead
reply exactly: "I can only answer questions related to airline ticket
sales."
`.trim();

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

console.log("Ask me about airline tickets. Press Ctrl-D to stop.");
rl.prompt();

for await (const line of rl) {
  const question = line.trim();
  if (question) {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 16000,
      system: SYSTEM,
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
