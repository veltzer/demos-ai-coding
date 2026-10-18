"""Money helpers. Amounts are integer cents."""


def parse(text):
    """'12.30' -> 1230"""
    whole, _, frac = text.strip().partition(".")
    sign = -1 if whole.startswith("-") else 1
    return sign * (abs(int(whole or "0")) * 100 + int((frac + "00")[:2]))


def fmt(cents):
    """1230 -> '12.30'"""
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


def percent_of(cents, percent):
    """percent% of an amount, rounded down to a whole cent."""
    return cents * percent // 100
