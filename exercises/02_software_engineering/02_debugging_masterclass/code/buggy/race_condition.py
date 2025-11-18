import threading
import time

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

# Test to expose race condition
def test_race_condition():
    global balance
    balance = 0

    threads = []
    for i in range(10):
        t = threading.Thread(target=deposit, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {balance}")
    print(f"Expected: 100, Got: {balance}")
    # Often gets less than 100 due to race condition

test_race_condition()
