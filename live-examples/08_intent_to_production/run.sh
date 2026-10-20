#!/usr/bin/env bash
# Demo 08: one feature from intent to production, one artifact per phase.
#
# The starting point is a working, tested, documented tic-tac-toe game for the
# browser, which the script deploys to production first so it can be played.
# Then the business hands over intent.md: a secret cheat code that lets the
# player steal a square from the computer. It goes all the way: spec -> plan
# -> implementation -> unit tests -> system test -> lint -> code review ->
# review fixes -> deploy to production. Every phase is a fresh AI session with
# a one-line prompt; docs/process.md says what each phase does, and the files
# in changes/cheat-code/ are the only memory. After each phase the script
# checks the result itself and commits it, so git log is the pipeline.
# Production (default port 8088) stays up after the demo.
#
# Between phases a browser tab shows the pipeline with the current stage
# highlighted, and each artifact (intent, spec, plan, ...) opens rendered as it
# is written. Production and the preview open in the browser too.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses)
#        PREVIEW_PORT=8087 PROD_PORT=8088 ./run.sh
#        VIEW=0 ./run.sh      no browser windows, terminal only

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/common.sh
source "${HERE}/../lib/common.sh"

case "${1:-}" in
--yes) export YES=1 ;;
-h | --help)
	sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
	exit 0
	;;
"") ;;
*)
	echo "unknown option: $1 (try --help)" >&2
	exit 2
	;;
esac

require claude git python3 ruff curl pandoc xdg-open
python3 -c 'import pytest' 2>/dev/null || {
	echo "missing required tool: pytest (for python3 -m pytest)" >&2
	exit 1
}

RED=$'\033[31m'
CHANGE="changes/cheat-code"
PREVIEW_PORT="${PREVIEW_PORT:-8087}"
export PROD_PORT="${PROD_PORT:-8088}"
PROD_URL="http://127.0.0.1:${PROD_PORT}"
EDIT_TOOLS=("Read" "Glob" "Grep" "Write" "Edit" "Bash(python3:*)" "Bash(ruff:*)")
REVIEW_TOOLS=("Read" "Glob" "Grep" "Write" "Bash(git diff:*)" "Bash(git log:*)" "Bash(python3 -m pytest:*)" "Bash(ruff:*)")
DEPLOY_TOOLS=("${EDIT_TOOLS[@]}" "Bash(./ops/deploy.sh:*)" "Bash(ops/deploy.sh:*)" "Bash(curl:*)")

# A production server left running by the previous run lives in the work
# dir about to be wiped: stop it first.
WORKDIR="${WORKDIR:-${TMPDIR:-/tmp}/demo-$(basename "${HERE}")}"
if [[ -f "${WORKDIR}/.demo-workdir" && -f "${WORKDIR}/production/server.pid" ]]; then
	kill "$(cat "${WORKDIR}/production/server.pid")" 2>/dev/null || true
fi
make_workdir "${HERE}"
APP="${WORKDIR}/app"
copy_app "${HERE}/app" "${APP}"
git -C "${APP}" branch baseline

PREVIEW_PID=""
stop_preview() {
	[[ -n "${PREVIEW_PID}" ]] && kill "${PREVIEW_PID}" 2>/dev/null
	PREVIEW_PID=""
}
trap stop_preview EXIT

ok() { printf '  %s✔ %s%s\n' "${GREEN}" "$*" "${RESET}"; }
bad() { printf '  %s✘ %s%s\n' "${RED}${BOLD}" "$*" "${RESET}"; }
need() {
	[[ -e "${APP}/$1" ]] || {
		bad "$1 was not written - rerun the demo"
		exit 1
	}
}
progress() { python3 "${LIB_DIR}/checklist.py" "${APP}/${CHANGE}/plan.md" "$@"; }

# phase <key> <title> <prompt> <tool...>: one fresh session, then a commit
phase() {
	local key="$1" title="$2" prompt="$3"
	shift 3
	banner "${title}"
	run_claude "${APP}" "${WORKDIR}/${key}.json" "${prompt}" --allowedTools "$@"
	snapshot "${APP}" "${key}"
}

prompt_for() { echo "Do phase $1 of docs/process.md for the change in ${CHANGE}/."; }

# check <label> <command...>: run a gate in the app, show a pass/fail line
check() {
	local label="$1" out
	shift
	if out="$(cd "${APP}" && "$@" 2>&1)"; then
		ok "${label}"
	else
		bad "${label}"
		printf '%s\n' "${out}" | tail -n 15 | sed 's/^/      /'
		return 1
	fi
}

