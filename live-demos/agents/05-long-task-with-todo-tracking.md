# Demo 05 — Long Tasks and Todo Tracking

## Goal of this demo
Show what happens when a task has **many steps that take real time**. The agent breaks the work into a checklist, marks items done as it goes, and you (the human) can see progress. This is how agents avoid getting lost on long jobs.

**Estimated time:** 15 minutes
**Complexity:** Moderate–high. Pupils start to see the shape of real work.

---

## What pupils should walk away with
- For multi-step work, the agent maintains a **todo list** internally.
- Each item is started → completed in order, visibly.
- This isn't decoration — it's how the agent stays on track without losing items.

---

## Setup before class
1. A small Python project that needs work:

   ```bash
   mkdir /tmp/demo05 && cd /tmp/demo05

   cat > calc.py <<'EOF'
   def add(a, b):
       return a + b

   def subtract(a, b):
       return a - b

   def multiply(a, b):
       return a * b

   def divide(a, b):
       return a / b
   EOF
   ```

2. Launch the agent in `/tmp/demo05`.

---

## Live script

### Step 1 — Give a task with many obvious sub-tasks (3 min)
Type:

```txt
Improve calc.py: add type hints, add docstrings, handle division by zero,
write a tests/ folder with pytest tests covering every function including
edge cases, add a README.md explaining how to use the module, and a
Makefile with `make test` and `make lint`. Use a todo list to track your
progress.
```

The agent will respond by **creating a checklist** of about 6–8 items.
Read it out loud to the class. Items will look something like:
- Add type hints to calc.py
- Add docstrings to each function
- Handle division by zero
- Create tests/ with pytest tests
- Write README.md
- Add Makefile with test and lint targets

### Step 2 — Watch items flip from pending → in_progress → completed (8 min)
This is the heart of the demo. As the agent works, the list updates live. **Narrate the rhythm:**

- "It just marked 'add type hints' as in-progress."
- "It edited calc.py, marked that one done, moved to the next."
- "Notice — it's not skipping ahead. One thing at a time."

**Halfway through**, ask the class:

> "If I closed this terminal right now and reopened it, would the agent know what was already done?"

(Answer: kind of — it would see the files on disk. The todo list itself is in the conversation context. This is a good moment to mention that **state lives in the workspace**, not in the agent's head.)

### Step 3 — Verify the result (3 min)
Open the new files and walk through them:
- `calc.py` — type-hinted, docstrings, raises on divide-by-zero.
- `tests/test_calc.py` — has tests for each function and the error case.
- `README.md` — usage examples.
- `Makefile` — `make test` and `make lint` targets.

Run together:

```bash
make test
```

If pytest isn't installed, the test run will fail — which is itself a great teaching moment about the agent's environment vs. yours.

---

## Question to throw at the class
> "Why a todo list? Why not just remember it all?"

(Expected: long tasks → easy to lose track, easy to miss an item, easy for an interruption to derail. The list is **external memory** for the agent and a **status display** for you.)

---

## Common pitfalls / things to flag
- If the agent tries to do everything in one giant edit without a todo list, **stop it** and ask: "give me the todo list first." Today's lesson is the list itself.
- Don't make the task too small. If there are only 2 sub-tasks, the list is pointless. 6+ items is the sweet spot.
- Resist micromanaging mid-execution. Let pupils see uninterrupted progress so the rhythm is clear.
