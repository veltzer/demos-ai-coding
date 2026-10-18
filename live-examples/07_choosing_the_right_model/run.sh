#!/usr/bin/env bash
# Demo 07: choosing the right model.
#
# One detail-heavy task, a fixed-width bank payment file from a two-page spec
# (app/docs/bankfile.md), given to several models with the same prompt. The
# first runs live, the others in parallel. A hidden check scores every rule
# of the spec, and the scoreboard shows what each model cost.
# The lesson: use the cheapest model that passes, not the biggest by default.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses)
#        MODELS="claude-haiku-5-5 claude-opus-5-5" ./run.sh

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/common.sh
source "${HERE}/../lib/common.sh"

case "${1:-}" in
--yes) export YES=1 ;;
-h | --help)
	sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
	exit 0
	;;
"") ;;
*)
	echo "unknown option: $1 (try --help)" >&2
	exit 2
	;;
esac

require claude git python3

read -r -a MODEL_LIST <<<"${MODELS:-claude-haiku-5-5 claude-sonnet-5-5 claude-opus-5-5}"
REQUEST="Implement export_bank_file in ledger/bankfile.py, following the bank's format in docs/bankfile.md. Our first payment run with the new bank is tomorrow."
TOOLS=(--allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)")

make_workdir "${HERE}"
for model in "${MODEL_LIST[@]}"; do
	copy_app "${HERE}/app" "${WORKDIR}/${model}"
done

# attempt <model> [quiet]: one session with that model, in its own copy
attempt() {
	local dir="${WORKDIR}/$1"
	(
		unset MODEL
		if [[ "${2:-}" == quiet ]]; then
			run_claude "${dir}" "${dir}.json" "${REQUEST}" --model "$1" "${TOOLS[@]}" >"${dir}.log" 2>&1
		else
			run_claude "${dir}" "${dir}.json" "${REQUEST}" --model "$1" "${TOOLS[@]}"
		fi
	)
}

banner "The task"
say "A two-page bank file spec: fixed positions, padding, name cleaning, totals,"
say "an entry hash, blocking, validation. One wrong character and the bank rejects it."
echo
sed -n '/^## 2/,/^### Payee/p' "${HERE}/app/docs/bankfile.md" | sed 's/^/    /'
echo "  ${REQUEST}"
echo
say "The same prompt goes to: ${MODEL_LIST[*]}"
pause "to start them"

banner "${MODEL_LIST[0]} (live), the others in parallel"
for model in "${MODEL_LIST[@]:1}"; do
	attempt "${model}" quiet &
done
attempt "${MODEL_LIST[0]}"
if ((${#MODEL_LIST[@]} > 1)); then
	echo
	say "waiting for ${MODEL_LIST[*]:1}..."
	wait
fi
pause "to score every model"

banner "Scoring every rule of the spec"
for model in "${MODEL_LIST[@]}"; do
	echo "${BOLD}${model}${RESET}"
	python3 "${HERE}/acceptance/check.py" "${WORKDIR}/${model}" | tee "${WORKDIR}/${model}.score" | grep -E 'FAIL|score' || true
	echo
done
pause "for the scoreboard"

banner "Scoreboard"
rows=()
for model in "${MODEL_LIST[@]}"; do
	rows+=("${model}|$(grep -o 'score: [0-9]*/[0-9]*' "${WORKDIR}/${model}.score" | cut -d' ' -f2)|${WORKDIR}/${model}.json")
done
python3 "${LIB_DIR}/scoreboard.py" "${rows[@]}"
echo
python3 - "${WORKDIR}" "${MODEL_LIST[@]}" <<'EOF'
import json, re, sys
work, models = sys.argv[1], sys.argv[2:]
B, G, X = "\033[1m", "\033[32m", "\033[0m"
rows = []
for m in models:
    got, total = map(int, re.search(r"score: (\d+)/(\d+)", open(f"{work}/{m}.score").read()).groups())
    rows.append((m, got == total, json.load(open(f"{work}/{m}.json"))["cost"]))
passing = sorted((cost, m) for m, ok, cost in rows if ok)
if passing:
    cost, m = passing[0]
    dearest = max(c for _, _, c in rows)
    times = f", {dearest / cost:.0f}x cheaper than the most expensive run" if cost and dearest > cost else ""
    print(f"  {B}Cheapest model that passed every check:{X} {G}{m}{X} at ${cost:.3f}{times}.")
else:
    print(f"  {B}No model passed every check this time.{X} That is the other half of the lesson: measure.")
EOF
echo
say "Bigger models are not wrong, just often unnecessary. Measure on your own task,"
say "then pick the cheapest model that passes; keep the big one for the hard parts."
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
