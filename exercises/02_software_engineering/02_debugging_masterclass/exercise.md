# Debugging Masterclass with AI: Finding and Fixing Bugs Systematically

## Learning Objective
Learn systematic debugging techniques using AI assistance. Master reading stack traces, forming hypotheses, using debuggers effectively, and creating minimal reproductions of bugs.

## The Debugging Mindset

Debugging is **scientific investigation**, not guessing:
1. **Observe** - What is actually happening?
2. **Hypothesize** - What could cause this?
3. **Test** - Can I prove/disprove the hypothesis?
4. **Fix** - Address the root cause
5. **Verify** - Confirm the fix works

## Prerequisites
- Basic programming knowledge
- Familiarity with your language's debugger (pdb for Python, debugger for JavaScript)
- GitHub Copilot or similar AI assistant
- Willingness to think systematically

---

## Part 1: Reading Stack Traces

### Exercise 1.1: Decoding Python Stack Traces

**The Bug:**

```python
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
```

**Stack Trace:**

```txt
Traceback (most recent call last):
  File "buggy_app.py", line 31, in <module>
    result = process_order(order)
  File "buggy_app.py", line 19, in process_order
    discounted_items = apply_bulk_discounts(items)
  File "buggy_app.py", line 10, in apply_bulk_discounts
    discounted = calculate_discount(item['price'], item['discount'])
  File "buggy_app.py", line 3, in calculate_discount
    discount_amount = price * (discount_percent / 100)
TypeError: unsupported operand type(s) for /: 'NoneType' and 'int'
```

**Exercise:** Ask AI to analyze this stack trace.

**Prompt:**

```txt
Analyze this Python stack trace and explain:
1. What line is the actual error?
1. What is the root cause?
1. How did we get there (the call chain)?
1. What should be fixed?
1. How can we prevent this in the future?
```

**Manual Analysis:**

```txt
Reading bottom-up:
1. Line 3: discount_percent / 100 - trying to divide None by 100
1. Line 10: Calling calculate_discount with item['discount']
1. Line 19: Processing all items
1. Line 31: Entry point

Root cause: One item has discount=None, no validation

Fix: Add validation in calculate_discount or apply_bulk_discounts
```

**The Fix:**

```python
def calculate_discount(price, discount_percent):
    # Add validation
    if discount_percent is None:
        return price  # No discount
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price
```

---

### Exercise 1.2: JavaScript Stack Trace

**The Bug:**
```javascript
// server.js
const express = require('express');
const app = express();

app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  const user = await getUser(userId);
  const userData = formatUserData(user);
  res.json(userData);
});

async function getUser(id) {
  // Simulating database call
  const users = {
    '1': { name: 'Alice', email: 'alice@example.com', age: 30 },
    '2': { name: 'Bob', email: 'bob@example.com', age: 25 }
  };
  return users[id];
}

function formatUserData(user) {
  return {
    name: user.name.toUpperCase(),
    email: user.email,
    ageGroup: user.age >= 30 ? 'adult' : 'young'
  };
}

app.listen(3000, () => console.log('Server running'));

// Test: curl http://localhost:3000/api/users/999
```

**Error:**

```txt
TypeError: Cannot read property 'toUpperCase' of undefined
    at formatUserData (/app/server.js:19:21)
    at /app/server.js:7:32
    at processTicksAndRejections (internal/process/task_queues.js:95:5)
```

**Exercise:** Debug this issue.

**Prompt:**

```txt
This Node.js API crashes when requesting a non-existent user.
1. Explain why formatUserData fails
2. Why doesn't the error say "Cannot read property 'name' of undefined"?
3. How should we handle missing users?
4. Implement proper error handling
```

---

## Part 2: Using Debuggers Effectively

### Exercise 2.1: Python Debugger (pdb)

**Scenario:** Find why this function returns wrong results.

```python
def find_duplicates(items):
    seen = set()
    duplicates = []

    for item in items:
        if item in seen:
            duplicates.append(item)
        seen.add(item)

    return duplicates

# Bug: Returns [2, 3, 3] instead of [2, 3]
result = find_duplicates([1, 2, 2, 3, 3, 3, 4])
print(result)  # Expected: [2, 3], Got: [2, 3, 3]
```

