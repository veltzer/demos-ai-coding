#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "math-mcp-service",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "Add two numbers together",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "First number",
            },
            b: {
              type: "number",
              description: "Second number",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "multiply",
        description: "Multiply two numbers",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "First number",
            },
            b: {
              type: "number",
              description: "Second number",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "get_random_fact",
        description: "Get a random math fact",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "add":
      const sum = args.a + args.b;
      return {
        content: [
          {
            type: "text",
            text: `${args.a} + ${args.b} = ${sum}`,
          },
        ],
      };

    case "multiply":
      const product = args.a * args.b;
      return {
        content: [
          {
            type: "text",
            text: `${args.a} × ${args.b} = ${product}`,
          },
        ],
      };

    case "get_random_fact":
      const facts = [
        "Zero is the only number that is neither positive nor negative.",
        "The number 9 is considered a magic number because when you multiply any number by 9, the digits of the result always add up to 9.",
        "Pi (π) has been calculated to over 31 trillion decimal places.",
        "The fibonacci sequence appears frequently in nature, like in flower petals and spiral shells.",
        "There are exactly 177,147 ways to tie a tie.",
      ];
      const randomFact = facts[Math.floor(Math.random() * facts.length)];
      return {
        content: [
          {
            type: "text",
            text: `Math Fact: ${randomFact}`,
          },
        ],
      };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Math MCP service running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});