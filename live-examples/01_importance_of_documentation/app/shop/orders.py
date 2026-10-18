"""Order lifecycle."""

from shop import inventory, notifications
from shop.models import Order, Status


def create_order(store, customer_id, lines):
    order = Order(store.next_order_id(), customer_id, lines)
    store.add_order(order)
    return order


def pay(store, order):
    inventory.reserve(store, order)
    order.status = Status.PAID
    notifications.order_paid(store, order)


def cancel(store, order):
    if order.status is Status.PAID:
        inventory.release(store, order)
    order.status = Status.CANCELLED


def refund(store, order):
    inventory.release(store, order)
    order.status = Status.REFUNDED


def paid_orders(store, customer_id):
    return [o for o in store.orders_for(customer_id) if o.status is Status.PAID]