**Debugging Steps:**

1. **Insert breakpoint:**

```python
import pdb

def find_duplicates(items):
    seen = set()
    duplicates = []

    for item in items:
        pdb.set_trace()  # Debugger will stop here
        if item in seen:
            duplicates.append(item)
        seen.add(item)

    return duplicates
```

1. **Run and use debugger commands:**

```txt
(Pdb) p item         # Print current item
(Pdb) p seen         # Print seen set
(Pdb) p duplicates   # Print duplicates list
(Pdb) n              # Next line
(Pdb) c              # Continue
```

1. **Observe the bug:**
    - When item=2 (second time): duplicates=[2], correct
    - When item=3 (second time): duplicates=[2,3], correct
    - When item=3 (third time): duplicates=[2,3,3], BUG!
    - It adds duplicate every time, not just first occurrence

1. **The fix:**
```python
def find_duplicates(items):
    seen = set()
    duplicates = set()  # Use set instead of list!

    for item in items:
        if item in seen:
            duplicates.add(item)  # Add to set (no duplicates)
        seen.add(item)

    return list(duplicates)
```

**Exercise:** Use AI to suggest debugger strategies.

**Prompt:**

```txt
I have a bug in this function. Guide me through debugging it step-by-step using pdb:
1. Where should I set breakpoints?
1. What variables should I inspect?
1. What am I looking for?
1. Suggest the fix

[Paste the buggy code]
```

---

### Exercise 2.2: Conditional Breakpoints

**Scenario:** Bug only happens with certain inputs.

```python
def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def process_grades(students):
    results = []
    for student in students:
        grade = calculate_grade(student['score'])
        results.append({
            'name': student['name'],
            'grade': grade
        })
    return results

# Bug only happens for one specific student!
students = [
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 85},
    {'name': 'Charlie', 'score': None},  # This causes the bug
    {'name': 'David', 'score': 75}
]

process_grades(students)  # Crashes at Charlie
```

**Using Conditional Breakpoints:**

```python
import pdb

def process_grades(students):
    results = []
    for student in students:
        # Only break when we hit the problematic case
        if student['name'] == 'Charlie':
            pdb.set_trace()
        grade = calculate_grade(student['score'])
        results.append({
            'name': student['name'],
            'grade': grade
        })
    return results
```

**Or in VS Code / IDE:**

```txt
Set breakpoint on calculate_grade line
Condition: student['score'] is None
```

---

## Part 3: Binary Search Debugging

### Exercise 3.1: Finding the Guilty Commit

**Scenario:** A test was passing last week, now it fails. Find which commit broke it.

**Git Bisect Process:**

```bash
# 1. Start bisect
git bisect start

# 2. Mark current commit as bad
git bisect bad

# 3. Mark a known good commit (e.g., from last week)
git bisect good abc123

# Git will checkout a commit in the middle
# 4. Test the current commit
python -m pytest test_feature.py

# 5. Mark as good or bad
git bisect good   # if test passes
# or
git bisect bad    # if test fails

# Repeat until Git finds the exact commit
# Result: "abc456 is the first bad commit"

# 6. Finish bisect
git bisect reset
```

**Exercise:** Use AI to help analyze the problematic commit.

**Prompt:**

```txt
Git bisect found this commit broke the tests:

commit abc456
Author: Developer <dev@example.com>
Date: Mon Nov 13 2024

    Refactor user validation

diff --git a/validators.py b/validators.py
--- a/validators.py
+++ b/validators.py
@@ -10,7 +10,7 @@ def validate_email(email):
-    if '@' in email:
+    if '@' in email and '.' in email:
         return True

Analyze:
1. What changed?
2. Why did tests start failing?
3. Is the new logic correct?
4. What was the intention?
5. How should we fix it?
```

---

### Exercise 3.2: Binary Search in Code

**Scenario:** Bug in a large data processing pipeline.

```python
def process_pipeline(data):
    # 10 steps of processing
    step1 = clean_data(data)
    step2 = normalize(step1)
    step3 = filter_invalid(step2)
    step4 = enrich_data(step3)
    step5 = calculate_metrics(step4)
    step6 = group_by_category(step5)
    step7 = apply_transformations(step6)
    step8 = aggregate_results(step7)
    step9 = format_output(step8)
    step10 = validate_results(step9)

    return step10

# Bug: Output is wrong, but which step causes it?
```

