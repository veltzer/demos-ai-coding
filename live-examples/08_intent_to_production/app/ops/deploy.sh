#!/usr/bin/env bash
# Deploy tictactoe to production. Owned by the platform team: do not edit.
#
# Gates (tests, lint, review) -> release copy -> switch -> smoke test,
# rolling back to the previous release if the smoke test fails.
#
# Usage: ops/deploy.sh            deploy the working tree
#        ops/deploy.sh --status   show what is running
#        ops/deploy.sh --stop     stop production
# Env:   PROD_DIR  (default: ../production next to the repository)
#        PROD_PORT (default: 8088)

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PROD_DIR="${PROD_DIR:-$(dirname "${REPO}")/production}"
PROD_PORT="${PROD_PORT:-8088}"
PID_FILE="${PROD_DIR}/server.pid"
URL="http://127.0.0.1:${PROD_PORT}"

step() { printf '\n==> %s\n' "$*"; }
fail() {
	printf 'DEPLOY FAILED: %s\n' "$*" >&2
	exit 1
}

running_pid() {
	local pid
	[[ -f "${PID_FILE}" ]] || return 1
	pid="$(cat "${PID_FILE}")"
	kill -0 "${pid}" 2>/dev/null && echo "${pid}"
}

stop_server() {
	local pid
	if pid="$(running_pid)"; then
		kill "${pid}"
		for _ in $(seq 50); do
			kill -0 "${pid}" 2>/dev/null || break
			sleep 0.1
		done
	fi
	rm -f "${PID_FILE}"
}

start_server() {
	(
		cd "${PROD_DIR}/current"
		setsid nohup python3 -m tictactoe --host 127.0.0.1 --port "${PROD_PORT}" \
			>>"${PROD_DIR}/server.log" 2>&1 </dev/null &
		echo $! >"${PID_FILE}"
	)
}

smoke_test() {
	local health
	for _ in $(seq 50); do
		health="$(curl -fsS --max-time 1 "${URL}/health" 2>/dev/null)" && break
		sleep 0.1
	done
	[[ "${health:-}" == ok ]] || return 1
	curl -fsS --max-time 2 "${URL}/" | grep -qi '<html'
}

case "${1:-}" in
--status)
	if pid="$(running_pid)"; then
		echo "running: release $(basename "$(readlink "${PROD_DIR}/current")"), pid ${pid}, ${URL}"
	else
		echo "not running"
	fi
	exit 0
	;;
--stop)
	stop_server
	echo "stopped"
	exit 0
	;;
"") ;;
*) fail "unknown option: $1" ;;
esac

cd "${REPO}"

step "Gate 1/4: tests"
python3 -m pytest -q || fail "tests failed"

step "Gate 2/4: ruff check"
ruff check . || fail "lint findings"

step "Gate 3/4: ruff format --check"
ruff format --check . || fail "formatting"

step "Gate 4/4: reviews"
for change in changes/*/; do
	[[ -d "${change}" ]] || continue
	[[ -f "${change}review.md" ]] || fail "${change} has no review.md: it has not been reviewed"
	if grep -nE '^[[:space:]]*- \[ \] \*\*(blocker|major)\*\*' "${change}review.md"; then
		fail "unresolved blocker/major findings in ${change}review.md (above)"
	fi
	echo "${change}: no open blocker or major findings"
done

step "Release"
id="$(date +%Y%m%d-%H%M%S)"
release="${PROD_DIR}/releases/${id}"
[[ -e "${release}" ]] && fail "release ${id} already exists, try again in a second"
mkdir -p "${release}"
cp -r tictactoe "${release}/"
find "${release}" -name __pycache__ -prune -exec rm -rf {} +
commit="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
[[ -n "$(git status --porcelain 2>/dev/null)" ]] && commit+="-dirty"
echo "${commit}" >"${release}/COMMIT"
echo "release ${id} from commit ${commit}"

step "Switch"
previous=""
[[ -L "${PROD_DIR}/current" ]] && previous="$(readlink "${PROD_DIR}/current")"
stop_server
if curl -fsS --max-time 1 "${URL}/health" >/dev/null 2>&1; then
	fail "port ${PROD_PORT} is taken by something that is not production"
fi
ln -sfn "${release}" "${PROD_DIR}/current"
start_server
echo "started pid $(cat "${PID_FILE}")"

step "Smoke test"
if ! smoke_test; then
	echo "smoke test failed; last lines of server.log:" >&2
	tail -n 20 "${PROD_DIR}/server.log" >&2
	stop_server
	if [[ -n "${previous}" ]]; then
		ln -sfn "${previous}" "${PROD_DIR}/current"
		start_server
		if smoke_test; then
			echo "rolled back to $(basename "${previous}")" >&2
		else
			echo "rolled back to $(basename "${previous}"), but it did not come up either" >&2
		fi
	fi
	fail "release ${id} did not come up"
fi
echo "health ok, page ok"

printf '\nDEPLOYED release %s (commit %s) at %s\n' "${id}" "${commit}" "${URL}"
