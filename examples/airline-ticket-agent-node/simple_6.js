#!/usr/bin/env node

/*
 * Stage 6: add a /clear command.
 *
 * Same ticket-selling agent as stage 5, but the user can type "/clear" to
 * throw away the conversation history and start from scratch. The command is
 * handled by this program -- it never reaches the LLM.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import readline from "node:readline";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-opus-5";

const SYSTEM = `
You are an airline ticket sales agent. Only discuss things related to
airline ticket sales; if asked about anything else, reply that you can only
answer questions related to airline ticket sales.

Your goal is to sell the user a ticket. For that you need three pieces of
information: the departure city, the arrival city and the date of the
flight. Ask for whatever is still missing. As soon as you know all three,
call the buy_the_ticket tool without asking for further confirmation, then
tell the user the ticket was bought.
`.trim();

const TOOLS = [
  {
    name: "buy_the_ticket",
    description:
      "Buy a flight ticket. Call this only once the departure city, " +
      "the arrival city and the date of the flight are all known.",
    input_schema: {
      type: "object",
      properties: {
        departure_city: { type: "string", description: "City to fly from" },
        arrival_city: { type: "string", description: "City to fly to" },
        date: { type: "string", description: "Date of the flight" },
      },
      required: ["departure_city", "arrival_city", "date"],
    },
  },
];

function buyTheTicket({ departure_city, arrival_city, date }) {
  console.log(
    `buying the ticket with data: departure_city=${departure_city}, ` +
      `arrival_city=${arrival_city}, date=${date}`,
  );
  return "the ticket was bought successfully";
}

const apiKey = execFileSync("pass", ["show", "keys/claude.ai"], {
  encoding: "utf8",
}).trimEnd();
const client = new Anthropic({ apiKey });

// The whole conversation, shared by all turns; /clear empties it.
let messages = [];

async function handleUserTurn(question) {
  messages.push({ role: "user", content: question });
  // Inner agentic loop: keep going as long as the model wants to call tools.
  while (true) {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 16000,
      system: SYSTEM,
      tools: TOOLS,
      messages,
    });
    messages.push({ role: "assistant", content: response.content });
    for (const block of response.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
    if (response.stop_reason !== "tool_use") {
      break;
    }
    const toolResults = [];
    for (const block of response.content) {
      if (block.type === "tool_use") {
        // buy_the_ticket is the only tool we declared.
        const result = buyTheTicket(block.input);
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: result,
        });
      }
    }
    messages.push({ role: "user", content: toolResults });
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: "\n> ",
});
rl.on("SIGINT", () => rl.close());

console.log(
  "Hello, I sell airline tickets. Type /clear to start over. " +
    "Press Ctrl-D to stop.",
);
rl.prompt();

for await (const line of rl) {
  const question = line.trim();
  if (question === "/clear") {
    messages = [];
    console.log("conversation history cleared, starting from scratch");
  } else if (question) {
    await handleUserTurn(question);
  }
  rl.prompt();
}
console.log();
