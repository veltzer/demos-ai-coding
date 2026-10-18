#!/usr/bin/env bash
# Demo 02: a plan with checkboxes, implemented one phase at a time.
#
#   1. The AI writes plan.md: phases ("## Phase N: ...") of "- [ ]" tasks,
#      each phase ending in a verification task. No code yet.
#   2. A loop starts a FRESH AI session per phase: "do the first phase that
#      still has unchecked boxes, tick each box as soon as it is done, stop".
#      Ticks show up live in green; the checklist is redrawn after each phase.
#   3. When every box is ticked, the finished program runs.
#
# Each phase is a new session with no memory of the previous one: plan.md is
# the only thing carrying the work forward.
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

require claude git python3

GOAL="Build life.py: Conway's Game of Life for the terminal, plain Python, standard library only.
It loads a named pattern (glider, blinker, a random soup) or a plain-text pattern file,
runs N generations on a board that wraps around at the edges, prints each generation,
and has unittest tests for the rules."

PLAN_PROMPT="Do NOT write any code yet. Write plan.md for this goal:

${GOAL}

Format, exactly:
- First line '# Plan: <title>', then a line 'Demo: <one shell command>' that shows the
  finished program off in under 3 seconds of output (few generations, no screen clearing
  or sleeping).
- 3 to 5 phases, each a heading '## Phase N: <name>' followed only by task lines '- [ ] <task>'.
- 3 to 5 tasks per phase. Each phase's LAST task verifies that phase (a test or a command to run).
- Each phase must leave the project working, so the next phase can start from it."

PHASE_PROMPT="Read plan.md. Implement the FIRST phase that still has unchecked boxes, and ONLY that phase.
After finishing each task, immediately tick its box in plan.md with the Edit tool
('- [ ]' -> '- [x]'), one task per edit, before starting the next task.
Run the phase's verification. When it passes and the phase is fully ticked, stop."

TOOLS=(--allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)")

progress() { python3 "${LIB_DIR}/checklist.py" "${APP}/plan.md" "$@"; }

make_workdir "${HERE}"
APP="${WORKDIR}/life"
copy_app "${HERE}/start" "${APP}"

banner "The goal"
printf '  %s\n' "${GOAL//$'\n'/$'\n'  }"
echo
say "Starting from an empty folder. Step one is a plan, not code."
pause "to write the plan"

banner "Step 1: write plan.md"
run_claude "${APP}" "${WORKDIR}/plan.json" "${PLAN_PROMPT}" "${TOOLS[@]}"
if [[ ! -f "${APP}/plan.md" ]]; then
	echo "plan.md was not written - rerun the demo" >&2
	exit 1
fi
show_path "plan.md is on disk - open it in an editor and watch the boxes tick" "${APP}/plan.md"
echo
progress
echo
say "This is where you edit the plan: reorder phases, cut scope, add a task."
choice="$(ask "[enter] start phase 1, or [e]dit plan.md first?" "")"
if [[ "${choice}" == e ]]; then
	"${EDITOR:-vi}" "${APP}/plan.md"
	echo
	progress
fi

read -r ticked total < <(progress --summary)
phase=0
max_phases=8
while ((ticked < total)); do
	phase=$((phase + 1))
	if ((phase > max_phases)); then
		echo "still ${ticked}/${total} after ${max_phases} sessions - stopping" >&2
		exit 1
	fi
	before=${ticked}
	banner "Session ${phase}: next unchecked phase  (${ticked}/${total} done)"
	say "A brand-new session. All it knows is what plan.md and the code tell it."
	run_claude "${APP}" "${WORKDIR}/phase${phase}.json" "${PHASE_PROMPT}" "${TOOLS[@]}"
	echo
	progress
	read -r ticked total < <(progress --summary)
	if ((ticked == before)); then
		echo "session ${phase} ticked nothing - stopping" >&2
		exit 1
	fi
	snapshot "${APP}" "phase${phase}"
	if ((ticked < total)); then
		pause "for the next phase"
	fi
done

banner "All boxes ticked: run it"
# shellcheck disable=SC2016  # the backticks are literal: strip markdown code quotes
demo_cmd="$(grep -m1 '^Demo:' "${APP}/plan.md" | sed 's/^Demo:[[:space:]]*//; s/^`//; s/`$//')"
if [[ -n "${demo_cmd}" ]]; then
	printf '%s$ %s%s\n\n' "${BOLD}" "${demo_cmd}" "${RESET}"
	(cd "${APP}" && timeout 10 bash -c "${demo_cmd}" | head -n 60) || true
else
	say "plan.md has no 'Demo:' line; try: cd ${APP} && python3 life.py --help"
fi
pause "for the scoreboard"

banner "Scoreboard"
rows=("plan||${WORKDIR}/plan.json")
all="${WORKDIR}/plan.json"
for ((i = 1; i <= phase; i++)); do
	rows+=("session ${i}||${WORKDIR}/phase${i}.json")
	all+=",${WORKDIR}/phase${i}.json"
done
python3 "${LIB_DIR}/scoreboard.py" "${rows[@]}" "||" "total|${ticked}/${total}|${all}"
echo
say "Every phase is a commit: git -C ${APP} log --oneline"
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
