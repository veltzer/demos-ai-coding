# Demo 09 — Multi-Agent Orchestration: A Real Workflow

## Goal of this demo
Bring everything together. An **orchestrator** agent coordinates **specialist** subagents (researcher, coder, reviewer) to deliver an end-to-end result. This is what real agentic systems look like, and it's the capstone of the course.

**Estimated time:** 25–30 minutes
**Complexity:** Highest. Combines tools + plans + subagents + review.

---

## What pupils should walk away with
- Real agent systems are usually **a graph of agents**, each with a role.
- Orchestration ≠ doing the work. The orchestrator's job is to *route*, not produce.
- Specialization beats generalism: a "reviewer" agent does a better review than the same agent that wrote the code.
- The pattern (research → build → review → fix) generalizes far beyond coding.

---

## Setup before class
1. Empty directory:

   ```bash
   mkdir /tmp/demo09 && cd /tmp/demo09
   ```

2. Launch the agent in `/tmp/demo09`.
3. **Have a printed copy of the architecture diagram below on screen** before you start. Pupils need a mental map.

---

## The architecture you'll demo

```text
                 +---------------------+
                 |    ORCHESTRATOR     |
                 |  (main agent)       |
                 +----------+----------+
                            |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
+--------------+    +---------------+    +--------------+
|  RESEARCHER  |    |     CODER     |    |   REVIEWER   |
| (subagent)   |    |  (subagent)   |    | (subagent)   |
| reads docs,  |    | writes code   |    | audits code  |
| picks lib    |    | based on plan |    | for problems |
+--------------+    +---------------+    +--------------+
```

The orchestrator never writes code itself. It just **dispatches** and **integrates**.

---

## Live script

### Step 1 — Set the scene (3 min)
Tell the class:

> "We're going to build a small command-line tool that converts a JSON file into a CSV file. Sounds easy. Let's do it the *grown-up* way: research a good library first, then write the code, then have someone independent review it."

> "I'll do all three with one agent, but the agent is going to delegate to specialists for each phase. I (the human) am going to act like a project manager who only talks to the orchestrator."

### Step 2 — Kick off with an explicit orchestration request (4 min)
Type:

```txt
I want to build a small Python CLI that converts a JSON file (an array of
objects) into a CSV file. Same column for every key.

Run this as an orchestrated workflow:

1. Spawn a RESEARCHER subagent. Its job: pick the best Python library for
   this (or argue for stdlib). Return a one-paragraph recommendation with
   reasons.

2. Based on the researcher's answer, spawn a CODER subagent. Its job:
   write json2csv.py implementing the tool, plus a small example.json so
   we can test it. Return the file paths it created.

3. Spawn a REVIEWER subagent. Its job: read json2csv.py and find issues —
   bugs, edge cases, missing error handling. Return a bulleted list.

4. If the reviewer finds issues, spawn the CODER again with the issues
   and ask it to fix them.

5. Report back to me with the final files and a summary of what each
   subagent contributed.
```

This prompt is doing a lot. Read it carefully on screen with the class before sending.

### Step 3 — Watch each phase (10 min)
Narrate as it runs:

**Researcher phase:**
- "Researcher is spawning. It will probably WebFetch or read its training knowledge."
- When it returns: read the recommendation aloud. Maybe it picked stdlib `csv` + `json`. Maybe it picked `pandas`. Discuss with the class whether you agree.

**Coder phase:**
- "Coder is spawning, with the recommendation as input."
- When it finishes, open `json2csv.py` together. Run it on the example:

  ```bash
  python json2csv.py example.json out.csv
  cat out.csv
  ```

**Reviewer phase:**
- "Reviewer is spawning. It hasn't seen the researcher or the coder — fresh eyes."
- Read its findings. Common ones: "doesn't handle nested objects", "no UTF-8 BOM option", "crashes on empty array", "no help text on `-h`".

**Fix phase:**
- The orchestrator re-spawns the coder with the issue list.
- The fixes appear in `json2csv.py`.

### Step 4 — Make the architecture visible (3 min)
Point at the diagram. Trace the actual flow that just happened:

> "The orchestrator made four delegations. It never wrote a line of code itself. It never read PyPI itself. Its job was *routing and integration*."

> "The researcher knew nothing about coding standards. The coder knew nothing about reviewing. The reviewer knew nothing about library selection. Each one had a clean job."

### Step 5 — The big lesson (3 min)
Step back. This is the closing message of the entire course:

> "An agent is an LLM with tools and a loop."
> "A multi-agent system is **agents giving each other jobs.**"
> "And just like with humans: clear roles, clear handoffs, and someone in charge of integration. That's the whole game."

> "What we just built is a tiny version of how real agentic products work — code review bots, research assistants, customer-support pipelines. Same shape. More agents. More tools. Same loop."

### Step 6 — Open the floor (5 min+)
Ask pupils to design their own multi-agent workflow on paper for **5 minutes**, for any task they want — onboarding a new hire, planning a trip, writing a blog post, triaging bugs. Have a few share. Sketch their graphs on the board.

---

## Question to throw at the class
> "What goes wrong if the orchestrator and the workers are the *same* agent on the same prompt?"

(Expected: no specialization, context bloats, the 'reviewer' is biased toward the code 'they' wrote, no parallelism. This is why specialists matter — even when they're all the same model under the hood.)

---

## Common pitfalls / things to flag
- This demo will take longer than you think. Budget the full 30 minutes.
- If a subagent wanders off, **stop it and remind the orchestrator** of the role boundaries. The orchestrator can correct mid-flight.
- Don't try to add a fourth or fifth specialist on the live stage. Three is enough to make the point. More is showing off and increases failure modes.
- **End on the meta-point**, not on a code listing. Pupils came to learn about agents — make sure they leave thinking about the architecture, not the JSON-to-CSV tool.
