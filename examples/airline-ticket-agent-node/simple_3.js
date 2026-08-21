#!/usr/bin/env node

/*
 * Stage 3b: same as stage 3, but the topic check is a separate LLM call.
 *
 * For every question we first ask the LLM whether the question is related to
 * flights, expecting a bare "yes" or "no". Only on "yes" do we send a second
 * request to actually answer the question. On "no" the refusal is printed by
 * this program, not by the LLM. No history is kept.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import readline from "node:readline";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-opus-5";

const CLASSIFY_SYSTEM = `
You are a classifier. The user message is a question. Decide whether the
question is at least somewhat related to flights or airline ticket sales:
flights, fares, bookings, schedules, baggage, seating, airports, airlines,
travel documents and the like. Answer with a single word: "yes" or "no".
`.trim();

const ANSWER_SYSTEM = `
You are a helpful airline ticket sales agent. Answer the user's question.
`.trim();

const apiKey = execFileSync("pass", ["show", "keys/claude.ai"], {
  encoding: "utf8",
}).trimEnd();
const client = new Anthropic({ apiKey });

function textOf(response) {
  return response.content
    .filter((block) => block.type === "text")
    .map((block) => block.text)
    .join("");
}

async function isFlightRelated(question) {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 256,
    system: CLASSIFY_SYSTEM,
    messages: [{ role: "user", content: question }],
  });
  return textOf(response).trim().toLowerCase().startsWith("yes");
}

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
    if (await isFlightRelated(question)) {
      const response = await client.messages.create({
        model: MODEL,
        max_tokens: 16000,
        system: ANSWER_SYSTEM,
        messages: [{ role: "user", content: question }],
      });
      console.log(textOf(response));
    } else {
      console.log("I cannot answer questions not related to flights.");
    }
  }
  rl.prompt();
}
console.log();
