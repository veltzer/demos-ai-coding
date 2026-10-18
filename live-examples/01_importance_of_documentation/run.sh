#!/usr/bin/env bash
# Demo 01: a documented repo gets better AI work than an undocumented one.
#
# Two copies of the same small shop codebase get the same one-line request:
#   A - code only:  no CLAUDE.md, no docs/.
#   B - documented: CLAUDE.md + docs/architecture.md + docs/business-rules.md.
# The code is byte-identical. The docs hold what code cannot say: business
# rules, a known bug, a module that is frozen, how rounding works.
# A hidden acceptance check scores both, naming the doc each failure was
# written down in, and the scoreboard shows what each side spent.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/common.sh
source "${HERE}/../lib/common.sh"

case "${1:-}" in
--yes) export YES=1 ;;
-h | --help)
	sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
	exit 0
	;;
"") ;;
*)
	echo "unknown option: $1 (try --help)" >&2
	exit 2
	;;
esac

require claude git python3 diff

REQUEST="Add a loyalty discount: customers who already have 5 or more orders get 10% off."

TOOLS=(--allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)")

make_workdir "${HERE}"
A="${WORKDIR}/A-code-only"
B="${WORKDIR}/B-documented"
copy_app "${HERE}/app" "${A}"
copy_app "${HERE}/app" "${B}" "${HERE}/docs-only"

banner "Two copies of the same codebase"
say "A small shop backend: orders, discounts, pricing, shipping, stock. Same code in both:"
echo
(cd "${A}" && find shop tests -name '*.py' | sort | sed 's/^/    /')
echo
say "The only difference:"
echo
diff -rq --exclude=.git "${A}" "${B}" | sed "s|${WORKDIR}/||g; s/^/    /" || true
pause "to read B's CLAUDE.md"
sed 's/^/    /' "${B}/CLAUDE.md"
echo
say "...plus docs/business-rules.md: what 'orders' means, stacking, a known bug."
pause "to see the request"

banner "The request (same for both)"
echo "  ${REQUEST}"
echo
say "One sentence. Everything else, each AI has to find out for itself."
pause "to run A: code only"

banner "A: code only"
run_claude "${A}" "${WORKDIR}/A.json" "${REQUEST}" "${TOOLS[@]}"
echo
git -C "${A}" --no-pager diff --stat
pause "to run B: documented"

banner "B: documented"
run_claude "${B}" "${WORKDIR}/B.json" "${REQUEST}" "${TOOLS[@]}"
echo
git -C "${B}" --no-pager diff --stat
pause "to score both"

banner "Scoring against the business rules"
for side in "${A}" "${B}"; do
	echo "${BOLD}$(basename "${side}")${RESET}"
	python3 "${HERE}/acceptance/check.py" "${side}" | tee "${side}.score" || true
	echo
done
say "Each FAIL names the doc that had the answer. A was not careless: those"
say "rules exist only in people's heads, or in docs A never got."
pause "for the scoreboard"

banner "Scoreboard"
score() { grep -o 'score: [0-9]*/[0-9]*' "$1.score" | cut -d' ' -f2; }
python3 "${LIB_DIR}/scoreboard.py" \
	"A code only|$(score "${A}")|${WORKDIR}/A.json" \
	"B documented|$(score "${B}")|${WORKDIR}/B.json"
echo
docs_lines="$(cat "${HERE}/docs-only/CLAUDE.md" "${HERE}"/docs-only/docs/*.md | wc -l)"
echo "  ${BOLD}Cost of the docs:${RESET} ${docs_lines} lines of markdown, written once," \
	"read by every session and every new colleague."
echo
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
