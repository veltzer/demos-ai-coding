import threading
import time

balance = 0
lock = threading.Lock()

def deposit_fixed(amount):
    global balance
    with lock:
        current = balance
        time.sleep(0.001)
        balance = current + amount
        print(f"Deposited {amount}, balance now {balance}")

# Test to verify fix
def test_race_condition_fixed():
    global balance
    balance = 0

    threads = []
    for i in range(10):
        t = threading.Thread(target=deposit_fixed, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {balance}")
    print(f"Expected: 100, Got: {balance}")
    # Should always be 100

test_race_condition_fixed()
