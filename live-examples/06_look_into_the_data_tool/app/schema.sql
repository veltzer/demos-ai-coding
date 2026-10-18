-- shop.db: production replica, refreshed nightly.

CREATE TABLE countries (
    code TEXT PRIMARY KEY,          -- ISO 3166-1 alpha-2
    name TEXT NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    country_code TEXT NOT NULL REFERENCES countries(code),
    kind TEXT NOT NULL              -- customer segment
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    ordered_at TEXT NOT NULL,       -- ISO 8601, UTC
    status TEXT NOT NULL,
    currency TEXT NOT NULL,         -- ISO 4217
    total_minor INTEGER NOT NULL    -- order total in the currency's minor unit
);

CREATE TABLE refunds (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    refunded_at TEXT NOT NULL,
    amount_minor INTEGER NOT NULL
);

CREATE TABLE fx_rates (
    currency TEXT NOT NULL,
    month TEXT NOT NULL,            -- YYYY-MM
    rate REAL NOT NULL,             -- exchange rate for the month
    PRIMARY KEY (currency, month)
);
