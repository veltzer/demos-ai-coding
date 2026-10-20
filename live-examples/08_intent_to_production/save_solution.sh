#!/usr/bin/env bash
# Save a finished run of demo 08 as solution/, for ./run.sh --with-solution
# and for showing the artifacts without waiting for the AI.
#
# For every AI phase it keeps <key>.patch (the change the session made) and
# <key>.jsonl (its event log, replayed on stage; the work dir's path becomes
# @APP@). cheat-code/ holds the artifacts as the run ended, and change.diff
# the whole code change.
#
# Usage: ./save_solution.sh [work-dir]   (default: the work dir run.sh uses)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:-${TMPDIR:-/tmp}/demo-$(basename "${HERE}")}"
APP="${WORK}/app"
OUT="${HERE}/solution"

git -C "${APP}" rev-parse --verify -q 9-deploy >/dev/null || {
	echo "${WORK} holds no finished run (no 9-deploy commit)" >&2
	exit 1
}

rm -rf "${OUT}"
mkdir -p "${OUT}/cheat-code"
# Every commit after the baseline is one step; 0-intent and 3-preview are
# made by run.sh itself, the rest by an AI session.
git -C "${APP}" log --reverse --format=%s baseline..9-deploy | while read -r key; do
	[[ "${key}" == 0-intent || "${key}" == 3-preview ]] && continue
	[[ -f "${WORK}/${key}.jsonl" ]] || {
		echo "no session log ${WORK}/${key}.jsonl - was the run made before logs were kept?" >&2
		exit 1
	}
	git -C "${APP}" diff --binary "${key}^" "${key}" >"${OUT}/${key}.patch"
	grep -v '"type":"stream_event"' "${WORK}/${key}.jsonl" | sed "s|${APP}|@APP@|g" >"${OUT}/${key}.jsonl"
	echo "saved ${key}"
done
cp "${APP}/changes/cheat-code/"*.md "${OUT}/cheat-code/"
git -C "${APP}" diff baseline 9-deploy -- . ':!changes' >"${OUT}/change.diff"
echo "saved the artifacts and change.diff in ${OUT}"
