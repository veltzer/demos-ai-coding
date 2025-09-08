#!/usr/bin/env python3
import argparse
import csv
import math
import os
import random
import sys
from typing import Iterator, Dict, List, Optional

try:
    from faker import Faker
except ImportError:
    print("Missing dependency: faker. Install with: pip install faker", file=sys.stderr)
    sys.exit(1)

# Optional Parquet support (pyarrow)
try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAVE_PARQUET = True
except Exception:
    HAVE_PARQUET = False


MARITAL_STATUSES = ["single", "married", "divorced", "widowed"]

def choose_marital_status(rng: random.Random, age: int) -> str:
    # Simple age-informed probabilities (tweak as needed)
    if age < 22:
        weights = [0.94, 0.04, 0.01, 0.01]
    elif age < 30:
        weights = [0.6, 0.35, 0.03, 0.02]
    elif age < 45:
        weights = [0.25, 0.65, 0.07, 0.03]
    elif age < 65:
        weights = [0.15, 0.7, 0.1, 0.05]
    else:
        weights = [0.1, 0.65, 0.1, 0.15]
    return rng.choices(MARITAL_STATUSES, weights=weights, k=1)[0]

def sample_age(rng: random.Random) -> int:
    # Skew towards working-age adults. Triangular distribution works well.
    # min=18, mode=32, max=90
    return int(rng.triangular(18, 90, 32))

def sample_children(rng: random.Random, age: int, marital_status: str) -> int:
    if age < 22:
        return 0
    # Base weights for number of children 0..5
    # Adjusted by marital status and age
    if marital_status == "single":
        weights = [0.85, 0.1, 0.04, 0.009, 0.0009, 0.0001]
    elif marital_status == "married":
        if age < 30:
            weights = [0.5, 0.35, 0.12, 0.027, 0.0028, 0.0002]
        elif age < 40:
            weights = [0.25, 0.35, 0.28, 0.1, 0.02, 0.005]
        elif age < 55:
            weights = [0.2, 0.3, 0.3, 0.15, 0.04, 0.01]
        else:
            weights = [0.2, 0.3, 0.3, 0.15, 0.04, 0.01]
    elif marital_status == "divorced":
        weights = [0.45, 0.3, 0.18, 0.06, 0.01, 0.005]
    else:  # widowed
        weights = [0.4, 0.3, 0.2, 0.08, 0.015, 0.005]
    return rng.choices([0, 1, 2, 3, 4, 5], weights=weights, k=1)[0]

def generate_people(
    n: int,
    locale: str,
    seed: Optional[int],
    with_progress: bool = True
) -> Iterator[Dict[str, object]]:
    rng = random.Random(seed)
    fake = Faker(locale=locale)
    if seed is not None:
        Faker.seed(seed)

    for i in range(n):
        age = sample_age(rng)
        marital_status = choose_marital_status(rng, age)
        children = sample_children(rng, age, marital_status)
        person = {
            "name": fake.first_name(),
            "family_name": fake.last_name(),
            "marital_status": marital_status,
            "age": age,
            "number_of_children": children,
        }
        if with_progress and (i + 1) % 100000 == 0:
            print(f"Generated {i+1}/{n} rows...", file=sys.stderr)
        yield person

def write_csv(path: str, rows: Iterator[Dict[str, object]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "family_name", "marital_status", "age", "number_of_children"]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def write_parquet(path: str, rows: Iterator[Dict[str, object]], chunk_size: int = 100_000) -> None:
    if not HAVE_PARQUET:
        print("Parquet support requires pyarrow. Install with: pip install pyarrow", file=sys.stderr)
        sys.exit(1)

    schema = pa.schema([
        ("name", pa.string()),
        ("family_name", pa.string()),
        ("marital_status", pa.string()),
        ("age", pa.int16()),
        ("number_of_children", pa.int8()),
    ])

    writer = None
    try:
        batch: Dict[str, List] = {
            "name": [],
            "family_name": [],
            "marital_status": [],
            "age": [],
            "number_of_children": [],
        }
        count = 0
        for row in rows:
            for k in batch:
                batch[k].append(row[k])
            count += 1

            if count % chunk_size == 0:
                table = pa.Table.from_pydict(batch, schema=schema)
                if writer is None:
                    writer = pq.ParquetWriter(path, table.schema, compression="zstd")
                writer.write_table(table)
                for k in batch:
                    batch[k].clear()

        if batch["name"]:
            table = pa.Table.from_pydict(batch, schema=schema)
            if writer is None:
                writer = pq.ParquetWriter(path, table.schema, compression="zstd")
            writer.write_table(table)
    finally:
        if writer is not None:
            writer.close()

def main():
    parser = argparse.ArgumentParser(description="Generate fake people data.")
    parser.add_argument("-n", "--num", type=int, default=1_000_000, help="Number of records to generate")
    parser.add_argument("-o", "--out", type=str, default="people.csv", help="Output file path")
    parser.add_argument("-f", "--format", choices=["csv", "parquet"], default="csv", help="Output format")
    parser.add_argument("-l", "--locale", type=str, default="en_US", help="Faker locale (e.g., en_US, fr_FR, he_IL)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress messages")
    args = parser.parse_args()

    rows_iter = generate_people(args.num, args.locale, args.seed, with_progress=not args.no_progress)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    if args.format == "csv":
        write_csv(args.out, rows_iter)
    else:
        write_parquet(args.out, rows_iter)

    print(f"Done. Wrote {args.num} rows to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()