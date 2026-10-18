# Demo 06: look into the data tool

```bash
./run.sh          # interactive, pauses between steps so you can talk
./run.sh --yes    # unattended dry run
```

## What happens

`make_db.py` builds `shop.db`, a fictional production replica (240
customers, about 1,400 orders over 2026), from a fixed seed. Two copies of an
analytics repo get the same request: a SQLite query for monthly revenue in USD
per country, paid orders minus refunds, converted with `fx_rates`, without
internal test accounts.

- **A, schema only**: `schema.sql` (accurate and current) and a README.
- **B, can look**: the same, plus `shop.db`, which the AI may query.

After both runs the script lists the queries B ran to look at the data, then
scores both queries.

## The surprises: in the data, not the schema

| Surprise | The schema says | The data shows |
|----------|-----------------|----------------|
| status | `status TEXT` | `paid` and an old importer's `PAID` |
| test accounts | `kind TEXT -- customer segment` | `retail`, `business`, `staff_test` |
| money | `total_minor -- the currency's minor unit` | JPY orders: yen has no minor unit |
| exchange rate | `rate REAL -- exchange rate for the month` | EUR 0.92, JPY 150: per USD, so divide |

## Scoring

`acceptance/check.py` runs the query against `shop.db` and gives each surprise
its own **invariance test**: a copy of the database is changed so that a
correct query cannot tell the difference (`PAID` rewritten as `paid`, test
accounts' orders deleted, refunds folded into the totals, JPY or EUR/GBP
orders converted to USD). If the answer moves, the query got that surprise
wrong. A final check compares every number with a reference query.

Rehearsal: **A 5/8, B 8/8**. A got yen and the rate direction right (or
lucky), but counted only `paid` and kept the test accounts: it reported
**$130K instead of $141K**. An 8% error looks plausible, and nobody would
catch it in a meeting. B ran about twenty `SELECT DISTINCT`-style queries
first and matched every number.

## Talking points

- The schema was right. It just doesn't tell you what is in the columns.
- A without access is not careless: often it builds a fake database from
  `schema.sql` to test its query. The query runs fine, and the numbers are
  still wrong.
- Show "What B looked at": `SELECT DISTINCT status`, `kind`, the currencies
  and a few rates. It is what a careful analyst does in the first five minutes.
- In real life, a data tool means a read-only database connection, an MCP
  server, or a sample export: any way for the AI to check instead of assume.

## Files

- `app/`: the analytics repo (`schema.sql`, `README.md`)
- `make_db.py`: builds `shop.db` with the surprises
- `acceptance/check.py`: the reference query and the invariance tests
- Work dir `/tmp/demo-06_look_into_the_data_tool/`: both copies, `shop.db` and the logs
