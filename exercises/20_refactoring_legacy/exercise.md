# Refactoring Legacy Code with AI: From Chaos to Clean

## Learning Objective
Learn how to systematically refactor legacy code using AI assistance. Identify code smells, apply refactoring patterns, maintain backward compatibility, and improve code quality while preserving functionality.

## What is Legacy Code?

Legacy code is code that:
- Works but is hard to understand
- Lacks tests
- Has accumulated technical debt
- Uses outdated patterns or practices
- Scares developers away from changing it

**Michael Feathers' Definition:** "Legacy code is code without tests."

## Prerequisites
- Understanding of SOLID principles
- Familiarity with design patterns
- Basic testing knowledge
- GitHub Copilot or similar AI assistant

---

## Part 1: Identifying Code Smells

### Common Code Smells

#### Smell 1: God Class (Does Too Much)

**Before - The Problem:**

```python
# user_manager.py - A 500-line god class
class UserManager:
    def __init__(self):
        self.db = MySQLConnection()
        self.cache = RedisConnection()
        self.email_service = SMTPService()
        self.logger = Logger()
        self.session_store = SessionStore()
        self.file_storage = S3Storage()

    def create_user(self, data):
        # Validate email
        if not '@' in data['email']:
            raise ValueError("Invalid email")

        # Check if user exists
        existing = self.db.query("SELECT * FROM users WHERE email = ?", data['email'])
        if existing:
            raise ValueError("User exists")

        # Hash password
        import hashlib
        hashed = hashlib.md5(data['password'].encode()).hexdigest()
        data['password'] = hashed

        # Insert into database
        user_id = self.db.insert("users", data)

        # Clear cache
        self.cache.delete_pattern("users:*")

        # Send welcome email
        self.email_service.send(
            to=data['email'],
            subject="Welcome!",
            body=self.generate_welcome_email(data)
        )

        # Create session
        session_id = self.session_store.create(user_id)

        # Upload default avatar
        avatar_url = self.file_storage.upload_default_avatar(user_id)
        self.db.update("users", user_id, {"avatar_url": avatar_url})

        # Log action
        self.logger.info(f"User created: {user_id}")

        return user_id

    def login_user(self, email, password):
        # ... another 50 lines of mixed concerns

    def update_profile(self, user_id, data):
        # ... another 50 lines

    def delete_user(self, user_id):
        # ... another 50 lines

    def reset_password(self, email):
        # ... another 50 lines

    def generate_welcome_email(self, user_data):
        # ... email template logic

    # ... 10 more methods mixing all concerns
```

**Exercise 1.1:** Ask AI to identify all the responsibilities this class has.

**Prompt:**

```txt
Analyze this UserManager class and list all the distinct responsibilities it has.
Group them by concern (database, email, validation, etc.).
```

**Exercise 1.2:** Use AI to refactor into separate classes.

**Prompt:**

```txt
Refactor this god class into multiple focused classes following Single Responsibility Principle.
Create:
- UserValidator for validation logic
- UserRepository for database operations
- EmailService for email operations
- UserService for orchestrating user operations
- Keep each class focused on one responsibility
```

**Expected Result:**

```python
# validators.py
class UserValidator:
    def validate_email(self, email: str) -> None:
        if not '@' in email:
            raise ValueError("Invalid email")

    def validate_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password too short")

# repositories.py
class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.query("SELECT * FROM users WHERE email = ?", email)

    def create(self, user_data: dict) -> int:
        return self.db.insert("users", user_data)

# services.py
class EmailService:
    def send_welcome_email(self, user_email: str, user_name: str):
        # Focused on email sending only

class UserService:
    def __init__(self, repository, validator, email_service, cache):
        self.repository = repository
        self.validator = validator
        self.email_service = email_service
        self.cache = cache

    def create_user(self, data: dict) -> int:
        self.validator.validate_email(data['email'])
        # ... orchestrates the operations
```

---

#### Smell 2: Long Method

**Before:**

