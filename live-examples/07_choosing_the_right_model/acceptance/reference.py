"""Reference implementation of docs/bankfile.md, used only by the hidden check."""

import re
import unicodedata

CRLF = "\r\n"


def clean_name(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    upper = re.sub(r"[^A-Z0-9 ]", " ", ascii_name.upper())
    return " ".join(upper.split())[:22]


def export_bank_file(payments, company_id, file_date, sequence):
    records = [f"1{company_id[:10]:<10}{file_date:%Y%m%d}{sequence:04d}".ljust(80)]
    credits = debits = entry_hash = 0
    for n, p in enumerate(payments, 1):
        if not re.fullmatch(r"\d{9}", p.routing):
            raise ValueError(f"bad routing number {p.routing!r}")
        if len(p.account) > 17:
            raise ValueError(f"account number too long {p.account!r}")
        kind = "C" if p.amount_cents >= 0 else "D"
        if kind == "C":
            credits += p.amount_cents
        else:
            debits += -p.amount_cents
        entry_hash += int(p.routing[:8])
        records.append(f"6{p.routing}{p.account:<17}{abs(p.amount_cents):010d}{kind}"
                       f"{clean_name(p.name):<22}{p.reference[:15]:<15}{n:05d}")
    records.append(f"9{len(payments):06d}{credits:012d}{debits:012d}{entry_hash % 10**10:010d}".ljust(80))
    while len(records) % 10:
        records.append("9" * 80)
    return "".join(r + CRLF for r in records)
