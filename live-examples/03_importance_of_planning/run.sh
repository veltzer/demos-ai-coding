#!/usr/bin/env bash
# Demo 03: why "write plan.md first" beats "just build it".
#
# The same feature request is given to two fresh copies of a tiny app:
#   A - "just do it": the AI codes straight away and guesses every ambiguity.
#   B - plan first:   the AI writes plan.md (no code), a human corrects it in
#                     ~30 seconds, then the AI implements the plan.
# Both results are then scored by a hidden acceptance check that encodes what
# the "product owner" really meant. A then gets the same corrections B got,
# but after the code exists, as review feedback. The tokens A spends on that
# rework are the price of its bad decisions.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses, auto-decisions)

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

require claude git python3

REQUEST="Add a \`report\` command to expenses.py that shows how much was spent per category in a given month."

PLAN_PROMPT="Do NOT write or change any code yet. Write a file plan.md for this request:

  ${REQUEST}

plan.md must contain: the intended behaviour with an example of the output,
the files and functions to change, numbered implementation steps, how you will
verify it, and a section 'Open questions & assumptions' that lists EVERY
ambiguity you notice in the request or in the data (look at expenses.csv),
each with the default you would pick. Keep it under one screen."

IMPLEMENT_PROMPT="Implement plan.md. Where the 'Decisions' section disagrees with the rest of
the plan, the Decisions section wins. Run the app to verify before you finish."

REWORK_PROMPT="A reviewer went through your \`report\` command and wants it changed to follow
these decisions:
$(cat "${HERE}/decisions.md")

Run the app to verify before you finish."

# Presenter aid, not part of the comparison: a quick model call that lists
# where plan.md disagrees with decisions.md, so the human knows what to edit.
REVIEW_MODEL="${REVIEW_MODEL:-claude-haiku-5-5}"
review_notes() {
	local prompt="${WORKDIR}/review.prompt"
	{
		echo "Compare the plan with the product owner's decisions below. A decision counts as"
		echo "covered if the plan states it anywhere (open questions, behaviour, steps or example)"
		echo "and nothing else in the plan contradicts it. List only decisions that are missing or"
		echo "contradicted. Ignore implementation detail and wording; do not nitpick. One line each:"
		echo "- <topic>: plan says \"<short quote from the plan, or: nothing>\" -> change to \"<new wording>\""
		echo "Output only that list. If every decision is covered, output exactly: PLAN OK"
		echo
		echo "=== decisions ==="
		cat "${HERE}/decisions.md"
		echo
		echo "=== plan.md ==="
		cat "${B}/plan.md"
	} >"${prompt}"
	(cd "${WORKDIR}" && claude -p --model "${REVIEW_MODEL}" --setting-sources project --tools "" \
		--system-prompt "You compare documents precisely and answer tersely." \
		<"${prompt}" 2>>"${WORKDIR}/review.stderr") || cat "${HERE}/decisions.md"
}

TOOLS=(--allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)")

make_workdir "${HERE}"
A="${WORKDIR}/A-just-do-it"
B="${WORKDIR}/B-plan-first"
copy_app "${HERE}/app" "${A}"
copy_app "${HERE}/app" "${B}"

banner "The task"
say "A tiny expense tracker: expenses.py + expenses.csv. The request is one sentence:"
echo
echo "  ${REQUEST}"
echo
say "Sounds clear. Have a look at the data though:"
echo
sed 's/^/    /' "${HERE}/app/expenses.csv"
echo
say "Food / FOOD / ' FOOD '? Refunds? A category that nets to zero? Which month by default?"
pause "to run A: just do it"

banner "A: just do it"
run_claude "${A}" "${WORKDIR}/A1.json" "${REQUEST}" "${TOOLS[@]}"
echo
git -C "${A}" --no-pager diff --stat
snapshot "${A}" round1
pause "to run B: plan first"

