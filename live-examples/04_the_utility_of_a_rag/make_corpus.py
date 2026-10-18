#!/usr/bin/env python3
"""Generate the internal wiki of Quillstack, a company that does not exist.

Everything is fictional and generated from a fixed seed, so no model can
know it from training, every run produces the same wiki, and the true
answers to the demo questions are known exactly.

Usage: make_corpus.py <out-dir>
Writes <out-dir>/corpus/**/*.md and <out-dir>/questions.json.
"""

import json
import random
import sys
from pathlib import Path

RNG = random.Random(4242)

PREFIXES = ["ledger", "billing", "quota", "relay", "atlas", "ember", "harbor", "lumen", "nimbus",
            "orchid", "pylon", "quartz", "rivet", "saffron", "tundra", "vesper", "willow", "zephyr",
            "cobalt", "dune"]
SUFFIXES = ["sync", "gateway", "worker", "indexer", "scheduler", "proxy", "store", "notifier",
            "auth", "export"]
TEAMS = ["Payments Core", "Data Platform", "Edge Networking", "Identity", "Search Relevance",
         "Growth Infra", "Storage", "Observability", "Mobile Backend", "Developer Tools",
         "Risk & Fraud", "Messaging"]
FIRST = ["Ines", "Tomasz", "Priya", "Kofi", "Mei", "Rafael", "Hana", "Oskar", "Leila", "Dmitri",
         "Aiyana", "Bruno", "Sunniva", "Jae-won", "Farah", "Callum", "Noor", "Mateo", "Yuki", "Zainab"]
LAST = ["Okafor", "Lindqvist", "Ramaswamy", "Brennan", "Takahashi", "Moreau", "Kowalczyk", "Haddad",
        "Fernandes", "Ivanova", "Nakamura", "Achterberg", "Osei", "Quintero", "Varga", "Whitlock"]
# (text in the wiki, the key an answer must contain to count as correct)
DATASTORES = [("PostgreSQL 16 (cluster pg-main)", "pg-main"), ("PostgreSQL 16 (cluster pg-ledger)", "pg-ledger"),
              ("Cassandra (ring cass-east)", "cass-east"), ("Redis 7 (cluster cache-shared)", "cache-shared"),
              ("ClickHouse (cluster ch-analytics)", "ch-analytics"), ("S3 bucket qs-artifacts", "qs-artifacts"),
              ("DynamoDB table qs-sessions", "qs-sessions")]
CAUSES = [("the upstream token cache expired mid-request", "token cache"),
          ("a schema migration is still running", "migration"),
          ("the regional quota for the tenant is exhausted", "quota"),
          ("the request was signed with a rotated key", "rotated"),
          ("the idempotency key was reused with a different body", "idempotency"),
          ("the shard map is stale after a rebalance", "shard map"),
          ("the message exceeded the 256 KB broker limit", "256"),
          ("clock skew between nodes exceeded 2 seconds", "clock skew")]
LANGS = ["Go 1.23", "Kotlin 2.0", "Python 3.13", "Rust 1.82", "TypeScript (Node 22)"]


def person():
    return f"{RNG.choice(FIRST)} {RNG.choice(LAST)}"


def slug(text):
    return text.lower().replace(" & ", "-").replace(" ", "-")


def make_teams():
    teams = {}
    for name in TEAMS:
        teams[name] = {
            "lead": person(), "escalation": person(), "slack": f"#team-{slug(name)}",
            "rotation": f"rot-{slug(name)}-{RNG.randint(1, 9)}",
        }
    return teams


def make_services(teams):
    names = RNG.sample([f"{p}-{s}" for p in PREFIXES for s in SUFFIXES], 160)
    ports = RNG.sample(range(7000, 7999), 160)
    services = {}
    for name, port in zip(names, ports, strict=True):
        team = RNG.choice(TEAMS)
        services[name] = {
            "team": team, "prod_port": port, "staging_port": port + 1000,
            "datastore": RNG.choice(DATASTORES), "lang": RNG.choice(LANGS),
            "flag": f"{name.replace('-', '_')}_v{RNG.randint(2, 4)}",
            "slo": RNG.choice(["99.9%", "99.95%", "99.5%", "99.99%"]),
            "p99": RNG.choice([80, 120, 150, 200, 250, 400]),
            "deps": [],
        }
    for name, svc in services.items():
        svc["deps"] = RNG.sample([n for n in services if n != name], 3)
    return services


