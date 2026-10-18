# Live examples

Scripted live demos of where AI coding works better. Each folder has a
`run.sh` that runs the whole demo with headless `claude -p` sessions and a
`README.md` with what to say.

| Demo | Shows |
|------|-------|
| `01_importance_of_documentation/` | the same code with and without CLAUDE.md + docs |
| `02_how_to_make_a_plan/` | a checkbox plan carried out phase by phase, boxes ticked live |
| `03_importance_of_planning/` | plan first vs just do it, and the tokens spent fixing the bad guesses |
| `04_the_utility_of_a_rag/` | private knowledge: no RAG vs RAG vs the whole wiki in the prompt |

```bash
cd 01_importance_of_documentation && ./run.sh          # interactive: pauses so you can talk
cd 01_importance_of_documentation && ./run.sh --yes    # unattended rehearsal
MODEL=claude-sonnet-5-5 ./run.sh   # any demo, another model
```

Each run works on fresh copies in `/tmp/demo-<demo folder>/`, a fixed path that is
reset on every run, so you can open files there (like `plan.md`) mid-demo.
The folders here never change. Set `WORKDIR=` to put the copies elsewhere. The demo sessions load only project settings,
so your personal `~/.claude` instructions, memory and hooks stay out of them.

`lib/` is shared: `common.sh` (pauses, copies, running claude), `stream.py`
(live view of the session), `scoreboard.py` (time/tokens/cost table) and
`checklist.py` (draws a checkbox plan).
