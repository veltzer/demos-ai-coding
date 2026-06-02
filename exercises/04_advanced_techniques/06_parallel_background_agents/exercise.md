# Launching Agents in Parallel in the Background

## Learning Objective

Learn how to make an AI assistant such as Claude Code do more work in less
wall-clock time by **launching subagents that run in parallel and in the
background**. By the end of this exercise you will understand when parallelism
helps (and when it hurts), how to decompose a task into independent units of
work, how to fan out subagents concurrently, and how to collect and reconcile
their results.

## Why Parallel Background Agents Matter

A single agent works sequentially: it reads one file, then the next, then
reasons, then acts. For many tasks that is fine. But some tasks are
*embarrassingly parallel* — they break cleanly into independent pieces that have
no dependency on one another. For those, running pieces concurrently is a large
win:

- **Speed**: Ten independent searches finish in roughly the time of the slowest
  one, not the sum of all ten.
- **Context isolation**: Each subagent gets its own fresh context window, so one
  agent reading a huge file does not pollute the others' context.
- **Specialization**: Different subagents can be given different roles, models,
  or instructions for the same task (e.g. three reviewers each with a distinct
  lens).
- **Throughput on long jobs**: Background agents keep working while you continue
  the conversation; you are notified when they finish.

The flip side — and the thing this exercise will teach you to judge — is that
parallelism only pays off when the work is **genuinely independent**. Forcing
parallelism onto dependent steps creates races, duplicated effort, and confusion.

## Prerequisites

- An AI assistant that supports subagents / background tasks (e.g. Claude Code,
  which exposes an `Agent` tool and background execution).
- A medium-to-large code repository to experiment on.
- Completion of `05_writing_a_skill` is helpful but not required.

---

## Part 1: When to Parallelize (and When Not To)

Before launching anything, classify the work. Ask: **does step B need the result
of step A?**

| Work shape                                          | Parallel? |
| --------------------------------------------------- | --------- |
| Search 8 directories for the same pattern           | ✅ yes     |
| Summarize 5 unrelated modules                       | ✅ yes     |
| Review a diff from 4 independent angles             | ✅ yes     |
| Refactor a function, then update its callers        | ❌ no — sequential |
| Read a file, then edit it based on what you read    | ❌ no — sequential |
| Run migrations that must apply in order             | ❌ no — sequential |

### The golden rule

> **Fan out only over independent work. The moment one unit needs another's
> output, that boundary becomes a barrier — finish the first wave before
> starting the next.**

### Exercise 1.1: Classify your task

