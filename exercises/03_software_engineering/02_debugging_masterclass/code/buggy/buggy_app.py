
from typing import Any

# buggy_app.py
"""Application seeded with bugs for the debugging masterclass."""

def calculate_discount(price: float, discount_percent: float):
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount

def apply_bulk_discounts(items: list[dict[str, Any]]):
    results = []
    for item in items:
        discounted = calculate_discount(item['price'], item['discount'])
        results.append({
            'name': item['name'],
            'final_price': discounted
        })
    return results

def process_order(order_data: dict[str, list[dict[str, int | str] | dict[str, int | str | None]]]):
    items = order_data['items']
    discounted_items = apply_bulk_discounts(items)
    total = sum(item['final_price'] for item in discounted_items)
    return {
        'items': discounted_items,
        'total': total
    }

# Test code
order = {
    'items': [
        {'name': 'Widget', 'price': 100, 'discount': 10},
        {'name': 'Gadget', 'price': 200, 'discount': None},
        {'name': 'Doohickey', 'price': 50, 'discount': 5}
    ]
}

result = process_order(order)
print(result)
