# Writing a Skill for an AI Assistant

## Learning Objective

Learn how to author a **Skill** — a reusable, self-contained packet of
instructions (and optionally scripts and resources) that an AI assistant such as
Claude Code can discover and invoke on demand. By the end of this exercise you
will understand what a skill is, how the AI decides when to use one, and you will
have written, tested, and iterated on a working skill of your own.

## Why Skills Matter

Out of the box an AI coding assistant is a generalist. Skills let you teach it a
*specific, repeatable procedure* once and have it apply that procedure
consistently every time it is relevant:

- **Reusability**: Encode a workflow once, trigger it any number of times.
- **Consistency**: The same steps run the same way regardless of how the request
  is phrased.
- **Progressive disclosure**: The assistant only loads the skill's full
  instructions when it is actually needed, keeping the context window lean.
- **Shareability**: A skill is just files, so it can be committed to a repo and
  shared across a team.
- **Composability**: Skills can call scripts, reference templates, and build on
  other skills.

A skill is different from a one-off prompt: a prompt is consumed and gone, while
a skill is a durable capability the assistant carries between conversations.

## Prerequisites

- An AI assistant that supports skills (e.g. Claude Code).
- Basic familiarity with Markdown and YAML frontmatter.
- A terminal and a text editor.

---

## Part 1: Anatomy of a Skill

A skill lives in its own directory. The minimum is a single file named
`SKILL.md`. More elaborate skills add scripts and reference material alongside it:

```
my-skill/
├── SKILL.md            # required: frontmatter + instructions
├── scripts/            # optional: helper scripts the skill can run
│   └── do_thing.sh
└── references/         # optional: templates, examples, docs
    └── template.md
```

### The `SKILL.md` file

Every `SKILL.md` begins with YAML frontmatter followed by the instruction body:

```markdown
---
name: commit-helper
description: >
  Write a well-structured git commit message for the currently staged changes,
  following Conventional Commits. Use when the user asks to commit, write a
  commit message, or save their work to git.
---

# Commit Helper

When invoked, do the following:

1. Run `git diff --cached` to inspect the staged changes. If nothing is staged,
   tell the user and stop.
2. Determine the change type (feat, fix, docs, refactor, test, chore).
3. Write a commit message with:
   - a concise subject line (≤ 50 chars) in the form `type(scope): summary`
   - a blank line
   - a body explaining *what* changed and *why*, wrapped at 72 columns
4. Show the proposed message to the user and ask for confirmation before
   running `git commit`.
```

### The two fields that matter most

- **`name`**: a short, kebab-case identifier. This is how the skill is invoked.
- **`description`**: the single most important field. The assistant reads *only*
  the description to decide whether a skill is relevant to the current request.
  A vague description means the skill never fires; a precise one — including the
  **trigger conditions** ("Use when…") — means it fires exactly when intended.

> **Rule of thumb:** Write the `description` for the *router*, and the body for
> the *worker*. The description sells the skill; the body executes it.

---

## Part 2: Write Your First Skill

You will write a skill that generates a Markdown changelog entry from recent git
history.

### Exercise 2.1: Scaffold the skill

Create the directory and file:

```bash
mkdir -p changelog-entry
$EDITOR changelog-entry/SKILL.md
```

### Exercise 2.2: Write the frontmatter

Fill in the frontmatter. Think hard about the `description` — list the phrasings
a user might actually use.

```markdown
---
name: changelog-entry
description: >
  Generate a Markdown changelog entry summarizing recent commits. Use when the
  user asks to update the changelog, write release notes, or summarize what
  changed since the last tag/release.
---
```

### Exercise 2.3: Write the instruction body

Give the assistant an unambiguous, numbered procedure. Be explicit about inputs,
outputs, and edge cases:

```markdown
# Changelog Entry

1. Find the most recent git tag with `git describe --tags --abbrev=0`. If there
   are no tags, use the first commit instead.
2. Collect commits since that point with
   `git log <ref>..HEAD --pretty=format:'%s'`.
3. Group the commit subjects under these headings, omitting any empty group:
   - **Added** (feat)
   - **Fixed** (fix)
   - **Changed** (refactor, perf)
   - **Other**
4. Produce a Markdown block like:

   ## [Unreleased] - YYYY-MM-DD

   ### Added
   - ...

5. Show the result. Do NOT edit any file unless the user asks you to insert it
   into `CHANGELOG.md`.
```

