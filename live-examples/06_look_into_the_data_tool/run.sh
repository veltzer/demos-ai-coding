#!/usr/bin/env bash
# Demo 06: let the AI look at the data instead of guessing.
#
# Write a revenue query for a shop database. Both copies have the repo with
# the current, accurate schema.sql. The difference:
#   A - schema only:  no access to the database.
#   B - can look:     shop.db is there, and the AI may query it (read-only use).
# The schema is right, but the data holds surprises: an old importer's
# upper-case 'PAID', a 'staff_test' customer segment, JPY without cents, and an
# exchange-rate column whose direction only the numbers reveal.
# A hidden check tests each surprise separately and compares with the truth.
#
# Usage: ./run.sh [--yes]     --yes runs unattended (no pauses)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/common.sh
source "${HERE}/../lib/common.sh"

case "${1:-}" in
--yes) export YES=1 ;;
-h | --help)
	sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
	exit 0
	;;
"") ;;
*)
	echo "unknown option: $1 (try --help)" >&2
	exit 2
	;;
esac

require claude git python3 sqlite3

REQUEST="Write revenue.sql: a SQLite query for monthly revenue in USD per country for 2026, with the columns month (YYYY-MM), country (the country's name) and revenue_usd (rounded to 2 decimals), one row per month and country. Revenue means paid orders minus any refunds, converted to USD with that month's rate from fx_rates. Leave out our internal test accounts."

TOOLS=(--allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Bash(sqlite3:*)" "Bash(python3:*)")

make_workdir "${HERE}"
A="${WORKDIR}/A-schema-only"
B="${WORKDIR}/B-can-look"
DB="${WORKDIR}/shop.db"
python3 "${HERE}/make_db.py" "${DB}" >/dev/null
mkdir -p "${WORKDIR}/db-only"
cp "${DB}" "${WORKDIR}/db-only/shop.db"
copy_app "${HERE}/app" "${A}"
copy_app "${HERE}/app" "${B}" "${WORKDIR}/db-only"

banner "The repo: an analytics folder with an accurate schema"
(cd "${A}" && find . -maxdepth 1 -type f ! -name '.*' | sed 's|^\./|    |' | sort)
echo
sed -n '/CREATE TABLE customers/,/^);/p;/CREATE TABLE orders/,/^);/p;/CREATE TABLE fx_rates/,/^);/p' "${A}/schema.sql" | sed 's/^/    /'
pause "to see the request"

banner "The request (same for both)"
echo "  ${REQUEST}"
echo
say "Only B also gets shop.db, the nightly replica of production:"
echo
diff -rq --exclude=.git "${A}" "${B}" | sed "s|${WORKDIR}/||g; s/^/    /" || true
pause "to run A: schema only"

banner "A: schema only"
run_claude "${A}" "${WORKDIR}/A.json" "${REQUEST}" "${TOOLS[@]}"
pause "to run B: can look at the data"

banner "B: can look at the data"
run_claude "${B}" "${WORKDIR}/B.json" "${REQUEST}" "${TOOLS[@]}"
pause "to see what B looked at"

banner "What B looked at before writing the query"
python3 - "${WORKDIR}/B.json" <<'EOF'
import json, re, sys
seen = []
for command in json.load(open(sys.argv[1])).get("commands", []):
    for stmt in re.findall(r"(?is)\bselect\b.*?(?=;|\"|$)", command):
        one = " ".join(stmt.split())
        if "$" not in one and "sqlite_master" not in one and one not in seen and "revenue" not in one.lower():
            seen.append(one)
for one in seen[:12]:
    print("    " + (one if len(one) <= 110 else one[:109] + "…"))
if len(seen) > 12:
    print(f"    ... and {len(seen) - 12} more")
EOF
pause "to score both queries"

banner "Scoring against the real data"
for side in "${A}" "${B}"; do
	echo "${BOLD}$(basename "${side}")${RESET}"
	python3 "${HERE}/acceptance/check.py" "${side}" "${DB}" | tee "${side}.score" || true
	echo
done
say "Each surprise has its own check: the data is changed so that a correct query"
say "cannot tell the difference. If the answer moves, the query got that one wrong."
pause "for the scoreboard"

banner "Scoreboard"
score() { grep -o 'score: [0-9]*/[0-9]*' "$1.score" | cut -d' ' -f2; }
python3 "${LIB_DIR}/scoreboard.py" \
	"A schema only|$(score "${A}")|${WORKDIR}/A.json" \
	"B can look|$(score "${B}")|${WORKDIR}/B.json"
echo
say "The schema says what columns exist. Only the data says what is in them."
say "An AI that can run a query checks; one that can't has to guess."
say "Everything is in ${WORKDIR}"
echo "${GREEN}done${RESET}"
