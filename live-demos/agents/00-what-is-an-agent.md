# Demo 00 — What Is an Agent?

## Goal of this demo
Introduce the pupils to the very basic idea: an **agent** is an LLM that can take actions in the world, not just talk. Before showing actions, contrast with a plain chat so the difference lands.

**Estimated time:** 5–7 minutes
**Complexity:** Trivial. This is the warm-up.

---

## What pupils should walk away with
- An agent = LLM + tools + a loop ("think → act → observe → think again").
- Without tools, the LLM can only produce text. With tools, it can read files, run commands, search the web, etc.
- Today's demos use Claude Code (or GitHub Copilot Agent Mode) as the agent.

---

## Setup before class
1. Open a terminal in an **empty scratch directory** (e.g., `/tmp/agent-demo`).
2. Have a browser tab open to a regular chat (claude.ai or ChatGPT) on a second screen.
3. Have Claude Code (or your agent of choice) ready to launch in the terminal.

---

## Live script

### Step 1 — The "no tools" baseline (2 min)
On the **browser chat** (not the agent), type:

```txt
What files are in my home directory right now?
```

Show the answer. The model will say something like *"I can't access your filesystem"* — or worse, hallucinate a list. **This is the moment.** Say out loud:

> "The model has no hands. It can talk, but it cannot look. That's a chat."

### Step 2 — Same question, to the agent (2 min)
Switch to the terminal, launch Claude Code, and ask exactly the same thing:

```txt
What files are in my home directory right now?
```

Pupils will see the agent **call a tool** (probably `Bash` running `ls ~`), get a real result, and answer with the actual files.

### Step 3 — Narrate the loop (2 min)
Point at the screen and name the parts as they appear:
1. **Think** — "The model decides it needs to run `ls`."
2. **Act** — "It calls the Bash tool."
3. **Observe** — "It reads the output that came back."
4. **Respond** — "It now answers the user with grounded information."

That four-step cycle is the entire idea of an agent. Everything else in this course is variations on it.

---

## Question to throw at the class
> "What's the difference between an agent that runs `ls` and a script that runs `ls`?"

(Expected: the agent **chose** to run `ls`; nobody told it which command. That's the LLM-driven decision-making.)

---

## Common pitfalls / things to flag
- Don't go deep on prompt engineering yet — that's a later demo.
- If the agent asks for permission to run `ls`, **approve it** and tell pupils that permission prompts are a safety feature; we'll see them throughout.
- Resist showing fancy stuff. The point of this demo is the *contrast* between chat and agent.
