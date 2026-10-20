# shellcheck shell=bash
# Shared helpers for the live demos. Source it, don't run it.
#
# Environment knobs (all optional):
#   YES=1        never pause, take the default answer everywhere
#   MODEL=...    model passed to claude (default: claude's own default)
#   WORKDIR=...  where the demo builds its throwaway copies
#                (default: ${TMPDIR:-/tmp}/demo-<demo folder>, reset on every run)

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BOLD=$'\033[1m'
DIM=$'\033[2m'
YELLOW=$'\033[33m'
# shellcheck disable=SC2034  # used by the demo scripts
GREEN=$'\033[32m'
RESET=$'\033[0m'

banner() {
	printf '\n%s━━━ %s %s%s\n\n' "${BOLD}${YELLOW}" "$1" "$(printf '━%.0s' $(seq 1 $((70 - ${#1}))))" "${RESET}"
}

say() {
	printf '%s%s%s\n' "${DIM}" "$*" "${RESET}"
}

pause() {
	[[ "${YES:-0}" == 1 ]] && return
	read -r -p "${DIM}[enter] ${1:-to continue}${RESET} " _
}

# ask "question" default -> echoes the answer (the default under YES=1)
ask() {
	local answer
	if [[ "${YES:-0}" == 1 ]]; then
		echo "$2"
		return
	fi
	read -r -p "$1 " answer
	echo "${answer:-$2}"
}

require() {
	local tool
	for tool in "$@"; do
		command -v "${tool}" >/dev/null || {
			echo "missing required tool: ${tool}" >&2
			exit 1
		}
	done
}

# make_workdir <demo-dir>: a fixed path named after the demo folder, so files
# like plan.md are easy to
# find and show while the demo runs. Wiped at the start of every run, but
# only if it carries our marker, never a directory we did not create.
make_workdir() {
	WORKDIR="${WORKDIR:-${TMPDIR:-/tmp}/demo-$(basename "$1")}"
	if [[ -e "${WORKDIR}" ]]; then
		if [[ ! -f "${WORKDIR}/.demo-workdir" ]]; then
			echo "${WORKDIR} exists and was not made by a demo - set WORKDIR= elsewhere" >&2
			exit 1
		fi
		rm -rf "${WORKDIR}"
	fi
	mkdir -p "${WORKDIR}"
	touch "${WORKDIR}/.demo-workdir"
}

# show_path <label> <path>: make a file the audience may want to see stand out.
show_path() {
	printf '\n  %s📄 %s:%s %s%s%s\n' "${BOLD}" "$1" "${RESET}" "${BOLD}${YELLOW}" "$2" "${RESET}"
}

# open_url <url-or-file>: show it in the desktop's browser, detached, so the
# terminal keeps the stage. VIEW=0 turns all browser windows off.
open_url() {
	[[ "${VIEW:-1}" == 0 ]] && return
	setsid -f xdg-open "$1" >/dev/null 2>&1 || true
}

# show_md <file.md> [title] [note]: render a markdown file to HTML with
# pandoc (GitHub-flavoured, code highlighted, inline <mark> kept) and open it
# in the browser. A note becomes a bar pinned to the top of the page, for
# telling the room what happens next. The page is a snapshot under
# ${WORKDIR}/view/; run it again to show a newer version of the same file.
show_md() {
	local md="$1" title="${2:-$(basename "$1")}" note="${3:-}" before html
	[[ "${VIEW:-1}" == 0 ]] && return
	mkdir -p "${WORKDIR}/view"
	html="${WORKDIR}/view/$(basename "${md%.md}").html"
	before="<div class=\"source\">${md}</div>"
	[[ -n "${note}" ]] && before="<div class=\"next\">${note}</div>${before}"
	if pandoc --standalone --embed-resources -f gfm -t html5 \
		--css "${LIB_DIR}/mdview.css" --metadata pagetitle="${title}" \
		-V include-before="${before}" \
		-o "${html}" "${md}" 2>/dev/null; then
		open_url "${html}"
	else
		say "(could not render ${md} with pandoc)"
	fi
}

# copy_app <src-dir> <dest-dir> [overlay-dir...]: a fresh copy, with each
# overlay copied on top, and a baseline commit so the AI's changes can be
# shown with git diff afterwards.
copy_app() {
	local overlay
	rm -rf "$2"
	cp -r "$1" "$2"
	for overlay in "${@:3}"; do
		cp -r "${overlay}/." "$2"
	done
	find "$2" -name __pycache__ -prune -exec rm -rf {} +
	git -C "$2" init -q
	# Keep bytecode out of the diffs without adding a file the AI would see.
	echo "__pycache__/" >>"$2/.git/info/exclude"
	git -C "$2" add -A
	git -C "$2" -c user.name=demo -c user.email=demo@example.invalid commit -qm baseline
}

# show_prompt <dir> <prompt-file> [extra claude args...]: the prompt as a
# readable box, with notes for the options the audience should know about.
show_prompt() {
	local dir="$1" file="$2" box_notes=() arg prev=""
	shift 2
	for arg in "$@"; do
		case "${prev}" in
		--model) box_notes+=("model: ${arg}") ;;
		--system-prompt) box_notes+=("system prompt: ${arg}") ;;
		--tools) [[ -z "${arg}" ]] && box_notes+=("no tools: it can only answer from the prompt") ;;
		*) ;;
		esac
		case "${arg}" in
		--continue | --resume) box_notes+=("continues the same conversation as before") ;;
		*) ;;
		esac
		prev="${arg}"
	done
	python3 "${LIB_DIR}/prompt_box.py" "Prompt to Claude, working in $(basename "${dir}")/" "${file}" "${box_notes[@]}"
}

# run_claude <dir> <stats-file> <prompt> [extra claude args...]
# Runs a headless session inside <dir> and renders it live. A prompt of
# "@<file>" is read from that file, for prompts too big for one argument.
# Only project settings are loaded so the presenter's personal CLAUDE.md,
# memory and hooks do not leak into the demo. claude's stderr (auth notices
# and the like) goes to <stats>.stderr to keep the stage clean.
run_claude() {
	local dir="$1" stats="$2" prompt="$3"
	shift 3
	local model_args=() input
	[[ -n "${MODEL:-}" ]] && model_args=(--model "${MODEL}")
	if [[ "${prompt}" == @* ]]; then
		input="${prompt#@}"
	else
		input="${stats%.json}.prompt"
		printf '%s\n' "${prompt}" >"${input}"
	fi
	show_prompt "${dir}" "${input}" "$@"
	(
		cd "${dir}" || exit
		claude -p \
			--output-format stream-json --verbose --include-partial-messages \
			--setting-sources project \
			--permission-mode acceptEdits \
			"${model_args[@]}" "$@" <"${input}" 2>>"${stats%.json}.stderr" |
			python3 "${LIB_DIR}/stream.py" --stats "${stats}"
	)
}

# snapshot <dir> <name>: commit whatever the AI changed and mark it with a
# branch (not a tag: tag.gpgSign-style user config would demand a message),
# so a later round can be diffed against it.
snapshot() {
	git -C "$1" add -A
	git -C "$1" -c user.name=demo -c user.email=demo@example.invalid commit -qm "$2" --allow-empty
	git -C "$1" branch "$2"
}