**Binary Search Strategy:**

```python
def process_pipeline(data):
    step1 = clean_data(data)
    step2 = normalize(step1)
    step3 = filter_invalid(step2)
    step4 = enrich_data(step3)
    step5 = calculate_metrics(step4)

    # Check halfway point
    print("After step 5:", step5)
    # Is the data correct here? If yes, bug is in steps 6-10
    # If no, bug is in steps 1-5

    step6 = group_by_category(step5)
    step7 = apply_transformations(step6)
    step8 = aggregate_results(step7)

    # Check 3/4 point
    print("After step 8:", step8)
    # Narrows down further

    step9 = format_output(step8)
    step10 = validate_results(step9)

    return step10
```

---

## Part 4: Creating Minimal Reproductions

### Exercise 4.1: Simplifying a Bug Report

**Original Bug Report:**

```txt
"The application crashes when I log in, but only sometimes,
and it seems to happen more often in the afternoon, and
I think it might be related to the email notifications feature,
and also I was using Chrome on Windows..."
```

**Create Minimal Reproduction:**

**Step 1 - Identify the Error:**

```python
# Get the actual error message
try:
    login_user(email, password)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
```

**Step 2 - Simplify:**

```python
# Minimal test case
def test_login_bug():
    """Bug: Login fails when user has pending notifications."""
    # Setup
    user = create_test_user(email="test@example.com")
    create_notification(user_id=user.id, unread=True)

    # The bug
    result = login_user("test@example.com", "password")

    # Expected: Success
    # Actual: Crashes with KeyError: 'notification_count'
    assert result is not None
```

**Step 3 - Remove Unnecessary Details:**

```python
# Absolute minimum to reproduce
def test_minimal_bug():
    user = {'id': 1, 'notifications': [{'unread': True}]}
    # Bug is here:
    count = user['notification_count']  # KeyError - should be len(user['notifications'])
```

**Exercise:** Use AI to help create minimal reproductions.

**Prompt:**

```txt
I have a bug that happens "sometimes" in production. Help me create
a minimal reproduction:

Symptoms:
- Application becomes slow
- Only happens after 1-2 hours of runtime
- Memory usage grows continuously
- No obvious error messages

What could cause this? How do I isolate the problem?
Create minimal test cases for each hypothesis.
```

---

### Exercise 4.2: Isolating Dependencies

**The Bug:**

```python
# complex_system.py - 1000 lines, many dependencies
import requests
import redis
import celery
import elasticsearch
from mylib import custom_processor
from another_lib import data_transformer

def process_data(input_data):
    # Uses all the above dependencies
    # Bug happens somewhere in here
    ...

# How do you debug this?
```

**Isolation Strategy:**

```python
# Step 1: Create standalone test
def test_process_data_isolated():
    # Remove external dependencies
    # Mock or stub everything

    input_data = {'value': 123}

    # Mock all external calls
    with patch('requests.get') as mock_requests:
        with patch('redis.Redis') as mock_redis:
            mock_requests.return_value.json.return_value = {'result': 'ok'}
            mock_redis.return_value.get.return_value = 'cached_value'

            result = process_data(input_data)

    # Does bug still happen?
    # If yes: Bug is in process_data logic
    # If no: Bug is in one of the dependencies
```

**Step 2: Binary search the dependencies:**

```python
# Test with half the dependencies mocked
# Narrow down to guilty dependency
# Then debug that specific interaction
```

---

## Part 5: Common Bug Patterns

### Pattern 1: Off-By-One Errors

**Bug:**

```python
def get_last_n_items(items, n):
    """Get last n items from list."""
    return items[len(items) - n : len(items)]

# Bug: Includes n+1 items!
items = [1, 2, 3, 4, 5]
result = get_last_n_items(items, 3)
print(result)  # Expected: [3, 4, 5], Got: [3, 4, 5] (actually correct!)

# The real bug appears with edge case:
result = get_last_n_items(items, 0)
print(result)  # Expected: [], Got: [1, 2, 3, 4, 5] (entire list!)
```