banner "B, step 1: write plan.md (no code)"
run_claude "${B}" "${WORKDIR}/B1.json" "${PLAN_PROMPT}" "${TOOLS[@]}"
echo
if [[ ! -f "${B}/plan.md" ]]; then
	echo "plan.md was not written - rerun the demo" >&2
	exit 1
fi
show_path "plan.md is on disk - open it in another window to show it" "${B}/plan.md"
pause "to read plan.md here"
sed 's/^/    /' "${B}/plan.md"

banner "B, step 2: the human reviews the plan"
say "This is the cheap moment: fixing a sentence in a plan, not a function in a codebase."
show_path "the plan" "${B}/plan.md"
while true; do
	echo
	say "Checking plan.md against what the product owner wants (decisions.md)..."
	notes="$(review_notes)"
	if [[ "${notes}" == *"PLAN OK"* ]]; then
		echo "  ${GREEN}${BOLD}✔ plan.md agrees with every decision${RESET}"
		break
	fi
	echo
	echo "  ${BOLD}${YELLOW}What to change in plan.md:${RESET}"
	printf '%s\n' "${notes}" | sed 's/^/    /'
	echo
	choice="$(ask "[e]dit plan.md now, append the [p]repared decisions, or [c]ontinue as is? [e]" p)"
	case "${choice:-e}" in
	e)
		"${EDITOR:-vi}" "${B}/plan.md"
		;;
	p)
		cat "${HERE}/decisions.md" >>"${B}/plan.md"
		echo
		say "Appended decisions.md. What the plan now ends with:"
		tail -n 15 "${B}/plan.md" | sed 's/^/    /'
		break
		;;
	*) break ;;
	esac
done
pause "to implement the plan"

banner "B, step 3: implement plan.md"
run_claude "${B}" "${WORKDIR}/B2.json" "${IMPLEMENT_PROMPT}" "${TOOLS[@]}"
echo
git -C "${B}" --no-pager diff --stat
pause "to score both"

banner "Scoring against what was really wanted"
for side in "${A}" "${B}"; do
	echo "${BOLD}$(basename "${side}")${RESET}"
	python3 "${HERE}/acceptance/check.py" "${side}" | tee "${side}.score1" || true
	echo
done
say "Every FAIL on A is a decision it guessed wrong. The plan surfaced those same"
say "questions for B, and the human answered them before any code existed."
pause "to send A the same corrections, as review feedback on finished code"

banner "A, round 2: rework after code review"
say "Same chat as round 1 (--continue), the way you would reply to the AI in real life."
run_claude "${A}" "${WORKDIR}/A2.json" "${REWORK_PROMPT}" --continue "${TOOLS[@]}"
echo
python3 "${HERE}/acceptance/check.py" "${A}" | tee "${A}.score2" || true
read -r added removed _ < <(git -C "${A}" diff --numstat round1 -- expenses.py) || true
pause "for the scoreboard"

banner "Scoreboard"
score() { grep -o 'score: [0-9]*/[0-9]*' "$1" | cut -d' ' -f2; }
python3 "${LIB_DIR}/scoreboard.py" \
	"A round 1: guess|$(score "${A}.score1")|${WORKDIR}/A1.json" \
	"A round 2: rework|$(score "${A}.score2")|${WORKDIR}/A2.json" \
	"A total||${WORKDIR}/A1.json,${WORKDIR}/A2.json" \
	"||" \
	"B step 1: plan||${WORKDIR}/B1.json" \
	"B step 3: implement|$(score "${B}.score1")|${WORKDIR}/B2.json" \
	"B total||${WORKDIR}/B1.json,${WORKDIR}/B2.json"
echo
echo "  ${BOLD}Cost of A's bad decisions:${RESET} the whole round-2 row, and round 2" \
	"deleted ${removed:-0} lines of round-1 code and added ${added:-0}."
echo
say "B also leaves behind plan.md: a reviewed record of the decisions, ready for the next session."
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
