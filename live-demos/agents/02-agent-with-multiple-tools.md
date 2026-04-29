# Demo 02 — An Agent With Multiple Tools

## Goal of this demo
Show the agent **choosing between tools** and **chaining them**: read something, transform it, write the result. This is the first demo where the agent does real work end-to-end.

**Estimated time:** 10 minutes
**Complexity:** Easy. Read → think → write.

---

## What pupils should walk away with
- The agent picks tools dynamically — Read for input, Write for output.
- Multiple tool calls in one turn is normal; that's the loop running multiple times.
- The agent's "thinking" connects the tools together.

---

## Setup before class
1. Create a small CSV file:

   ```bash
   mkdir /tmp/demo02 && cd /tmp/demo02
   cat > scores.csv <<EOF
   name,score
   Alice,87
   Bob,42
   Carol,95
   Dave,61
   Eve,73
   EOF
   ```

2. Launch the agent in `/tmp/demo02`.

---

## Live script

### Step 1 — A task that requires multiple tools (4 min)
Type:

```txt
Read scores.csv. Sort the people from highest to lowest score, and write the
result into a file called ranked.md as a markdown numbered list.
```

While it works, **narrate** to the class what each tool call does as it happens:
- "It's reading scores.csv now → that's the **Read** tool."
- "It's writing ranked.md now → that's the **Write** tool."
- "Notice it didn't ask me anything in between — it figured out the steps."

### Step 2 — Verify together (2 min)
Open `ranked.md` in the editor (or `cat` it). Pupils should see:

```markdown
1. Carol — 95
2. Alice — 87
3. Eve — 73
4. Dave — 61
5. Bob — 42
```

**Make the point:**
> "The sorting wasn't done by a tool. The Read gave it data, the Write put data on disk. The **sorting happened in the model's head.**"

### Step 3 — A small variation to show flexibility (3 min)
Without resetting, ask:

```txt
Now also create a file called bottom-three.txt with just the names of the
three lowest scorers, one per line.
```

The agent will reuse what it already knows (it remembers the data from earlier in the conversation) and just call **Write** — no second Read needed. That's worth pointing out:

> "It didn't re-read the file. The conversation has memory; the agent reuses what it already saw."

---

## Question to throw at the class
> "What would happen if I asked it to sort 1 million rows? Would it still do the sort 'in its head'?"

(Expected: at some point you want the agent to *call a sort tool* — e.g., run `sort` via Bash — instead of doing it itself. That's a great teaser for tool design.)

---

## Common pitfalls / things to flag
- If the agent decides to `cat` and `sort` via Bash instead of doing it in the model's head, **that's also fine** — point out it made a different choice and both are valid.
- Don't overload the demo with a giant file. Five rows is enough; pupils need to see the whole thing on screen.
