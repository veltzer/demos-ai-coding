"""Customer e-mails. Delivery is someone else's service; we only queue."""

OUTBOX = []


def order_paid(store, order):
    customer = store.customers[order.customer_id]
    OUTBOX.append((customer.email, f"Order #{order.id} is paid, thank you {customer.name}!"))
