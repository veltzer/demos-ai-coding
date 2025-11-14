def process_order(order_data):
    # Validate order
    if not order_data.get('customer_id'):
        return {"error": "Missing customer ID"}
    if not order_data.get('items'):
        return {"error": "No items in order"}

    # Calculate totals
    subtotal = 0
    for item in order_data['items']:
        if item['quantity'] <= 0:
            return {"error": "Invalid quantity"}
        subtotal += item['price'] * item['quantity']

    # Apply discount
    discount = 0
    if order_data.get('discount_code'):
        code = order_data['discount_code']
        if code == 'SAVE10':
            discount = subtotal * 0.10
        elif code == 'SAVE20':
            discount = subtotal * 0.20
        elif code == 'SUMMER':
            discount = subtotal * 0.15
        else:
            return {"error": "Invalid discount code"}

    # Calculate tax
    tax_rate = 0.08
    if order_data.get('state') == 'CA':
        tax_rate = 0.0875
    elif order_data.get('state') == 'NY':
        tax_rate = 0.04
    tax = (subtotal - discount) * tax_rate

    # Check inventory
    for item in order_data['items']:
        inventory = db.query("SELECT quantity FROM inventory WHERE product_id = ?", item['product_id'])
        if not inventory or inventory[0]['quantity'] < item['quantity']:
            return {"error": f"Insufficient inventory for {item['name']}"}

    # Process payment
    total = subtotal - discount + tax
    payment_result = stripe.charge(
        amount=int(total * 100),
        currency='usd',
        customer=order_data['customer_id']
    )
    if not payment_result.success:
        return {"error": "Payment failed"}

    # Update inventory
    for item in order_data['items']:
        db.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?",
            item['quantity'], item['product_id']
        )

    # Create order record
    order_id = db.insert('orders', {
        'customer_id': order_data['customer_id'],
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'status': 'completed'
    })

    # Send confirmation email
    email_service.send(
        to=order_data['customer_email'],
        subject='Order Confirmation',
        body=generate_confirmation_email(order_data, order_id)
    )

    return {"success": True, "order_id": order_id}
