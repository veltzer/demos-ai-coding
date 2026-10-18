# Bank payment file format (QBank batch upload v3)

Plain ASCII text. Every record is exactly **80 characters**, and every record,
including the last one, ends with **CRLF** (`\r\n`). Positions below are
1-based and inclusive. Alphanumeric fields are left-justified and padded with
spaces; numeric fields are right-justified and padded with zeros. Names and
references that are too long are truncated.

A file is: one file header, one payment record per payment (in input order),
one file control record, then blocking filler.

## 1. File header record

| Positions | Length | Content |
|-----------|--------|---------|
| 1 | 1 | `1` |
| 2-11 | 10 | company id |
| 12-19 | 8 | file date, `YYYYMMDD` |
| 20-23 | 4 | file sequence number |
| 24-80 | 57 | spaces |

## 2. Payment record

| Positions | Length | Content |
|-----------|--------|---------|
| 1 | 1 | `6` |
| 2-10 | 9 | routing number |
| 11-27 | 17 | account number |
| 28-37 | 10 | amount in cents, **absolute value** |
| 38 | 1 | `C` (credit) if the amount is zero or positive, `D` (debit) if negative |
| 39-60 | 22 | payee name, cleaned (see below) |
| 61-75 | 15 | reference |
| 76-80 | 5 | record sequence number: 1 for the first payment record, 2 for the next... |

### Payee name cleaning

1. Replace accented letters with their plain ASCII letter (`é` becomes `e`).
2. Convert to upper case.
3. Replace every character that is not `A-Z`, `0-9` or a space with a space.
4. Collapse runs of spaces into one space and strip leading/trailing spaces.
5. Truncate to 22 characters.

## 3. File control record

| Positions | Length | Content |
|-----------|--------|---------|
| 1 | 1 | `9` |
| 2-7 | 6 | number of payment records |
| 8-19 | 12 | total of the credit amounts, in cents |
| 20-31 | 12 | total of the debit amounts, in cents (absolute value) |
| 32-41 | 10 | entry hash (see below) |
| 42-80 | 39 | spaces |

**Entry hash:** take the first 8 digits of each payment's routing number as a
number, add them all up, and keep the last 10 digits of the sum.

## 4. Blocking

The total number of records (header + payment records + control) must be a
multiple of 10. Pad the end of the file with filler records consisting of 80
`9` characters each. If the count is already a multiple of 10, add no filler.

## 5. Validation

Raise `ValueError` if a routing number is not exactly 9 digits, or if an
account number is longer than 17 characters (never truncate an account).