**Debugging:**

```python
def get_last_n_items(items, n):
    # Let's trace the logic
    print(f"Items: {items}, n: {n}")
    start = len(items) - n
    end = len(items)
    print(f"Slice: items[{start}:{end}]")

    result = items[start:end]
    print(f"Result: {result}")
    return result

# With n=0:
# Items: [1, 2, 3, 4, 5], n: 0
# Slice: items[5:5]  <- Should be items[5:5] = []
# But when n=0: items[5-0:5] = items[5:5] = []
# Wait, that's correct...

# Let's try the actual bug case:
items = [1, 2, 3]
result = get_last_n_items(items, 5)  # n > len(items)
# Items: [1, 2, 3], n: 5
# Slice: items[-2:3]  <- Negative index! Bug found!
# items[-2:3] = [2, 3]
```

**The Fix:**

```python
def get_last_n_items(items, n):
    """Get last n items from list."""
    if n <= 0:
        return []
    if n >= len(items):
        return items.copy()
    return items[-n:]  # Simpler and correct!
```

---

### Pattern 2: Mutable Default Arguments

**Bug:**

```python
def add_item(item, items=[]):
    """Add item to list."""
    items.append(item)
    return items

# Bug: List is shared across calls!
list1 = add_item(1)
print(list1)  # [1]

list2 = add_item(2)
print(list2)  # [1, 2]  <- Bug! Should be [2]

print(list1)  # [1, 2]  <- list1 changed too!
```

**Debugging with AI:**

**Prompt:**

```txt
Why does this function share state between calls?

def add_item(item, items=[]):
    items.append(item)
    return items

list1 = add_item(1)  # [1]
list2 = add_item(2)  # [1, 2] <- Why?

Explain what's happening and how to fix it.
```

**The Fix:**

```python
def add_item(item, items=None):
    """Add item to list."""
    if items is None:
        items = []
    items.append(item)
    return items
```

---

### Pattern 3: Race Conditions

**Bug:**

```python
balance = 0

def deposit(amount):
    global balance
    current = balance
    # Imagine another thread runs here!
    balance = current + amount

# Thread 1: deposit(100)
# Thread 2: deposit(50)
# Expected final balance: 150
# Actual: Could be 100 or 50 (race condition!)
```

**Debugging Race Conditions:**

```python
import threading
import time

balance = 0
lock = threading.Lock()

def deposit_buggy(amount):
    global balance
    current = balance
    time.sleep(0.001)  # Simulate slow operation - makes race condition obvious
    balance = current + amount
    print(f"Deposited {amount}, balance now {balance}")

def deposit_fixed(amount):
    global balance
    with lock:
        current = balance
        time.sleep(0.001)
        balance = current + amount
        print(f"Deposited {amount}, balance now {balance}")

# Test to expose race condition
def test_race_condition():
    global balance
    balance = 0

    threads = []
    for i in range(10):
        t = threading.Thread(target=deposit_buggy, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {balance}")
    print(f"Expected: 100, Got: {balance}")
    # Often gets less than 100 due to race condition

test_race_condition()
```

**Exercise:** Use AI to identify race conditions.

**Prompt:**

```txt
Review this code for race conditions:

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count

# Used by multiple threads
counter = Counter()

Explain:
1. Where are the race conditions?
2. What can go wrong?
3. How to fix it?
```

---

## Part 6: Debugging Production Issues

### Exercise 6.1: Reading Logs

**Log File:**

```txt
2024-11-13 10:15:23 INFO Starting request processing
2024-11-13 10:15:23 DEBUG User ID: 12345
2024-11-13 10:15:24 INFO Database query took 1.2s
2024-11-13 10:15:24 WARN Slow query detected
2024-11-13 10:15:25 INFO Cache miss
2024-11-13 10:15:26 ERROR Failed to fetch user data
2024-11-13 10:15:26 ERROR Exception: ConnectionTimeout
2024-11-13 10:15:26 INFO Retrying request (attempt 1/3)
2024-11-13 10:15:29 ERROR Failed to fetch user data
2024-11-13 10:15:29 ERROR Exception: ConnectionTimeout
2024-11-13 10:15:29 INFO Retrying request (attempt 2/3)
2024-11-13 10:15:32 ERROR Failed to fetch user data
2024-11-13 10:15:32 ERROR Exception: ConnectionTimeout
2024-11-13 10:15:32 ERROR Max retries exceeded
2024-11-13 10:15:32 ERROR Request failed for user 12345
```

