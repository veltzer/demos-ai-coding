# Demo 07: choosing the right model

```bash
./run.sh                                              # interactive
./run.sh --yes                                        # unattended dry run
MODELS="claude-haiku-5-5 claude-opus-5-5" ./run.sh    # choose the models
```

## What happens

One detail-heavy task goes to several models with the same prompt:
implement a fixed-width bank payment file from a two-page spec
(`app/docs/bankfile.md`). It covers 80-character records, padding,
payee-name cleaning, credit and debit totals, an entry hash, blocking to
multiples of 10, and validation. The first model runs live, the others in
parallel.

`acceptance/check.py` scores each rule of the spec separately (14 checks)
against a reference implementation, on its own data. The scoreboard shows
score, time, tokens and cost per model, and names the cheapest model that
passed everything.

## Rehearsal numbers

| Model | Score | Time | Cost |
|-------|-------|------|------|
| Haiku | 14/14 | 62 s | $0.012 |
| Sonnet | 14/14 | 23 s | $0.06 |
| Opus | 14/14 | 57 s | $0.21 |

All three were correct in every run so far (8 runs across the models).
Opus cost 17 times as much as Haiku, and Sonnet was the fastest.

## Talking points

- On a clear, well-specified task, the small model was enough. Paying for
  the biggest one by default is a habit, not a requirement.
- Cost is not speed: Haiku read more and took longer, yet was the cheapest.
  Pick on what matters for the job: cost, latency or headroom.
- The other half: where a cheap model fails (vague specs, large codebases,
  long multi-step work), the bigger model earns its price. Measure on your
  own tasks, because a scoreboard like this is cheap to build.
- Mixing works too: a big model to plan, a small one to carry out the steps.

## Files

- `app/`: the ledger package with the spec and an empty `bankfile.py`
- `acceptance/check.py`, `acceptance/reference.py`: the hidden scoring
- Work dir `/tmp/demo-07_choosing_the_right_model/`: one copy and log per model