# run_tests <label>: the whole suite, once, shown as a pass/fail line
run_tests() {
	local out
	if out="$(cd "${APP}" && python3 -m pytest -q 2>&1)"; then
		ok "$1: $(tail -n 1 <<<"${out}")"
	else
		bad "$1: $(tail -n 1 <<<"${out}")"
		grep -E '^(FAILED|ERROR)' <<<"${out}" | head -n 10 | sed 's/^/      /' || true
	fi
}

# sign_off <verdict>: the person's preview result, recorded where the review
# will read it. An unattended run says so instead of pretending someone looked.
sign_off() {
	local who="${USER:-the presenter}" result="$1"
	if [[ "${YES:-0}" == 1 ]]; then
		who="nobody: unattended run (run.sh --yes)"
		result="not checked"
	elif [[ "${result}" == yes ]]; then
		result="passed every check in the plan's preview list"
	fi
	cat >"${APP}/${CHANGE}/preview.md" <<-EOF
		# Preview sign-off

		- Date: $(date '+%Y-%m-%d %H:%M')
		- Checked by: ${who}
		- What: the page at a preview server, against \`## For the preview\` in \`plan.md\`
		- Result: ${result}
	EOF
	snapshot "${APP}" 3-preview
	show_path "the sign-off, for the reviewer" "${APP}/${CHANGE}/preview.md"
}

# The stages of the pipeline, in order, as "stage|what it leaves".
STAGES=(
	"Version 1 in production|the game, deployed by ops/deploy.sh"
	"The intent|intent.md, from the business"
	"Phase 1: Spec|spec.md"
	"Phase 2: Plan|plan.md"
	"Phase 3: Implement|code, docs/architecture.md"
	"Preview (you)|preview.md, your sign-off"
	"Phase 4: Unit tests|tests/"
	"Phase 5: System test|tests/system/, test-report.md"
	"Phase 6: Lint|clean code"
	"Phase 7: Code review|review.md"
	"Phase 8: Review fixes|ticked review.md"
	"Phase 9: Deploy|release 2 in production"
)

# roadmap <n>: write pipeline.md with stage n highlighted as the current one
# (n past the last stage: all done) and show it. It lives in the work dir,
# not the app, so no session ever reads it.
roadmap() {
	local now="$1" i name leaves title="Pipeline: done" md="${WORKDIR}/pipeline.md"
	((now < ${#STAGES[@]})) && title="Pipeline: ${STAGES[now]%%|*}"
	{
		echo "# Intent to production: where we are"
		echo
		echo "Change \`cheat-code\`: a secret code that lets the player steal a square."
		echo
		echo "| | Stage | Leaves |"
		echo "|---|---|---|"
		for i in "${!STAGES[@]}"; do
			name="${STAGES[i]%%|*}"
			leaves="${STAGES[i]#*|}"
			if ((i < now)); then
				echo "| ✅ | ${name} | ${leaves} |"
			elif ((i == now)); then
				echo "| ▶ | <mark>${name} ← we are here</mark> | <mark>${leaves}</mark> |"
			else
				echo "| ⬜ | ${name} | ${leaves} |"
			fi
		done
		echo
		if ((now >= ${#STAGES[@]})); then
			echo "**Done:** every stage ran; production now serves release 2."
		else
			echo "**Now:** ${STAGES[now]%%|*}"
		fi
	} >"${md}"
	show_md "${md}" "${title}"
}

findings() {
	grep -E '^[[:space:]]*- \[[ xX]\] \*\*' "${APP}/${CHANGE}/review.md" | sed 's/^[[:space:]]*/    /' || true
}

# ── 0. where we start ────────────────────────────────────────────────────────
banner "Where we start: a working game, with its docs"
roadmap 0
(cd "${APP}" && find . -path ./.git -prune -o -type f -print | sort | sed 's|^\./|    |')
echo
run_tests "tests"
check "ruff" ruff check . || true
say "Version 1 goes to production the way every release does: through ops/deploy.sh."
if (cd "${APP}" && ops/deploy.sh >"${WORKDIR}/deploy-v1.log" 2>&1); then
	ok "$(grep DEPLOYED "${WORKDIR}/deploy-v1.log")"
else
	bad "the v1 deploy failed"
	tail -n 15 "${WORKDIR}/deploy-v1.log" | sed 's/^/      /'
	exit 1
fi
show_path "production, version 1 - try to beat Hard" "${PROD_URL}/"
open_url "${PROD_URL}/"
echo
pause "for the change request"

# ── the intent ───────────────────────────────────────────────────────────────
banner "The business hands over an intent"
roadmap 1
mkdir -p "${APP}/${CHANGE}"
cp "${HERE}/intent.md" "${APP}/${CHANGE}/intent.md"
snapshot "${APP}" 0-intent
show_path "the intent" "${APP}/${CHANGE}/intent.md"
show_md "${APP}/${CHANGE}/intent.md" "intent.md"
echo
sed -n '/^## What we want/,/^## How we will know/p' "${APP}/${CHANGE}/intent.md" | sed '$d' | sed 's/^/    /'
say "Business language only: no API, no modules, no tests. Nine phases turn it"
say "into a release. Every prompt is one line: docs/process.md carries the rest."
pause "to write the spec"

# ── 1. spec ──────────────────────────────────────────────────────────────────
roadmap 2
phase 1-spec "Phase 1: intent -> spec" "$(prompt_for "1 (Spec)")" "${EDIT_TOOLS[@]}"
need "${CHANGE}/spec.md"
show_path "the design" "${APP}/${CHANGE}/spec.md"
show_md "${APP}/${CHANGE}/spec.md" "spec.md"
grep -E '^#{1,3} ' "${APP}/${CHANGE}/spec.md" | sed 's/^/    /' || true
check "no code changed yet" git diff --quiet 0-intent 1-spec -- tictactoe tests || true
pause "to plan the implementation"

# ── 2. plan ──────────────────────────────────────────────────────────────────
roadmap 3
phase 2-plan "Phase 2: spec -> plan" "$(prompt_for "2 (Plan)")" "${EDIT_TOOLS[@]}"
need "${CHANGE}/plan.md"
show_path "the plan - open it and watch the boxes tick" "${APP}/${CHANGE}/plan.md"
show_md "${APP}/${CHANGE}/plan.md" "plan.md"
echo
progress
pause "to implement it, one plan phase per session"

# ── 3. implement ─────────────────────────────────────────────────────────────
roadmap 4
read -r ticked total < <(progress --summary)
sessions=0
while ((ticked < total)); do
	sessions=$((sessions + 1))
	if ((sessions > 6)); then
		bad "still ${ticked}/${total} after 6 sessions - stopping"
		exit 1
	fi
	before=${ticked}
	phase "3-implement-${sessions}" "Phase 3: implement, session ${sessions}  (${ticked}/${total} done)" \
		"$(prompt_for "3 (Implement)")" "${EDIT_TOOLS[@]}"
	echo
	progress
	read -r ticked total < <(progress --summary)
	if ((ticked == before)); then
		bad "session ${sessions} ticked nothing - stopping"
		exit 1
	fi
done
IMPLEMENTED="3-implement-${sessions}"
echo
run_tests "the existing tests"
git -C "${APP}" diff --stat 2-plan "${IMPLEMENTED}" -- tictactoe docs | sed 's/^/    /'

roadmap 5
banner "First look: a preview server (production still runs version 1)"
(cd "${APP}" && exec python3 -m tictactoe --port "${PREVIEW_PORT}" >"${WORKDIR}/preview.log" 2>&1) &
PREVIEW_PID=$!
for _ in $(seq 50); do
	curl -fsS --max-time 1 "http://127.0.0.1:${PREVIEW_PORT}/health" >/dev/null 2>&1 && break
	sleep 0.1
done
if check "GET /health on the preview server" curl -fsS --max-time 1 "http://127.0.0.1:${PREVIEW_PORT}/health"; then
	show_path "the preview" "http://127.0.0.1:${PREVIEW_PORT}/"
	open_url "http://127.0.0.1:${PREVIEW_PORT}/"
	echo
	say "Start a game against Hard, click into the page and type: ↑ ↑ ↓ ↓ ← → ← → B A"
	say "It runs. Is it right? Nothing new has been tested yet - that is the next phase."
	echo
	sed -n '/^## For the preview/,$p' "${APP}/${CHANGE}/plan.md" | sed 's/^/    /'
	echo
	verdict="$(ask "Did the page pass that list? [enter] yes, or type what was wrong:" "yes")"
else
	tail -n 15 "${WORKDIR}/preview.log" | sed 's/^/      /'
	say "The next phases test it and should find out why."
	verdict="the preview server did not start: $(tail -n 1 "${WORKDIR}/preview.log")"
fi
stop_preview
sign_off "${verdict}"

# ── 4. unit tests ────────────────────────────────────────────────────────────
roadmap 6
phase 4-unit-tests "Phase 4: unit tests" "$(prompt_for "4 (Unit tests)")" "${EDIT_TOOLS[@]}"
echo
run_tests "whole suite"
git -C "${APP}" diff --stat 3-preview 4-unit-tests | sed 's/^/    /'
say "(any tictactoe/ lines above are code the tests forced to change: bugs caught early)"
pause "to test the running system"

# ── 5. system test ───────────────────────────────────────────────────────────
roadmap 7
phase 5-system-test "Phase 5: system test over HTTP" "$(prompt_for "5 (System test)")" "${EDIT_TOOLS[@]}"
need "${CHANGE}/test-report.md"
echo
run_tests "whole suite"
show_path "the test report" "${APP}/${CHANGE}/test-report.md"
show_md "${APP}/${CHANGE}/test-report.md" "test-report.md"
pause "to lint"

# ── 6. lint ──────────────────────────────────────────────────────────────────
roadmap 8
banner "Before linting"
check "ruff check" ruff check . || true
check "ruff format --check" ruff format --check . || true
phase 6-lint "Phase 6: lint" "$(prompt_for "6 (Lint)")" "${EDIT_TOOLS[@]}"
echo
check "ruff check" ruff check . || true
check "ruff format --check" ruff format --check . || true
check "ruff config untouched" git diff --quiet baseline -- pyproject.toml || true
check "no # noqa anywhere" bash -c '! grep -rn "noqa" --include="*.py" .' || true
run_tests "tests still pass"
pause "for the code review"

# ── 7. review ────────────────────────────────────────────────────────────────
roadmap 9
phase 7-review "Phase 7: code review (a fresh reviewer, no code changes)" \
	"$(prompt_for "7 (Code review)")" "${REVIEW_TOOLS[@]}"
need "${CHANGE}/review.md"
echo
findings
echo
check "the reviewer changed no code" git diff --quiet 6-lint 7-review -- tictactoe tests docs || true
show_path "the review" "${APP}/${CHANGE}/review.md"
show_md "${APP}/${CHANGE}/review.md" "review.md"
pause "to fix the findings"

# ── 8. review fixes ──────────────────────────────────────────────────────────
roadmap 10
phase 8-fixes "Phase 8: fix the review findings" "$(prompt_for "8 (Review fixes)")" "${EDIT_TOOLS[@]}"
echo
findings
echo
run_tests "whole suite"
pause "to deploy to production"

# ── 9. deploy ────────────────────────────────────────────────────────────────
roadmap 11
phase 9-deploy "Phase 9: deploy to production" "$(prompt_for "9 (Deploy)")" "${DEPLOY_TOOLS[@]}"
echo
check "production: $(cd "${APP}" && ops/deploy.sh --status)" \
	curl -fsS --max-time 2 "${PROD_URL}/health" || true
say "releases (the first is version 1, kept for rollback):"
find "${WORKDIR}/production/releases" -mindepth 1 -maxdepth 1 -printf '    %f\n' 2>/dev/null | sort || true
show_path "production, with the cheat - ↑ ↑ ↓ ↓ ← → ← → B A" "${PROD_URL}/"
open_url "${PROD_URL}/"
pause "for the summary"

# ── summary ──────────────────────────────────────────────────────────────────
banner "The pipeline"
roadmap "${#STAGES[@]}"
git -C "${APP}" log --reverse --format='    %s' baseline..HEAD
echo
git -C "${APP}" diff --stat baseline HEAD | tail -n 1 | sed 's/^/   /'
echo
impl=""
for ((i = 1; i <= sessions; i++)); do impl+="${WORKDIR}/3-implement-${i}.json,"; done
all="${impl}"
rows=()
for key in 1-spec 2-plan 3-implement 4-unit-tests 5-system-test 6-lint 7-review 8-fixes 9-deploy; do
	if [[ "${key}" == 3-implement ]]; then
		rows+=("implement (${sessions} sessions)||${impl%,}")
	else
		rows+=("${key#*-}||${WORKDIR}/${key}.json")
		all+="${WORKDIR}/${key}.json,"
	fi
done
python3 "${LIB_DIR}/scoreboard.py" "${rows[@]}" "||" "total||${all%,}"
echo
say "Each phase left a file the next one read: intent -> spec -> plan -> code ->"
say "tests -> report -> review -> release, all in ${CHANGE}/. A human can read,"
say "change or veto any of them and rerun from there."
say "Production stays up: ${PROD_URL}/   stop it: ${APP}/ops/deploy.sh --stop"
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