**Exercise:** Ask AI to analyze logs.

**Prompt:**

```txt
Analyze these logs and explain:
1. What went wrong?
2. What was the timeline?
3. What is the root cause?
4. What should we investigate?
5. How can we prevent this?

[Paste logs]
```

**Manual Analysis:**

```txt
Timeline:
1. 10:15:23 - Request starts
2. 10:15:24 - Slow database query (1.2s - first red flag)
3. 10:15:25 - Cache miss (had to go to database)
4. 10:15:26 - Connection timeout (root cause!)
5. 10:15:26-32 - 3 failed retry attempts

Root Cause: Connection timeout to external service
Why? Possible causes:
- Service is down
- Network issues
- Firewall blocking
- Service overloaded
- Timeout set too low

Investigations needed:
- Check service status
- Check network connectivity
- Review timeout settings
- Check concurrent requests
```

---

### Exercise 6.2: Debugging Memory Leaks

**The Bug:**

```python
# web_server.py
class RequestHandler:
    _requests_cache = []  # Bug: Class variable grows forever!

    def handle_request(self, request):
        # Cache all requests
        self._requests_cache.append(request)

        # Process request
        result = self.process(request)

        return result

# After 100k requests, application crashes with MemoryError
```

**Debugging Steps:**

1. **Monitor memory usage:**

```python
import tracemalloc
import psutil
import os

tracemalloc.start()

def check_memory():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024  # MB
    print(f"Memory usage: {mem:.2f} MB")

    # Top memory allocations
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)

# Check periodically
check_memory()
```

1. **Use memory profiler:**

```python
from memory_profiler import profile

@profile
def handle_request(request):
    # memory_profiler will show line-by-line memory usage
    _requests_cache.append(request)  # This line grows infinitely!
    # ...
```

1. **The fix:**

```python
from collections import deque

class RequestHandler:
    def __init__(self, cache_size=1000):
        # Use bounded cache
        self._requests_cache = deque(maxlen=cache_size)

    def handle_request(self, request):
        # Old requests automatically removed when limit reached
        self._requests_cache.append(request)
        # ...
```

---

## Part 7: Advanced Debugging Techniques

### Technique 1: Time-Travel Debugging

**Using `rr` (Record and Replay):**

```bash
# Record program execution
rr record python buggy_script.py

# Replay and debug
rr replay

# In replay mode, you can:
# - Go backwards in time
# - Set breakpoints in the past
# - See exact state at any point
```

### Technique 2: Rubber Duck Debugging

**Exercise:** Explain your bug to AI as if it's a rubber duck.

**Prompt:**

```txt
I'm going to explain my bug step-by-step. Don't give me the answer yet,
just ask clarifying questions:

My program is supposed to calculate the average of numbers in a list.
It works for most inputs but fails for empty lists.
I'm checking if the list is empty...
[Explain line by line]

Wait, I just realized... [Aha moment!]
```

### Technique 3: Logging Strategies

**Strategic Logging:**

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)

def process_order(order):
    logger.info(f"Processing order {order['id']}")

    logger.debug(f"Order details: {order}")

    try:
        # Complex logic
        result = complex_calculation(order)
        logger.debug(f"Calculation result: {result}")

    except Exception as e:
        logger.error(f"Failed to process order {order['id']}", exc_info=True)
        raise

    logger.info(f"Order {order['id']} processed successfully")
    return result