```python
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
```

**Exercise 1.3:** Refactor long method into smaller, focused methods.

**Prompt:**

```txt
Refactor this long process_order function by extracting smaller methods.
Each extracted method should:
- Have a single, clear purpose
- Be named descriptively
- Be no more than 10-15 lines
- Follow the Single Responsibility Principle

Extract methods for:
- Validation
- Total calculation
- Discount application
- Tax calculation
- Inventory checking
- Payment processing
- Order creation
```

---

#### Smell 3: Duplicated Code

**Before:**

```python
def get_active_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE active = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_premium_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE premium = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_verified_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE verified = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
```

**Exercise 1.4:** Eliminate duplication.

**Prompt:**

```txt
Refactor these three functions to eliminate code duplication.
Create a generic query function that all three can use.
Use a context manager for database connection management.
```

---

#### Smell 4: Primitive Obsession

**Before:**

```python
def create_user(name: str, email: str, birthdate: str, phone: str, address: str):
    # Using primitives instead of objects
    if not validate_email_format(email):
        raise ValueError("Invalid email")
    if not validate_phone_format(phone):
        raise ValueError("Invalid phone")
    # ... lots of validation logic for primitives
```

**After - Use Value Objects:**

```python
class Email:
    def __init__(self, value: str):
        if not '@' in value:
            raise ValueError("Invalid email")
        self.value = value

    def __str__(self):
        return self.value

class Phone:
    def __init__(self, value: str):
        cleaned = re.sub(r'\D', '', value)
        if len(cleaned) != 10:
            raise ValueError("Invalid phone")
        self.value = cleaned

    def formatted(self):
        return f"({self.value[:3]}) {self.value[3:6]}-{self.value[6:]}"

def create_user(name: str, email: Email, phone: Phone, ...):
    # Email and Phone are already validated
    # Much cleaner interface
```

**Exercise 1.5:** Identify primitives that should be objects.

---

#### Smell 5: Feature Envy

**Before:**

```python
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

class OrderPrinter:
    def print_order(self, order):
        # This method knows too much about Order internals
        print(f"Customer: {order.customer.name}")
        print(f"Email: {order.customer.email}")
        print(f"Address: {order.customer.address.street}, {order.customer.address.city}")
        print("Items:")
        for item in order.items:
            print(f"  {item.name}: ${item.price} x {item.quantity}")
        total = sum(item.price * item.quantity for item in order.items)
        print(f"Total: ${total}")
```

**After - Move behavior to where the data is:**

```python
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def calculate_total(self):
        return sum(item.subtotal() for item in self.items)

    def format_for_printing(self):
        lines = []
        lines.append(f"Customer: {self.customer.format_name()}")
        lines.append(f"Email: {self.customer.email}")
        lines.append(f"Address: {self.customer.format_address()}")
        lines.append("Items:")
        for item in self.items:
            lines.append(f"  {item.format()}")
        lines.append(f"Total: ${self.calculate_total()}")
        return "\n".join(lines)

class OrderPrinter:
    def print_order(self, order):
        print(order.format_for_printing())
```

---

## Part 2: Systematic Refactoring Process

### The Golden Rule of Refactoring

**Before refactoring: Add tests!**

If legacy code has no tests, you must add characterization tests first.

### Step 1: Characterization Testing

**Exercise 2.1:** Write tests for existing behavior.

```python
# Legacy code without tests
def calculate_shipping(weight, distance, is_express):
    if is_express:
        base = 15.00
    else:
        base = 5.00

    if weight > 10:
        base += (weight - 10) * 0.5

    if distance > 100:
        base += (distance - 100) * 0.1

    return base

# Step 1: Characterize current behavior with tests
def test_calculate_shipping_standard():
    assert calculate_shipping(5, 50, False) == 5.00

def test_calculate_shipping_express():
    assert calculate_shipping(5, 50, True) == 15.00

def test_calculate_shipping_heavy():
    assert calculate_shipping(15, 50, False) == 7.50

def test_calculate_shipping_long_distance():
    assert calculate_shipping(5, 150, False) == 10.00

def test_calculate_shipping_heavy_and_far():
    assert calculate_shipping(15, 150, True) == 22.50

# Now we can safely refactor with confidence!
```