---

## Part 3: Test and Iterate

A skill is only as good as its triggering and its output. Test both.

### Exercise 3.1: Does it trigger?

Make the skill available to your assistant (for Claude Code, place the directory
under `.claude/skills/` in your project, or your user-level skills directory).
Then, in a fresh conversation, try phrasings that *should* trigger it and some
that should *not*:

| Prompt                                          | Should trigger? |
| ----------------------------------------------- | --------------- |
| "Write release notes for the latest changes"    | ✅ yes          |
| "Update the changelog"                          | ✅ yes          |
| "What does this function do?"                   | ❌ no           |
| "Summarize what changed since the last release" | ✅ yes          |

If a "yes" row fails to trigger, your `description` is too narrow — add the
missing phrasing. If a "no" row triggers, your description is too broad —
tighten it.

### Exercise 3.2: Is the output right?

Run the skill on a real repository. Check that it:

- handles the no-tags edge case you specified,
- groups commits correctly,
- does **not** modify files it was told to leave alone.

Refine the body until the behavior is reliable across a few different repos.

---

## Part 4: Add a Helper Script (Optional but Recommended)

Skills become far more powerful when they can run deterministic code instead of
asking the assistant to do fiddly text manipulation by hand.

### Exercise 4.1: Extract logic into a script

Create `changelog-entry/scripts/collect.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ref="$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)"
git log "${ref}..HEAD" --pretty=format:'%s'
```

Then update the body of `SKILL.md` to call it:

```markdown
1. Run `bash scripts/collect.sh` to get the list of commit subjects.
2. Group and format them as described below.
```

This makes the data-gathering step reliable and keeps the assistant focused on
the part it is genuinely good at: summarizing and formatting.

---

## Part 5: Principles of a Good Skill

Use these as a checklist when reviewing your own skills:

1. **One job.** A skill should do one thing well. If it has an "and" in its
   purpose, consider splitting it.
2. **A description that routes.** State *what it does* and *when to use it*,
   using the words real users would use.
3. **An imperative, numbered body.** Tell the assistant exactly what to do, in
   order, including how to handle the empty/error cases.
4. **Specify side effects.** Be explicit about what the skill is and is *not*
   allowed to change. Default to read-only and ask before writing.
5. **Push determinism into scripts.** Anything that can be a script probably
   should be — it is more reliable than free-form generation.
6. **Keep it lean.** Long bodies cost context and dilute focus. Move detail into
   `references/` files the skill can read on demand.

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Explain what a skill is and how it differs from a plain prompt.
- [ ] Describe the role of the `name` and `description` frontmatter fields.
- [ ] Write a `SKILL.md` with precise trigger conditions and an imperative body.
- [ ] Verify a skill triggers on the right prompts and not the wrong ones.
- [ ] Specify and respect a skill's allowed side effects.
- [ ] Extract deterministic work into a helper script the skill invokes.
- [ ] Critique a skill against the principles in Part 5.

## Stretch Goals

- Write a skill that **composes** with another (calls it as a sub-step).
- Add a `references/template.md` and have the skill read it on demand instead of
  inlining the template.
- Write a "meta" skill: a skill whose job is to help you *write other skills*,
  enforcing the checklist from Part 5.
- Share your skill with a teammate and watch where it triggers unexpectedly —
  real usage is the best test of a `description`.

## Real-World Applications

1. **Team conventions**: Encode your org's commit, PR, or review standards once.
2. **Onboarding**: A skill that scaffolds a new service the team's way.
3. **Repetitive analysis**: Standard security audits, dependency reviews, or
   release checklists.
4. **Domain procedures**: Wrap a complex internal workflow so anyone can invoke
   it correctly.

Remember: a great skill turns a vague request into a reliable, repeatable
procedure — the assistant stops improvising and starts executing.
