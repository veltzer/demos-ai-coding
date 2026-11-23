# The corrected counterpart to buggy/race_condition.py. The shared global is
# kept so the diff against the buggy version is purely the added lock - that
# contrast is the lesson, so `global` stays.

import threading
import time

balance = 0
lock = threading.Lock()

def deposit_fixed(amount):
    global balance  # noqa: PLW0603  teaching: kept from the buggy version so the diff is only the lock
    with lock:
        current = balance
        time.sleep(0.001)
        balance = current + amount
        print(f"Deposited {amount}, balance now {balance}")

# Test to verify fix
def test_race_condition_fixed():
    global balance  # noqa: PLW0603  teaching: kept from the buggy version so the diff is only the lock
    balance = 0

    threads = []
    for _ in range(10):
        t = threading.Thread(target=deposit_fixed, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {balance}")
    print(f"Expected: 100, Got: {balance}")
    # Should always be 100

test_race_condition_fixed()