---

### Step 2: Small, Safe Refactorings

**Exercise 2.2:** Refactor in tiny steps.

**Before:**
```python
def process_data(data):
    result = []
    for item in data:
        if item['status'] == 'active' and item['value'] > 0:
            result.append(item['name'].upper())
    return result
```

**Step 2a - Extract variable:**
```python
def process_data(data):
    result = []
    for item in data:
        is_valid = item['status'] == 'active' and item['value'] > 0
        if is_valid:
            result.append(item['name'].upper())
    return result
```

**Step 2b - Extract method:**
```python
def is_valid_item(item):
    return item['status'] == 'active' and item['value'] > 0

def process_data(data):
    result = []
    for item in data:
        if is_valid_item(item):
            result.append(item['name'].upper())
    return result
```

**Step 2c - Use list comprehension:**
```python
def is_valid_item(item):
    return item['status'] == 'active' and item['value'] > 0

def process_item_name(item):
    return item['name'].upper()

def process_data(data):
    return [process_item_name(item) for item in data if is_valid_item(item)]
```

---

## Part 3: Real Legacy Code Examples

### Example 1: The 1000-Line Controller

**Before - app.py:**

```python
from flask import Flask, request, session, jsonify
import mysql.connector
import hashlib
import smtplib
from datetime import datetime, timedelta
import stripe
import boto3

app = Flask(__name__)
app.secret_key = 'hardcoded_secret'

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    # Validation
    if not data.get('email'):
        return jsonify({"error": "Email required"}), 400
    if not '@' in data['email']:
        return jsonify({"error": "Invalid email"}), 400
    if not data.get('password'):
        return jsonify({"error": "Password required"}), 400
    if len(data['password']) < 6:
        return jsonify({"error": "Password too short"}), 400

    # Database connection
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='myapp'
    )
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "User exists"}), 400

    # Hash password
    password_hash = hashlib.md5(data['password'].encode()).hexdigest()

    # Insert user
    cursor.execute(
        "INSERT INTO users (email, password, created_at) VALUES (%s, %s, %s)",
        (data['email'], password_hash, datetime.now())
    )
    conn.commit()
    user_id = cursor.lastrowid

    # Send welcome email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('app@example.com', 'password')
    message = f"Welcome to our app! Your user ID is {user_id}"
    smtp.sendmail('app@example.com', data['email'], message)
    smtp.quit()

    cursor.close()
    conn.close()

    return jsonify({"user_id": user_id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    # Another 100 lines...

@app.route('/api/profile', methods=['GET', 'PUT'])
def profile():
    # Another 100 lines...

# ... 900 more lines of mixed concerns
```

**Exercise 3.1:** Refactor this monolithic controller.

**Prompt:**

```txt
Refactor this Flask application following these principles:

1. Separate concerns:
   - Create models.py for database models
   - Create validators.py for validation logic
   - Create services.py for business logic
   - Create repositories.py for database access
   - Keep controllers thin

2. Use dependency injection

3. Extract configuration to config.py

4. Use proper password hashing (bcrypt, not MD5!)

5. Use environment variables for secrets

6. Add proper error handling

7. Create a proper application factory pattern
```

**Expected Structure After Refactoring:**

```txt
app/
+-- __init__.py
+-- config.py
+-- models/
|   +-- __init__.py
|   +-- user.py
+-- repositories/
|   +-- __init__.py
|   +-- user_repository.py
+-- services/
|   +-- __init__.py
|   +-- auth_service.py
|   +-- email_service.py
+-- validators/
|   +-- __init__.py
|   +-- user_validator.py
+-- controllers/
|   +-- __init__.py
|   +-- auth_controller.py
+-- tests/
    +-- ...
```

