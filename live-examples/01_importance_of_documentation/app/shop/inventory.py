"""Stock keeping."""

from shop import settings


class OutOfStock(Exception):
    pass


def reserve(store, order):
    for line in order.lines:
        if store.stock.get(line.sku, 0) < line.qty:
            raise OutOfStock(line.sku)
    for line in order.lines:
        store.stock[line.sku] -= line.qty


def release(store, order):
    for line in order.lines:
        store.stock[line.sku] = store.stock.get(line.sku, 0) + line.qty


def low_stock(store):
    return sorted(sku for sku, n in store.stock.items() if n <= settings.LOW_STOCK_WARNING)
