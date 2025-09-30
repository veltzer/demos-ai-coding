# Simple Math MCP Service Exercise

This exercise demonstrates how to create and use a Model Context Protocol (MCP) service with GitHub Copilot in VS Code.

## What is MCP?

MCP (Model Context Protocol) allows AI assistants like GitHub Copilot to interact with external tools and services. This example creates a simple math service that Copilot can use to perform calculations and get math facts.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Test the MCP Service

First, let's verify the service works:

```bash
node math-mcp-service.js
```

You should see: `Math MCP service running on stdio`

Press `Ctrl+C` to stop it.

### 3. Configure VS Code

Create or edit your VS Code settings to include the MCP service:

1. Write this snipplet into `~/.config/mcp/my_mcp.json`:

```json
{
  "github.copilot.chat.mcp.servers": {
    "math-service": {
      "command": "node",
      "args": ["/full/path/to/math-mcp-service.js"]
    }
  }
}
```

**Important**: Replace `/full/path/to/` with the actual full path to your project directory.

### 4. Restart VS Code

After adding the configuration, restart VS Code completely to load the MCP service.

## How to Test It's Working

### Method 1: GitHub Copilot Chat

1. Open GitHub Copilot Chat (`Ctrl+Shift+I` or click the chat icon)
2. Try these prompts:

```
Can you add 15 and 27 for me?
```

```
What's 8 multiplied by 12?
```

```
Tell me a random math fact
```

### Method 2: Check MCP Connection

1. In Copilot Chat, type:
```
What MCP tools do you have access to?
```

You should see the math tools listed: `add`, `multiply`, and `get_random_fact`.

## Available Tools

The MCP service provides three tools:

- **add**: Adds two numbers together
- **multiply**: Multiplies two numbers
- **get_random_fact**: Returns a random mathematical fact

## Troubleshooting

### Service Not Found
- Ensure the full path in VS Code settings is correct
- Restart VS Code after configuration changes
- Check that Node.js is installed and accessible

### Copilot Not Using Tools
- Make sure GitHub Copilot extension is enabled
- Try being more explicit: "Use the math tools to calculate..."
- Check the VS Code Output panel for any error messages

### Debugging
To see if your MCP service is running, you can check the VS Code Output panel:
1. Go to View → Output
2. Select "GitHub Copilot" from the dropdown
3. Look for messages about MCP services

## Example Conversation

Here's what a successful interaction looks like:

**You**: Can you add 42 and 58 using the math service?

**Copilot**: I'll use the math service to add those numbers for you.

*[Copilot calls the add tool]*

**Copilot**: 42 + 58 = 100

## Next Steps

Once this is working, you can:
- Add more mathematical operations to the service
- Create MCP services for other domains (file operations, web APIs, etc.)
- Explore more complex MCP features like resources and prompts

The key is seeing Copilot successfully call your MCP tools rather than doing calculations itself!
