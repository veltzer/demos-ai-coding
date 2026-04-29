# Demo 06 — Reaching Outside: Web and External Data

## Goal of this demo
So far the agent has only touched the local machine. Now show it **reaching out to the world** — fetching a web page, checking real-time information, grounding its answer in something fresh. This is where the agent stops being a closed box.

**Estimated time:** 12 minutes
**Complexity:** Moderate. The new idea is "tool returns network data."

---

## What pupils should walk away with
- The agent can be given tools that hit the network (WebFetch, WebSearch, HTTP).
- "Real-time" answers are real, not from training data.
- The same loop applies — think → call tool → observe → answer.

---

## Setup before class
1. Pick **one** stable, public URL with content that's clearly more recent than the model's training cutoff. Good choices:
   - The latest Python release notes page.
   - A library's GitHub releases page.
   - Today's weather (if you have a public weather API set up).
2. Launch the agent in any directory.
3. **Test the network tool yourself** before class — nothing kills a demo like firewall blocks discovered live.

---

## Live script

### Step 1 — Show the limit (2 min)
Without using any tool, ask:

```txt
What is the latest stable version of Python, as of right now?
```

The agent will answer based on training data — and will usually **flag** that it's not real-time. This is honest behavior; point it out:

> "It told us 'as of my training data.' That's the polite way of saying 'I'm guessing'."

### Step 2 — Same question, with permission to fetch (4 min)
Now ask:

```txt
Use the web to find the actual latest stable version of Python right now,
from python.org. Tell me the version and the release date.
```

The agent will use **WebFetch** (or WebSearch). Watch:
1. It picks a URL — likely `https://www.python.org/downloads/`.
2. It fetches the page.
3. It extracts the version and date from the HTML.
4. It answers, **citing the URL it used.**

**Make the point:**
> "Now it didn't guess. It went and looked. The answer is grounded in something we can verify."

### Step 3 — Show the failure mode (3 min)
Ask something only available behind a login or paywall:

```txt
Fetch my private Gmail inbox and tell me how many unread mails I have.
```

The agent will refuse or fail — no credentials, no access. Use this to make the point:

> "Web access ≠ omniscience. The agent only sees what the tool can see. Public pages, yes. Your authenticated accounts, no — unless you give it a tool that has those credentials."

### Step 4 — Combine local and web (3 min)
Bring the two worlds together:

```txt
Read requirements.txt in this directory, then check on PyPI which of these
packages have a newer version available. Write the upgrade list to
upgrades.md.
```

(Make sure you have a `requirements.txt` in the working directory with 2–3 packages, e.g., `requests==2.20.0`.)

The agent will:
1. **Read** requirements.txt (local tool).
2. **WebFetch** PyPI for each package (network tool).
3. **Write** upgrades.md (local tool).

**This is the punchline:** real agents stitch local and remote tools into one workflow.

---

## Question to throw at the class
> "If the agent fetches a webpage, can the webpage tell the agent to do something bad?"

(Expected: yes — this is **prompt injection**. Web content is *untrusted input*. Mention it briefly; it's a topic worth its own session.)

---

## Common pitfalls / things to flag
- **Test the URL before class.** If python.org is having a bad day or your network blocks it, the demo dies.
- If the agent tries to use search instead of fetch (or vice versa), let it — both are valid. Just narrate which it picked.
- Keep the requirements.txt small (2–3 lines). Big lists make the demo drag.