def make_errors(services):
    errors = {}
    for code in RNG.sample(range(1000, 4999), 600):
        svc = RNG.choice(list(services))
        cause, cause_key = RNG.choice(CAUSES)
        fix, fix_key = RNG.choice([
            (f"set flag `{services[svc]['flag']}` to off and retry", services[svc]["flag"]),
            (f"run `qsctl cache flush --service {svc}`", "cache flush"),
            (f"run `qsctl shard refresh --service {svc}`", "shard refresh"),
            (f"page the {services[svc]['team']} on-call", services[svc]["team"]),
        ])
        errors[f"QS-{code}"] = {"service": svc, "cause": cause, "fix": fix,
                                "keys": [cause_key, fix_key]}
    return errors


def write_team(path, name, t, services):
    owned = sorted(n for n, s in services.items() if s["team"] == name)
    path.write_text(f"""# Team: {name}

## People

- Team lead: {t['lead']}
- Escalation contact (Sev1/Sev2, after the on-call): {t['escalation']}
- Slack: {t['slack']}

## On-call

The team's pager rotation is `{t['rotation']}`. Hand-over is every Monday at
10:00 Europe/Lisbon. The secondary is always the previous week's primary.

## Services owned

{chr(10).join(f'- {n}' for n in owned) or '- (none yet)'}
""")


def write_service(path, name, s, teams):
    t = teams[s["team"]]
    path.write_text(f"""# Service: {name}

## Overview

{name} is written in {s['lang']} and owned by the {s['team']} team
(Slack {t['slack']}). It depends on {', '.join(s['deps'])}.

## Endpoints

| Environment | Host | Port |
|-------------|------|------|
| production | {name}.prod.qs.internal | {s['prod_port']} |
| staging | {name}.stg.qs.internal | {s['staging_port']} |

Health check: `GET /healthz` on the same port.

## Storage

Primary datastore: {s['datastore'][0]}. Backups follow the platform defaults
described in the data retention policy.

## Reliability

- SLO: {s['slo']} monthly availability
- Latency target: p99 below {s['p99']} ms
- Pager rotation: same as the owning team

## Feature flags

The current rollout flag is `{s['flag']}`. Turning it off reverts to the
previous code path without a deploy.

## Runbook

1. Check the dashboard `svc/{name}` in Grafana.
2. If error rates are above 2%, set `{s['flag']}` to off.
3. If the service is unhealthy, restart with `qsctl restart {name} --env prod`.
4. If that does not help within 15 minutes, page the owning team's rotation.
""")


def write_errors(directory, errors):
    codes = sorted(errors)
    for i in range(0, len(codes), 25):
        chunk = codes[i:i + 25]
        body = [f"# Error codes {chunk[0]} to {chunk[-1]}\n"]
        for code in chunk:
            e = errors[code]
            body.append(f"## {code}\n\nRaised by {e['service']}. Cause: {e['cause']}. "
                        f"Fix: {e['fix']}.\n")
        (directory / f"errors-{chunk[0]}.md").write_text("\n".join(body))


