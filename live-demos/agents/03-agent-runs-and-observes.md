# Demo 03 — Run, Fail, React

## Goal of this demo
Show the **observe** part of the loop. The agent runs a command, sees the output, **and changes its plan based on what came back**. This is the moment pupils realize agents are not scripts.

**Estimated time:** 10–12 minutes
**Complexity:** Moderate. The interesting bit is the failure → recovery.

---

## What pupils should walk away with
- Agents react to tool output. They don't just execute a fixed plan.
- A failing command is **information**, not a dead end. The agent reads the error and tries something else.
- This is what makes an agent feel "alive" compared to a script.

---

## Setup before class
1. Create a project that has a deliberate problem:

   ```bash
   mkdir /tmp/demo03 && cd /tmp/demo03
   cat > greet.py <<'EOF'
   import sys

   def greet(name):
       print(f"Hello, {name.upper()!}")  # SyntaxError: stray !

   if __name__ == "__main__":
       greet(sys.argv[1])
   EOF
   ```

   The `{name.upper()!}` has an extra `!` inside the f-string — Python will refuse to parse it.

2. Launch the agent in `/tmp/demo03`.

---

## Live script

### Step 1 — Ask the agent to run it (2 min)
Type:

```txt
Run greet.py with the argument "world" and tell me what it prints.
```

The agent will run something like `python greet.py world` and see a `SyntaxError`. **Stop here and ask the class:**

> "What would a normal script do right now?"

(Answer: crash, exit with the error.)

> "What's the agent going to do?"

### Step 2 — Watch it react (3 min)
The agent will almost certainly:
1. Read the file.
2. Notice the stray `!` in the f-string.
3. Edit the file to fix it.
4. Re-run the command.
5. Report "Hello, WORLD".

**Narrate as it happens.** Especially highlight the moment it goes from *"the run failed"* to *"let me look at the source"*. That decision is the agent.

### Step 3 — Try a harder failure (4 min)
Without resetting, ask:

```txt
Now make greet.py also work without an argument — print "Hello, stranger" if
no name is given. Run it both ways to confirm.
```

Watch the agent:
1. Edit the file.
2. Run with an argument → success.
3. Run without an argument → success.
4. Report both outputs.

**Make the point:**
> "It tested its own work. It didn't just write code and hope. The 'observe' step matters as much as the 'act' step."

---

## Question to throw at the class
> "What if the error message had been misleading? What if Python had said 'permission denied' when actually the bug was in the source code?"

(Expected: the agent might have gone down a wrong path. Good agents are still fooled by bad error messages — same as humans. This is honest framing.)

---

## Common pitfalls / things to flag
- If the agent asks permission to run `python`, **approve it**. Don't break the flow.
- If the agent fixes the bug and forgets to verify by re-running, prompt it: "did you actually run it?" — this is also a teachable moment.
- Resist explaining the bug to the agent. Let it discover. The discovery **is** the demo.
