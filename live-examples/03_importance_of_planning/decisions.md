
## Decisions (from the human - these override anything above)

- Categories ignore case and surrounding spaces: "Food", " FOOD " and "food"
  are one category, shown in lowercase.
- Refunds (negative amounts) are subtracted from their category.
- Hide categories whose total for the month is exactly zero.
- Sort by total, largest first; break ties alphabetically.
- Finish with a `total` line.
- `--month YYYY-MM` is optional. Without it, report the most recent month
  that has data - not the current calendar month.
- Sum money with `decimal.Decimal`, never float.
