# Demo 01 — An Agent With One Tool

## Goal of this demo
Show the agent **using a single, specific tool** to answer a question that requires looking at real data. Slow it down so pupils can see one tool call clearly.

**Estimated time:** 7–10 minutes
**Complexity:** Very simple. One file read.

---

## What pupils should walk away with
- A tool is a function the model can call. The model picks the tool and the arguments.
- The tool returns data; the model then writes a natural-language answer based on the data.
- The model does not "magically know" — it had to look.

---

## Setup before class
1. Create a small text file the pupils will recognize. For example:

   ```bash
   mkdir /tmp/demo01 && cd /tmp/demo01
   cat > shopping-list.txt <<EOF
   - 2 kg apples
   - 1 loaf of bread
   - milk (3 cartons)
   - eggs (12)
   - dark chocolate (the good kind)
   EOF
   ```

2. Launch the agent in `/tmp/demo01`.

---

## Live script

### Step 1 — Ask a question that needs the file (2 min)
Type to the agent:

```txt
How many cartons of milk are on my shopping list?
```

The agent will use the **Read** tool (or `cat` via Bash) on `shopping-list.txt` and answer "3".

**Pause and ask the class:**
> "How did it know which file to read? I never told it the filename."

(Answer: it probably used `ls` first, or noticed only one `.txt` file exists. Highlight that the agent **explored** before acting.)

### Step 2 — Ask something that requires reasoning over the file (3 min)
```txt
Which item on the list is the most subjective? Explain.
```

The agent should pick "dark chocolate (the good kind)" — because *"the good kind"* is subjective. This shows pupils that:
- The tool gave it raw text.
- The **LLM**, not the tool, did the reasoning.

### Step 3 — Show the boundary (2 min)
Ask something the file **cannot** answer:

```txt
What did I buy last week?
```

The agent should say it doesn't know — there's no data about last week. Use this to make the point:

> "An agent is only as informed as the tools you give it. No tool for last week's purchases → no answer."

---

## Question to throw at the class
> "If I want the agent to answer 'what did I buy last week?', what would I have to give it?"

(Expected answers: a history file, a database tool, access to a receipts folder. This sets up the next demos.)

---

## Common pitfalls / things to flag
- If the agent guesses without reading the file, **call it out** and say "this is hallucination — we want grounded answers." Then re-ask, instructing it to read the file first.
- Don't add extra files to the directory. One file = one obvious choice = clean demo.
