# Demo 08 — Subagents: Agents That Spawn Agents

## Goal of this demo
Show that an agent can **delegate** to other agents. The main agent becomes an orchestrator: it decides what to do itself and what to hand off. This is the leap from "one agent doing things" to "agents collaborating."

**Estimated time:** 15–18 minutes
**Complexity:** High. New concept — context isolation.

---

## What pupils should walk away with
- A subagent is a fresh agent spawned by the main agent for a specific job.
- The subagent has its own context window — it doesn't see the parent's full conversation.
- Useful when: (a) the work is open-ended, (b) the output is bulky and you don't want it in the main context, (c) you can run multiple in parallel.

---

## Setup before class
1. A small codebase to investigate. Use any real project, or:

   ```bash
   git clone --depth 1 https://github.com/pallets/click /tmp/demo08
   cd /tmp/demo08
   ```

2. Launch the agent in `/tmp/demo08`.
3. Confirm the agent supports subagents (Claude Code does — it has the `Agent` tool / `Task` tool).

---

## Live script

### Step 1 — Set the scene (2 min)
> "Imagine I want to know three things about this codebase: how big is it, what's the test coverage like, and what's the most complex file. If I asked one agent to do all three serially, it would take a while and fill its memory with details I won't reuse."

### Step 2 — The single-agent approach (anti-pattern) (3 min)
Ask the main agent directly:

```txt
Investigate this repo and tell me three things: total lines of code,
how many tests exist, and which file has the most functions defined.
```

Let it work. It will read lots of files, run lots of commands. Watch the context grow. Notice that **all of those file contents are now in the main conversation** — even though we won't need them again.

### Step 3 — The subagent approach (6 min)
Now ask:

```txt
Same three questions, but spawn three subagents in parallel — one per
question. Each one investigates its own question and reports back a single
short answer. Then summarize the three answers for me.
```

Watch what happens:
1. The main agent **launches three subagents at once**.
2. Each subagent runs independently with its own tool calls and context.
3. Each returns a one-line answer.
4. The main agent stitches them into a summary.

**Make the points one at a time:**
- "**Parallel.** Three things happening simultaneously. Wall-clock time roughly = the slowest of the three."
- "**Isolated.** The main agent never saw the file contents the subagents read. Its context stayed clean."
- "**Composable.** The summary is just three short answers — the heavy lifting stayed in the subagents."

### Step 4 — Show context savings (3 min)
Compare (verbally or by glancing at the conversation length):
- Single-agent run: long, lots of file contents in scrollback.
- Subagent run: short, only the three answers.

> "If the next thing I ask is *unrelated*, the main agent in scenario two has more room to think. That's not a small thing — context is the agent's working memory."

### Step 5 — When NOT to use subagents (2 min)
Be honest:
- Subagents start fresh — they don't know what the parent knows. You have to brief them.
- For trivial tasks, the briefing overhead isn't worth it.
- For things you'll need the details of (e.g., "read this file so we can edit it together"), keep it in the main agent.

> "Subagents are for **research and reduction**. Anything where you want a small answer extracted from a big investigation."

---

## Question to throw at the class
> "If a subagent makes a wrong assumption, the main agent doesn't know. How do you protect against that?"

(Expected: write very specific subagent prompts; ask for sources/evidence in the answer; for important work, run two subagents and compare. Good lead-in to the next demo.)

---

## Common pitfalls / things to flag
- Some agents call this **"Task tool"**, others **"Agent tool"**, others **"subagent"**. Same idea.
- If the agent runs the three things sequentially instead of in parallel, **call it out**: "I asked for parallel — please launch them in one batch." This is the thing pupils need to see.
- Subagent output is summarized by default; if pupils want to see what a subagent did, you may need to dig into a transcript.
