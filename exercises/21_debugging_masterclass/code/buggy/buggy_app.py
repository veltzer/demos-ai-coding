# buggy_app.py
def calculate_discount(price, discount_percent):
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price

def apply_bulk_discounts(items):
    results = []
    for item in items:
        discounted = calculate_discount(item['price'], item['discount'])
        results.append({
            'name': item['name'],
            'final_price': discounted
        })
    return results

def process_order(order_data):
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