---

### Example 2: Spaghetti Code with No Structure

**Before:**

```python
# data_processor.py - 500 lines of procedural spaghetti

def main():
    # Read config
    config = {}
    with open('config.txt') as f:
        for line in f:
            parts = line.strip().split('=')
            config[parts[0]] = parts[1]

    # Connect to database
    import psycopg2
    conn = psycopg2.connect(
        host=config['db_host'],
        user=config['db_user'],
        password=config['db_pass']
    )
    cursor = conn.cursor()

    # Read data from API
    import requests
    response = requests.get(config['api_url'])
    data = response.json()

    # Process data
    processed = []
    for item in data:
        if item.get('status') == 'active':
            # Calculate score
            score = 0
            if item['views'] > 100:
                score += 10
            if item['likes'] > 50:
                score += 5
            if item['comments'] > 20:
                score += 3

            # Categorize
            if score > 15:
                category = 'hot'
            elif score > 10:
                category = 'trending'
            else:
                category = 'normal'

            # Transform data
            processed_item = {
                'id': item['id'],
                'title': item['title'].upper(),
                'score': score,
                'category': category,
                'processed_at': datetime.now().isoformat()
            }

            processed.append(processed_item)

            # Insert into database
            cursor.execute(
                """INSERT INTO processed_items
                   (id, title, score, category, processed_at)
                   VALUES (%s, %s, %s, %s, %s)""",
                (
                    processed_item['id'],
                    processed_item['title'],
                    processed_item['score'],
                    processed_item['category'],
                    processed_item['processed_at']
                )
            )

    conn.commit()

    # Generate report
    report = "Processing Report\n"
    report += "=" * 50 + "\n"
    report += f"Total items processed: {len(processed)}\n"
    hot = sum(1 for item in processed if item['category'] == 'hot')
    trending = sum(1 for item in processed if item['category'] == 'trending')
    normal = sum(1 for item in processed if item['category'] == 'normal')
    report += f"Hot items: {hot}\n"
    report += f"Trending items: {trending}\n"
    report += f"Normal items: {normal}\n"

    # Send email report
    import smtplib
    # ... 50 more lines of email logic

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
```

**Exercise 3.2:** Transform procedural spaghetti into OOP.

**Prompt:**

```txt
Refactor this procedural spaghetti code into a clean OOP structure:

1. Create classes for:
   - ConfigLoader
   - DataFetcher
   - DataProcessor (with ScoreCalculator, Categorizer)
   - DatabaseWriter
   - ReportGenerator
   - EmailSender

2. Each class should:
   - Have a single responsibility
   - Use dependency injection
   - Be testable

3. Create a main orchestrator class that coordinates

4. Extract all magic numbers into constants

5. Add type hints

6. Add docstrings

7. Make it extensible for new data sources
```

---

### Example 3: Tight Coupling Nightmare

**Before:**

```python
class OrderProcessor:
    def process_order(self, order_data):
        # Tightly coupled to specific implementations
        db = MySQLDatabase()  # Hard-coded dependency
        payment = StripePayment()  # Hard-coded dependency
        shipping = FedExShipping()  # Hard-coded dependency
        email = GmailSender()  # Hard-coded dependency

        # Validate
        if not order_data.get('items'):
            raise ValueError("No items")

        # Calculate total
        total = sum(item['price'] * item['qty'] for item in order_data['items'])

        # Process payment
        payment_result = payment.charge(order_data['card'], total)
        if not payment_result:
            raise Exception("Payment failed")

        # Save to database
        order_id = db.insert('orders', {
            'customer': order_data['customer'],
            'total': total,
            'status': 'paid'
        })

        # Arrange shipping
        tracking = shipping.create_shipment(
            order_data['address'],
            order_data['items']
        )

        # Send confirmation
        email.send(
            to=order_data['customer']['email'],
            subject='Order Confirmation',
            body=f'Your order {order_id} is confirmed'
        )

        return order_id
```

