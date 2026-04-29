# Demo 04 — Planning a Multi-Step Task

## Goal of this demo
Show that for non-trivial work, an agent doesn't just dive in — it **plans first**, then executes. Make pupils see the difference between "do everything at once" and "lay out the steps, then walk them."

**Estimated time:** 12–15 minutes
**Complexity:** Moderate. The work itself is small; the *planning* is the lesson.

---

## What pupils should walk away with
- For complex tasks, ask the agent to plan before acting.
- A good plan is a tool: it forces clarity, lets you correct course early, and produces better final work.
- Many agents (including Claude Code) have an explicit **Plan Mode** for exactly this.

---

## Setup before class
1. Empty directory:

   ```bash
   mkdir /tmp/demo04 && cd /tmp/demo04
   ```

2. Launch the agent in `/tmp/demo04`.

---

## Live script

### Step 1 — Anti-pattern: vague request, no plan (3 min)
Type a deliberately under-specified request:

```txt
Build me a small Python tool to manage a TODO list.
```

Let the agent start producing code. After ~30 seconds, **stop it** (or let it finish a tiny version) and ask the class:

> "Did anyone ask: store where? CLI or web? What commands? Single user or many?"

The point: vague request → the agent guessed. The result might be okay but it's not *yours*.

### Step 2 — Same task, but plan first (5 min)
Reset to a clean directory. Type:

```txt
I want to build a small Python TODO tool. Before writing any code, give me
a plan: what files you'll create, what commands the user will type, and
where the data will be stored. Wait for my approval.
```

The agent will produce a plan: e.g.,
- `todo.py` CLI with `add`, `list`, `done`, `remove`.
- Data stored in `~/.todo.json`.
- Uses argparse, no external deps.

**Talk through the plan with the class.** Pretend you're the customer:
- "I don't want it in my home dir, put it next to the script."
- "Skip `remove` — I don't need it."

Tell the agent the changes:

```txt
Two changes: store the data in todo.json next to the script, and skip the
remove command. Then go ahead.
```

### Step 3 — Watch it execute the *agreed* plan (4 min)
Now it will write the code matching the corrected plan. **Pupils see:**
- Files created exactly as planned.
- No surprise scope creep.
- A working tool that fits the spec.

Run it together:

```bash
python todo.py add "buy milk"
python todo.py list
python todo.py done 1
python todo.py list
```

### Step 4 — Make the meta-point (2 min)
> "The first version was the agent's idea. The second version was *our* idea, executed by the agent. That's the difference. Plans turn the agent into a builder, not a designer."

---

## Question to throw at the class
> "When is planning *not* worth it? When should I just let the agent dive in?"

(Expected: trivial tasks, throwaway scripts, when you genuinely don't care. Planning has a cost — use it when the cost of a wrong direction is high.)

---

## Common pitfalls / things to flag
- If the agent skips the plan and starts coding anyway, interrupt it. Re-emphasize: "plan first, code after I approve."
- Don't let the plan get too long. A plan should fit on one screen. If the agent writes a 5-page plan, ask it to compress.
- The point of the plan is the *conversation* about it, not the plan itself. Use it.
