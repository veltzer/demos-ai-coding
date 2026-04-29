# Demo 07 — Extending the Agent: MCP Servers

## Goal of this demo
So far the agent has used the **built-in** tools (Read, Write, Bash, WebFetch). Now show pupils that you can **plug in new tools** via MCP (Model Context Protocol) — and the agent will start using them as if they'd always been there.

**Estimated time:** 15 minutes
**Complexity:** Higher. There's installation and configuration to walk through.

---

## What pupils should walk away with
- An agent's tools are not fixed — you can add more.
- MCP is an open protocol; many servers exist (filesystem, github, postgres, slack, puppeteer, etc.).
- Once installed and configured, the agent **discovers** the new tools automatically.

---

## Setup before class
**Do this before pupils arrive — installation live is risky.**

1. Pick **one** MCP server that's reliable and impressive. Good first choices:
   - **Sequential-thinking** — no API key, always works, fun to demo.
   - **Filesystem** restricted to a sandbox dir — concrete and visual.
   - **Puppeteer** — flashy (takes screenshots) but heavier.

2. For this demo we'll use **Sequential-thinking** as the safe default. Install it:

   ```bash
   npx -y @modelcontextprotocol/server-sequential-thinking --help
   ```

3. Configure your agent to use it. For Claude Code, edit `~/.config/mcp/config.json` (or the equivalent for your client):

   ```json
   {
     "mcpServers": {
       "sequential-thinking": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
       }
     }
   }
   ```

4. Restart the agent so it picks up the new server.
5. **Verify before class** that the new tool shows up in the agent's tool list.

---

## Live script

### Step 1 — Show the "before" (2 min)
With the MCP server *disabled* (or using a fresh session that hasn't loaded it), ask the agent:

```txt
What tools do you have available?
```

It will list the built-ins. Note the absence of anything called "sequential thinking."

### Step 2 — Enable the MCP server and reload (3 min)
On screen, walk through:
1. The config file — show the JSON.
2. Restarting the agent.
3. Asking again: "What tools do you have available?" — now the new tool appears.

**Make the point:**
> "We didn't retrain the model. We didn't change the agent. We just gave it a new tool, and it knows how to use it."

### Step 3 — Use the new tool (5 min)
Give the agent a problem that benefits from structured reasoning:

```txt
Use the sequential-thinking tool to design a strategy for migrating a
500-table PostgreSQL database to a new schema with zero downtime.
Walk through your reasoning step by step.
```

Watch the agent invoke the new MCP tool. The thinking will be more structured than usual — that's the value. Read a few of the steps aloud.

### Step 4 — Mention the ecosystem (3 min)
Show pupils the breadth without installing more. Just *talk through* a few:

- **GitHub MCP** — agent can list issues, open PRs.
- **Postgres MCP** — agent can run SQL.
- **Slack MCP** — agent can post messages.
- **Filesystem MCP** — sandboxed file ops.
- **Puppeteer MCP** — agent drives a real browser.

**The big idea:**
> "If your team has a system, you can probably wrap it as an MCP server, and now the agent can talk to it. The agent's reach is whatever you give it."

### Step 5 — A note on trust (2 min)
This is the **must-say** part:

> "Every MCP server you install can read your conversations and run code. Treat them like browser extensions — install only what you trust, from sources you trust."

---

## Question to throw at the class
> "If you could give the agent **one** custom tool for your job, what would it be?"

(Great class discussion. Common answers: query our internal API, read our ticket system, deploy to staging. Many of these can become real MCP servers — see Demo 08 setup.)

---

## Common pitfalls / things to flag
- **Test before class.** MCP install can hit weird npm/node version issues. Solving them live is brutal.
- Keep the config file simple. One server. Don't try to demo five at once.
- Don't go deep into building an MCP server — that's a separate session. This demo is about *using* them.