**Exercise 3.3:** Decouple using dependency injection.

**Prompt:**

```txt
Refactor this tightly coupled class to use dependency injection:

1. Create interfaces (protocols) for:
   - PaymentProcessor
   - ShippingProvider
   - EmailSender
   - OrderRepository

2. Inject dependencies through constructor

3. Make it easy to swap implementations

4. Add factory pattern for creating configured OrderProcessor

5. Make it testable with mock implementations
```

---

## Part 4: Refactoring Patterns

### Pattern 1: Extract Method

**Before:**

```python
def print_invoice(invoice):
    # Print header
    print("*" * 50)
    print(f"Invoice #{invoice.number}")
    print(f"Date: {invoice.date}")
    print(f"Customer: {invoice.customer.name}")
    print("*" * 50)

    # Print items
    print("\nItems:")
    for item in invoice.items:
        print(f"  {item.description:30} ${item.amount:>10.2f}")

    # Print totals
    subtotal = sum(item.amount for item in invoice.items)
    tax = subtotal * 0.08
    total = subtotal + tax
    print("\n" + "-" * 50)
    print(f"Subtotal: ${subtotal:>10.2f}")
    print(f"Tax (8%): ${tax:>10.2f}")
    print(f"Total:    ${total:>10.2f}")
```

**After:**

```python
def print_invoice(invoice):
    print_header(invoice)
    print_items(invoice.items)
    print_totals(invoice)

def print_header(invoice):
    print("*" * 50)
    print(f"Invoice #{invoice.number}")
    print(f"Date: {invoice.date}")
    print(f"Customer: {invoice.customer.name}")
    print("*" * 50)

def print_items(items):
    print("\nItems:")
    for item in items:
        print(f"  {item.description:30} ${item.amount:>10.2f}")

def print_totals(invoice):
    subtotal = calculate_subtotal(invoice)
    tax = calculate_tax(subtotal)
    total = subtotal + tax

    print("\n" + "-" * 50)
    print(f"Subtotal: ${subtotal:>10.2f}")
    print(f"Tax (8%): ${tax:>10.2f}")
    print(f"Total:    ${total:>10.2f}")
```

### Pattern 2: Replace Conditional with Polymorphism

**Before:**

```python
class Employee:
    def __init__(self, name, employee_type):
        self.name = name
        self.type = employee_type

def calculate_pay(employee, hours):
    if employee.type == 'hourly':
        return hours * 15
    elif employee.type == 'salaried':
        return 5000
    elif employee.type == 'commissioned':
        return 3000 + (hours * 10)
    else:
        raise ValueError("Unknown type")
```

**After:**

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_pay(self, hours):
        pass

class HourlyEmployee(Employee):
    def calculate_pay(self, hours):
        return hours * 15

class SalariedEmployee(Employee):
    def calculate_pay(self, hours):
        return 5000

class CommissionedEmployee(Employee):
    def calculate_pay(self, hours):
        return 3000 + (hours * 10)
```

### Pattern 3: Replace Magic Numbers with Constants

**Before:**

```python
def calculate_shipping(weight, distance):
    if weight > 10:
        cost = 15.00
    else:
        cost = 5.00

    if distance > 100:
        cost += distance * 0.15
    else:
        cost += distance * 0.10

    if cost > 50:
        cost = 50  # Maximum shipping

    return cost
```

**After:**

```python
class ShippingConstants:
    HEAVY_WEIGHT_THRESHOLD = 10
    LIGHT_PACKAGE_BASE = 5.00
    HEAVY_PACKAGE_BASE = 15.00

    LONG_DISTANCE_THRESHOLD = 100
    SHORT_DISTANCE_RATE = 0.10
    LONG_DISTANCE_RATE = 0.15

    MAXIMUM_SHIPPING_COST = 50.00