POLICIES = {
    "data-retention.md": """# Data retention policy

## Scope

Applies to every datastore that holds customer or operational data.

## Retention periods

- Application logs: 30 days in hot storage, then deleted.
- Audit logs: 2555 days (7 years), immutable, in the qs-audit bucket.
- Database backups: nightly, kept for 35 days; monthly snapshots kept 13 months.
- Deleted customer accounts: hard-deleted 45 days after the deletion request.

## Exceptions

Exceptions need written approval from the Data Protection Officer, Carmen Aldana.
""",
    "api-rate-limits.md": """# Public API rate limits

## Plans

| Plan | Requests per minute | Burst |
|------|---------------------|-------|
| Free | 60 | 20 |
| Team | 600 | 150 |
| Pro | 2400 | 600 |
| Enterprise | negotiated, default 10000 | 2500 |

## Behaviour

Over the limit, the API answers 429 with a `Retry-After` header. Limits are
per API key, not per IP. The search endpoints count double.
""",
    "deploys.md": """# Deploy policy

## Windows

Production deploys are allowed Monday to Thursday, 09:00 to 16:00
Europe/Lisbon. There is a deploy freeze every Friday from 12:00 until
Monday 09:00, and from December 20 to January 3.

## Process

Every deploy goes through `qsctl deploy <service> --env prod`, which runs the
canary at 5% for 20 minutes before the full rollout. A rollback is
`qsctl rollback <service>` and needs no approval.
""",
    "incidents.md": """# Incident severities

## Levels

- Sev1: customer-facing outage or data loss. Page the owning rotation and the
  incident commander rotation `rot-incident-cmd`. Status page within 15 minutes.
- Sev2: degraded service for many customers. Page the owning rotation.
- Sev3: minor or internal impact. Ticket in the team queue, next business day.

## After an incident

A blameless postmortem is due within 5 business days for Sev1 and Sev2.
""",
    "onboarding.md": """# Engineering onboarding

## First week

Get access through the IT portal, install qsctl with `brew install qs/tap/qsctl`,
and join #eng-announce. Your buddy will pair with you on your first deploy.

## Laptops

Engineers get a 16-inch laptop with 64 GB RAM. Replacement cycle is 3 years.
""",
}


def main():
    out = Path(sys.argv[1])
    corpus = out / "corpus"
    for sub in ("services", "teams", "errors", "policies"):
        (corpus / sub).mkdir(parents=True, exist_ok=True)

    teams = make_teams()
    services = make_services(teams)
    errors = make_errors(services)
    for name, t in teams.items():
        write_team(corpus / "teams" / f"{slug(name)}.md", name, t, services)
    for name, s in services.items():
        write_service(corpus / "services" / f"{name}.md", name, s, teams)
    write_errors(corpus / "errors", errors)
    for name, text in POLICIES.items():
        (corpus / "policies" / name).write_text(text)

    pick = random.Random(7)
    svc = pick.sample(sorted(services), 5)
    code = pick.choice(sorted(errors))
    hop = services[svc[4]]
    questions = [
        {"q": f"Which port does {svc[0]} listen on in staging?",
         "expect": [str(services[svc[0]]["staging_port"])]},
        {"q": f"Which team owns {svc[1]}?", "expect": [services[svc[1]]["team"]]},
        {"q": f"What is the primary datastore of {svc[2]}?",
         "expect": [services[svc[2]]["datastore"][1]]},
        {"q": f"What is the name of the rollout feature flag for {svc[3]}?",
         "expect": [services[svc[3]]["flag"]]},
        {"q": f"What causes error {code}, and how do I fix it?",
         "expect": errors[code]["keys"]},
        {"q": "How many requests per minute does the Pro plan allow on the public API?",
         "expect": ["2400"]},
        {"q": "How long are audit logs kept?", "expect": ["2555"]},
        {"q": "When does the weekly production deploy freeze start?", "expect": ["Friday", "12:00"]},
        {"q": f"Who is the escalation contact for the service listening on production port {hop['prod_port']}?",
         "expect": [teams[hop["team"]]["escalation"]], "note": "multi-hop: port -> service -> team"},
        {"q": "What is the parking policy at the Lisbon office?", "expect": ["UNKNOWN"],
         "note": "not in the wiki: the right answer is UNKNOWN"},
    ]
    (out / "questions.json").write_text(json.dumps(questions, indent=2))
    n_files = sum(1 for _ in corpus.rglob("*.md"))
    n_chars = sum(p.stat().st_size for p in corpus.rglob("*.md"))
    print(f"{n_files} documents, {n_chars:,} characters (~{n_chars // 4:,} tokens)")


if __name__ == "__main__":
    main()