```

---

## Part 8: Debugging Checklist

### Before You Debug

- [ ] Can you reproduce the bug consistently?
- [ ] Do you have the exact error message?
- [ ] Do you have the complete stack trace?
- [ ] What are the inputs that cause the bug?
- [ ] What is the expected behavior?
- [ ] What is the actual behavior?
- [ ] When did the bug start happening?

### During Debugging

- [ ] Use the debugger, don't just print
- [ ] Create a minimal reproduction
- [ ] Use binary search to isolate the problem
- [ ] Check your assumptions
- [ ] Read error messages carefully
- [ ] Check documentation
- [ ] Look at recent changes

### After Fixing

- [ ] Add a test case for the bug
- [ ] Verify the fix works
- [ ] Check for similar bugs
- [ ] Update documentation if needed
- [ ] Consider how to prevent similar bugs

---

## Part 9: Real-World Debugging Scenarios

### Scenario 1: Production API Timeout

```python
# Problem: API endpoint times out randomly

@app.route('/api/dashboard')
def get_dashboard():
    # Slow query
    user_data = db.query("SELECT * FROM users").fetchall()

    # N+1 query problem
    for user in user_data:
        user['orders'] = db.query(
            "SELECT * FROM orders WHERE user_id = ?",
            user['id']
        ).fetchall()

    return jsonify(user_data)

# Sometimes takes 30+ seconds!
```

**Debugging:**

```python
import time

@app.route('/api/dashboard')
def get_dashboard():
    start = time.time()

    t1 = time.time()
    user_data = db.query("SELECT * FROM users").fetchall()
    print(f"User query: {time.time() - t1:.2f}s")

    t2 = time.time()
    for user in user_data:
        user['orders'] = db.query(
            "SELECT * FROM orders WHERE user_id = ?",
            user['id']
        ).fetchall()
    print(f"Orders query: {time.time() - t2:.2f}s")  # This is slow!

    print(f"Total time: {time.time() - start:.2f}s")
    return jsonify(user_data)

# Output:
# User query: 0.05s
# Orders query: 28.45s  <- Found the problem!
# Total time: 28.50s
```

**The Fix:**

```python
@app.route('/api/dashboard')
def get_dashboard():
    # Single query with JOIN
    query = """
        SELECT u.*, o.* FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
    """
    results = db.query(query).fetchall()

    # Group by user
    user_data = {}
    for row in results:
        user_id = row['id']
        if user_id not in user_data:
            user_data[user_id] = {
                'id': user_id,
                'name': row['name'],
                'orders': []
            }
        if row['order_id']:
            user_data[user_id]['orders'].append({
                'id': row['order_id'],
                'total': row['order_total']
            })

    return jsonify(list(user_data.values()))

# Now takes < 0.1s
```

---

### Scenario 2: Intermittent Test Failure

```python
# Test fails sometimes but not always

def test_concurrent_operations():
    """Test that concurrent operations work correctly."""
    result = process_concurrently([1, 2, 3, 4, 5])
    assert result == [2, 4, 6, 8, 10]

# Fails about 10% of the time
```

**Debugging:**

```python
# Run the test many times to expose the issue
def test_concurrent_operations_stress():
    failures = 0
    for i in range(100):
        try:
            result = process_concurrently([1, 2, 3, 4, 5])
            assert result == [2, 4, 6, 8, 10]
        except AssertionError as e:
            failures += 1
            print(f"Failure {failures}: {result}")

    print(f"Failed {failures}/100 times")

# Output:
# Failure 1: [2, 4, 6, 8, 10, 10]  <- Duplicate!
# Failure 2: [2, 4, 6, 8]  <- Missing item!
# Failure 3: [4, 2, 6, 8, 10]  <- Wrong order!

# Conclusion: Race condition in concurrent processing
```

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Read and understand stack traces
- [ ] Use debuggers effectively (pdb, IDE debuggers)
- [ ] Create minimal bug reproductions
- [ ] Use binary search to isolate bugs
- [ ] Identify common bug patterns
- [ ] Debug race conditions
- [ ] Analyze production logs
- [ ] Find memory leaks
- [ ] Debug performance issues
- [ ] Use AI assistance effectively for debugging

## Reflection Questions

1. What debugging techniques were most effective?
1. How did AI help (or not help) with debugging?
1. What bug took longest to find? Why?
1. How did you know when you found the root cause?
1. What would you do differently next time?

## Further Practice

- Practice debugging open source projects
- Set up monitoring for your applications
- Create a debugging runbook for your team
- Learn your IDE's debugging features deeply
- Practice explaining bugs clearly

Remember: **The best debugger is a clear head. Take breaks, think systematically, and don't guess!**