def calculate_shipping(weight, distance):
    base_cost = (ShippingConstants.HEAVY_PACKAGE_BASE
                 if weight > ShippingConstants.HEAVY_WEIGHT_THRESHOLD
                 else ShippingConstants.LIGHT_PACKAGE_BASE)

    distance_rate = (ShippingConstants.LONG_DISTANCE_RATE
                     if distance > ShippingConstants.LONG_DISTANCE_THRESHOLD
                     else ShippingConstants.SHORT_DISTANCE_RATE)

    total_cost = base_cost + (distance * distance_rate)

    return min(total_cost, ShippingConstants.MAXIMUM_SHIPPING_COST)
```

---

## Part 5: Complete Refactoring Project

### Project: Legacy E-commerce System

You inherit a 2000-line `shop.py` file. Your mission: Refactor it systematically.

#### Original System (Simplified)

```python
# shop.py - 2000 lines of legacy code
import sqlite3
import hashlib
import smtplib
from datetime import datetime

DATABASE = 'shop.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    # ... create tables

def register_user(email, password, name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return {"error": "User exists"}

    # Hash password
    hashed = hashlib.md5(password.encode()).hexdigest()

    # Insert
    cursor.execute(
        "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
        (email, hashed, name)
    )
    conn.commit()
    user_id = cursor.lastrowid

    # Send welcome email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # ... send email

    conn.close()
    return {"user_id": user_id}

def login_user(email, password):
    # ... 100 lines

def add_to_cart(user_id, product_id, quantity):
    # ... 100 lines

def checkout(user_id, payment_info):
    # ... 200 lines

def get_products(category=None):
    # ... 80 lines

# ... 50 more functions, 1500 more lines
```

#### Refactoring Plan

##### Phase 1: Add Tests

```python
# tests/test_user_registration.py
def test_register_new_user():
    result = register_user("test@example.com", "password123", "Test User")
    assert "user_id" in result

def test_register_duplicate_email():
    register_user("test@example.com", "password123", "Test User")
    result = register_user("test@example.com", "password123", "Test User")
    assert "error" in result
```

##### Phase 2: Extract Configuration

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'shop.db')
    SMTP_HOST: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-me')
```

##### Phase 3: Create Domain Models

```python
# models/user.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime
    is_active: bool = True
```

##### Phase 4: Create Repositories

```python
# repositories/user_repository.py
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def find_by_email(self, email: str) -> Optional[User]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def create(self, email: str, password_hash: str, name: str) -> User:
        # ...
```

##### Phase 5: Create Services

```python
# services/user_service.py
class UserService:
    def __init__(self, user_repo, password_hasher, email_service):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.email_service = email_service

    def register_user(self, email: str, password: str, name: str) -> User:
        # Check if exists
        existing = self.user_repo.find_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email)

        # Hash password
        password_hash = self.password_hasher.hash(password)

        # Create user
        user = self.user_repo.create(email, password_hash, name)

        # Send welcome email
        self.email_service.send_welcome_email(user)

        return user
```

**Exercise 5.1:** Complete the refactoring following this structure.

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Identify common code smells
- [ ] Write characterization tests for legacy code
- [ ] Refactor in small, safe steps
- [ ] Apply SOLID principles
- [ ] Use dependency injection
- [ ] Extract methods and classes
- [ ] Eliminate code duplication
- [ ] Decouple tightly coupled code
- [ ] Replace conditionals with polymorphism
- [ ] Make legacy code testable
- [ ] Use AI effectively for refactoring suggestions

## Reflection Questions

1. What was the most challenging code smell to fix?
1. How did tests give you confidence during refactoring?
1. What surprised you about AI's refactoring suggestions?
1. How would you prioritize refactorings in a real project?
1. When should you stop refactoring and move on?

## Further Practice

- Refactor your own legacy code
- Find open source projects needing refactoring
- Practice the "Boy Scout Rule" - leave code better than you found it
- Read "Refactoring" by Martin Fowler
- Read "Working Effectively with Legacy Code" by Michael Feathers

Remember: **Refactoring is not about making code perfect. It's about making code better, one small step at a time.**
