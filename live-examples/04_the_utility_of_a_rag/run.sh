#!/usr/bin/env bash
# Demo 04: answering from private knowledge with and without RAG.
#
# The internal wiki of a fictional company (generated, ~70k tokens, so no
# model can know it) and 10 questions about it, asked three ways:
#   A - no RAG:     just the questions.
#   B - RAG:        a small BM25 retriever puts the 5 best wiki sections per
#                   question into the prompt.
#   C - stuff it:   the entire wiki goes into the prompt.
# Same questions, same instructions, no tools: the only difference is the
# context. Answers are scored against the known truth, and the scoreboard
# shows what each approach costs.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/common.sh
source "${HERE}/../lib/common.sh"

case "${1:-}" in
--yes) export YES=1 ;;
-h | --help)
	sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
	exit 0
	;;
"") ;;
*)
	echo "unknown option: $1 (try --help)" >&2
	exit 2
	;;
esac

require claude python3

# Answer from the prompt only: no tools, and a plain system prompt instead of
# the coding-agent one, so the only difference between A, B and C is the
# context in the user message.
NO_TOOLS=(--system-prompt "You answer questions from the information you are given. You have no tools." --tools "")

make_workdir "${HERE}"
CORPUS="${WORKDIR}/corpus"
QUESTIONS="${WORKDIR}/questions.json"
EMPTY="${WORKDIR}/empty"
mkdir -p "${EMPTY}"
rag() { python3 "${HERE}/rag.py" "$@"; }

banner "The knowledge: Quillstack's internal wiki"
python3 "${HERE}/make_corpus.py" "${WORKDIR}" >/dev/null
say "Quillstack does not exist. Its wiki is generated, so no model has ever seen it:"
echo
rag stats "${CORPUS}" | sed 's/^/  /'
echo
(cd "${CORPUS}" && find . -name '*.md' | sort | sed 's|^\./||' | awk -F/ '{n[$1]++} END {for (d in n) printf "    %-10s %3d documents\n", d"/", n[d]}' | sort)
echo
say "One page, for a feel:"
sed -n '1,16p' "$(find "${CORPUS}/services" -name '*.md' | sort | head -1)" | sed 's/^/    /'
pause "to see the questions"

banner "The questions"
python3 -c 'import json,sys; [print("  Q%d: %s" % (i, q["q"])) for i, q in enumerate(json.load(open(sys.argv[1])), 1)]' "${QUESTIONS}"
pause "to ask without RAG"

banner "A: no RAG"
rag prompt "${CORPUS}" "${QUESTIONS}" none "${WORKDIR}/A.prompt" | sed 's/^/  /'
run_claude "${EMPTY}" "${WORKDIR}/A.json" "@${WORKDIR}/A.prompt" "${NO_TOOLS[@]}"
pause "to see how retrieval works"

banner "How the retriever works"
example="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[0]["q"])' "${QUESTIONS}")"
say "For every question, rank all wiki sections by word overlap (BM25) and keep the top 5."
echo
echo "  ${BOLD}query:${RESET} ${example}"
rag search "${CORPUS}" "${example}"
echo
say "Only those excerpts go into the prompt: a few hundred tokens per question, not the whole wiki."
pause "to ask with RAG"

banner "B: RAG"
rag prompt "${CORPUS}" "${QUESTIONS}" rag "${WORKDIR}/B.prompt" | sed 's/^/  /'
run_claude "${EMPTY}" "${WORKDIR}/B.json" "@${WORKDIR}/B.prompt" "${NO_TOOLS[@]}"
pause "to stuff the whole wiki into the prompt"

banner "C: the whole wiki in the prompt"
rag prompt "${CORPUS}" "${QUESTIONS}" full "${WORKDIR}/C.prompt" | sed 's/^/  /'
run_claude "${EMPTY}" "${WORKDIR}/C.json" "@${WORKDIR}/C.prompt" "${NO_TOOLS[@]}"
pause "to score the answers"

banner "Scoring against the truth"
python3 "${HERE}/score.py" "${QUESTIONS}" \
	"A no RAG=${WORKDIR}/A.json" "B RAG=${WORKDIR}/B.json" "C whole wiki=${WORKDIR}/C.json"
pause "for the scoreboard"

banner "Scoreboard"
python3 "${LIB_DIR}/scoreboard.py" \
	"A no RAG|$(cat "${WORKDIR}/A.score")|${WORKDIR}/A.json" \
	"B RAG|$(cat "${WORKDIR}/B.score")|${WORKDIR}/B.json" \
	"C whole wiki|$(cat "${WORKDIR}/C.score")|${WORKDIR}/C.json"
echo
say "C only works while the whole wiki fits in the context window, and every"
say "question pays for all of it. RAG pays for the few sections that matter."
say "Prompts, answers and the generated wiki are in ${WORKDIR}"
echo "${GREEN}done${RESET}"
