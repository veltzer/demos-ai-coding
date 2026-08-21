#!/usr/bin/env node

/*
 * Stage 7: let the model read a preferences file the user names.
 *
 * If the user's message contains a filename, the model is offered a
 * `read_preferences` tool for that turn. The client -- not the model -- does
 * the reading, and only for a filename the user actually typed, so the model
 * cannot reach a file the user did not ask for.
 *
 * The module you need to install to make this work is `@anthropic-ai/sdk`.
 * The api key is read from pass(1) via `pass show keys/claude.ai`.
 */

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
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

If the user names a preferences file, read it with the read_preferences
tool and take the preferences in it into account when selling the ticket.
`.trim();

const BUY_TOOL = {
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
};

const READ_PREFERENCES_TOOL = {
  name: "read_preferences",
  description:
    "Read the preferences file the user named in their message and " +
    "return its content.",
  input_schema: {
    type: "object",
    properties: {
      filename: {
        type: "string",
        description: "The filename exactly as the user typed it",
      },
    },
    required: ["filename"],
  },
};

// Debugging prints: [agent] is this program acting, [llm] is the model.
function debug(who, text) {
  console.log(`\x1b[2m[${who}] ${text}\x1b[0m`);
}

function buyTheTicket({ departure_city, arrival_city, date }) {
  console.log(
    `buying the ticket with data: departure_city=${departure_city}, ` +
      `arrival_city=${arrival_city}, date=${date}`,
  );
  return { content: "the ticket was bought successfully" };
}

// The client decides what looks like a filename; the model is only ever
// allowed to read those. Words like "prefs.txt", "./prefs.txt" or
// "/home/user/prefs.txt" qualify once surrounding punctuation is stripped.
function filenamesIn(text) {
  const names = [];
  for (let word of text.split(/\s+/)) {
    word = word.replace(/^["'(]+|["'),.?!:;]+$/g, "");
    if (/^[\w~/.-]+\.\w+$/.test(word)) {
      names.push(word);
    }
  }
  return names;
}

function readPreferences({ filename }, allowedFilenames) {
  if (!allowedFilenames.includes(filename)) {
    return {
      content: `reading ${filename} is not allowed: the user did not name it`,
      is_error: true,
    };
  }
  try {
    return { content: readFileSync(filename, "utf8") };
  } catch (err) {
    return { content: `cannot read ${filename}: ${err.message}`, is_error: true };
  }
}

const apiKey = execFileSync("pass", ["show", "keys/claude.ai"], {
  encoding: "utf8",
}).trimEnd();
const client = new Anthropic({ apiKey });

// The whole conversation, shared by all turns; /clear empties it.
let messages = [];

async function handleUserTurn(question) {
  messages.push({ role: "user", content: question });
  // Only a turn whose message names a file offers the read_preferences tool.
  const allowedFilenames = filenamesIn(question);
  const tools = allowedFilenames.length
    ? [BUY_TOOL, READ_PREFERENCES_TOOL]
    : [BUY_TOOL];
  if (allowedFilenames.length) {
    debug(
      "agent",
      `filenames found in the message: ${allowedFilenames.join(", ")} -- ` +
        "offering the read_preferences tool this turn",
    );
  }
  // Inner agentic loop: keep going as long as the model wants to call tools.
  while (true) {
    debug(
      "agent",
      `sending request to the llm ` +
        `(${messages.length} messages, ${tools.length} tools)`,
    );
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 16000,
      system: SYSTEM,
      tools,
      messages,
    });
    debug("llm", `answered with stop_reason=${response.stop_reason}`);
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
        debug(
          "llm",
          `wants to call ${block.name} with ${JSON.stringify(block.input)}`,
        );
        debug("agent", `executing ${block.name}`);
        const result =
          block.name === "read_preferences"
            ? readPreferences(block.input, allowedFilenames)
            : buyTheTicket(block.input);
        debug(
          "agent",
          `${block.name} ${result.is_error ? "failed" : "succeeded"}: ` +
            `sending ${result.content.length} characters back`,
        );
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          ...result,
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