Take a real task you would give your assistant ("audit this service",
"document every public API", "find all the places we call the old auth
function"). Write down:

1. The independent units of work it decomposes into.
2. Any dependencies between them (these become *barriers*).
3. What each unit should *return* so the results can be combined.

If you cannot list at least three independent units, the task is probably better
done sequentially — stop here for that task and pick another.

---

## Part 2: Fan Out a Parallel Search

The simplest, safest parallel pattern is a **read-only fan-out**: many subagents
search or read, none of them write.

### Exercise 2.1: Launch several agents at once

Ask your assistant to investigate several independent questions about the
codebase *in a single request*, so it launches them concurrently rather than one
after another. For example:

```txt
In parallel, launch one subagent for each of these and report back:
1. Where is authentication enforced? List the files and the mechanism.
2. What database(s) does this project use and where are they configured?
3. What is the test framework and how are tests run?
4. List every external HTTP API this project calls.
```

> **Key point:** To get true concurrency, the independent agents must be
> launched *in the same turn*. If you ask for them one message at a time, they
> run sequentially.

### Exercise 2.2: Observe the difference

Run the same four questions two ways and compare wall-clock time:

- **Sequential**: ask them one at a time, waiting for each answer.
- **Parallel**: ask for all four at once with an explicit "in parallel"
  instruction.

Note how the parallel run finishes in roughly the time of the *slowest* question
rather than the sum of all four.

### Exercise 2.3: Reason about what comes back

Each subagent returns only its *final summary* — not its full transcript. That
means:

- You must tell each agent **what to return** ("list file:line for each match").
- The main agent then **reconciles** the summaries into one answer.

Try a fan-out where the results overlap (e.g. two agents that might both find the
same file) and watch how the results get de-duplicated when combined.

---

## Part 3: Specialized Agents on the Same Target

Parallelism is not only about covering more ground — it is also about getting
**independent perspectives** on the *same* thing.

### Exercise 3.1: A panel of reviewers

Ask your assistant to review the current diff with three subagents launched in
parallel, each with a distinct lens:

```txt
Review the current git diff with three subagents in parallel:
- Agent A: correctness bugs and logic errors only.
- Agent B: security issues only (injection, authz, secrets).
- Agent C: readability and naming only.
Then merge their findings, removing duplicates, into one prioritized list.
```

### Exercise 3.2: Adversarial verification

A powerful pattern: after findings come back, launch a *second* wave of agents
whose job is to **try to refute** each finding. Only findings that survive
skeptical review make the final list. Notice that this is a **barrier**: the
verify wave cannot start until the find wave has produced findings.

```txt
For each issue the reviewers found, launch a subagent that tries to prove the
issue is NOT real. Keep only the issues that survive.
```

---

## Part 4: Background (Asynchronous) Agents

Some work takes minutes, not seconds — a broad migration, a large audit, a build.
For these, run the agent **in the background** so you are not blocked.

### Exercise 4.1: Kick off a long job in the background

Ask your assistant to start a long-running investigation as a background task and
to continue the conversation meanwhile:

```txt
Start a background agent that maps every public function in src/, its file,
and a one-line description. While it runs, help me with something else.
```

You will be **notified when it completes**, and its result is returned to the
main agent for you to use. Practice:

- launching the job,
- doing other work while it runs,
- collecting and using the result once you are notified.

### Exercise 4.2: Several background jobs at once

Launch two or three independent background jobs in the same turn (e.g. "audit
dependencies", "find dead code", "list TODOs with owners"). Observe that they all
progress concurrently and each notifies you on completion.

---

## Part 5: Isolation for Agents That Write

Read-only fan-out is safe. The moment subagents **modify files** in parallel,
they can clobber each other. The solution is **isolation** — give each writing
agent its own working copy (for Claude Code, a git *worktree*).

### Exercise 5.1: Parallel edits without conflicts

Pick a mechanical change that applies independently to several files (e.g. "add a
license header to each file in `src/`"). Ask for one isolated subagent per file
so they cannot conflict:

```txt
Add the standard license header to each file in src/. Use one isolated
(worktree) subagent per file so parallel writes do not conflict, then bring the
changes together.
```

> **Cost note:** Isolation is not free — each worktree costs setup time and disk.
> Use it *only* when agents genuinely write in parallel. For read-only work,
> never use it.

---

## Part 6: Pitfalls and Principles

Use these as a checklist when designing a parallel run:

1. **Independence first.** Only fan out over work with no cross-dependencies. A
   dependency is a barrier, not a parallel boundary.
2. **Launch in one turn.** Concurrency happens only when the agents are started
   together; serial requests run serially.
3. **Tell each agent what to return.** Subagents hand back a summary, not their
   transcript — specify the exact shape you need so results can be merged.
4. **Reconcile explicitly.** De-duplicate and resolve conflicts between agent
   results in the combining step.
5. **Barrier when results must be combined.** If the next wave needs *all* prior
   results (dedup, "0 found → skip"), wait for the whole wave before continuing.
6. **Isolate writers, never readers.** Parallel writes need isolation; parallel
   reads must not pay for it.
7. **Background the slow, foreground the fast.** Use background agents for
   minutes-long work; keep quick fan-outs in the foreground.
8. **Watch the cost.** More agents means more tokens. Scale the fleet to the
   task, not to the maximum possible.

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Decide whether a task is parallelizable by testing for independence.
- [ ] Decompose a task into independent units and identify the barriers.
- [ ] Launch multiple subagents concurrently in a single request.
- [ ] Specify what each subagent must return so results can be merged.
- [ ] Reconcile and de-duplicate results from a fan-out.
- [ ] Use a panel of specialized agents and an adversarial verification wave.
- [ ] Run long jobs as background agents and collect their results.
- [ ] Isolate parallel writers to avoid conflicts, and know when not to.

## Stretch Goals

- Build a **find → verify → synthesize** pipeline: a wave that finds issues, a
  wave that refutes them, and a final agent that writes the report.
- Implement a **loop-until-dry** discovery: keep launching finder agents until two
  consecutive waves surface nothing new.
- Run a **tournament**: generate N independent solutions to a design problem in
  parallel, score them with judge agents, and synthesize the winner.
- Measure it: time the same task sequentially vs. in parallel and quantify the
  speedup.

## Real-World Applications

1. **Large-scale audits**: security, dependency, or dead-code sweeps across a big
   repo.
2. **Codebase onboarding**: fan out to map architecture, data flow, and entry
   points at once.
3. **Multi-lens code review**: correctness, security, and style in parallel, then
   merged.
4. **Migrations**: transform many files independently in isolated worktrees.
5. **Research**: search many sources concurrently, then synthesize.

Remember: parallelism is a tool for *independent* work. Used well it multiplies
throughput; used on dependent steps it just multiplies confusion. Decompose
first, then fan out.
