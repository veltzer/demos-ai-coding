# Demo 04: RAG vs no RAG

```bash
./run.sh          # interactive, pauses between steps so you can talk
./run.sh --yes    # unattended dry run
./rag.py          # the retriever on its own (lists its commands)
```

## What happens

`make_corpus.py` generates the internal wiki of **Quillstack**, a company
that does not exist: 200 documents, about 70k tokens. It covers services
(ports, owners, datastores, flags, runbooks), teams, an error-code catalogue
and policies. A fixed seed means the same wiki every run, and the right
answers are known exactly.

The same 10 questions are asked three ways. The instructions are identical,
tools are switched off, and only the context changes:

| | Context in the prompt |
|---|---|
| **A, no RAG** | nothing, just the questions |
| **B, RAG** | for each question, the 5 best-matching wiki sections (`rag.py`, BM25) |
| **C, whole wiki** | all 200 documents |

`score.py` grades every answer as right, wrong or unknown. The scoreboard
shows the tokens and cost of each approach.

## What to expect

Rehearsal run: A 1/10 (737 tokens in, $0.01), B 9/10 (6,342 tokens, $0.04),
C 10/10 (117,633 tokens, $0.60). C sends 18 times the input of B for one
more right answer.

- **A** answers almost everything "UNKNOWN": the model knows it doesn't know.
  It may get a lucky guess on something generic. That is the point: private
  knowledge can't come from training.
- **B** gets the single-lookup questions right at a fraction of C's cost.
- **C** also gets them right, but pays for the whole wiki on every call. It
  stops working entirely once the knowledge outgrows the context window.
- **Q9 is a multi-hop question** (port → service → team → escalation
  contact). Naive retrieval finds the service page but not the team page,
  so B usually misses it while C gets it. Use it to show that retrieval
  quality is the hard part of RAG, and that agentic search (retrieve, read,
  retrieve again) is the next step.
- **Q10 has no answer in the wiki.** The right response is UNKNOWN, which
  checks that the context does not tempt the model to make something up.

## Talking points

- RAG is not magic, just good context: find the relevant text and put it in
  the prompt. The retriever here is 100 lines of BM25 with no embeddings and
  no vector database.
- RAG vs long context is a cost and scale question. Compare the tokens-in
  column for B and C, then picture a wiki 100 times bigger.
- Show the retrieval step (`rag.py search`): it is inspectable. When an
  answer is wrong, you can check whether retrieval or generation failed.
- Link to exercise `04_advanced_techniques/03_rag_implementation` for
  building one.

## Files

- `make_corpus.py`: generates the wiki and `questions.json` (with answers)
- `rag.py`: chunking, BM25 search, prompt building for the three modes
- `score.py`: grading
- Work dir (printed at the end) holds the wiki, all three prompts and the
  answers; set `WORKDIR=` to choose one.
