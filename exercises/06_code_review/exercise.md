# Code Review and Bug Detection with Copilot

## Learning Objective
Learn how GitHub Copilot can identify subtle bugs, security issues, and code quality problems that might be missed in manual reviews. This exercise focuses on signal safety and memory management issues.

## Background
Signal handlers in C have strict requirements about which functions are "async-signal-safe." Many common functions, including `malloc()`, `printf()`, and others, are NOT safe to call from signal handlers and can cause undefined behavior, deadlocks, or crashes.

## Instructions
1. Create a new C file called `calculator.c`
1. Implement the code as specified below
1. Use Copilot Chat to review your code
1. Learn to identify and fix signal safety issues

## Your Task

### Step 1: Basic Implementation
Write a C application with these requirements:
- Asks user for two numbers in a loop
- Prints the sum of the numbers
- Continues until interrupted
- Handles SIGINT (Ctrl+C) with a custom signal handler
- **Intentionally** include problematic code in the signal handler

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Global variable to control the main loop
volatile sig_atomic_t keep_running = 1;

// Signal handler - INTENTIONALLY PROBLEMATIC
void sigint_handler(int sig) {
    // Problem 1: malloc() is NOT async-signal-safe
    char *message = malloc(50);
    if (message) {
        // Problem 2: sprintf() is NOT async-signal-safe
        sprintf(message, "Caught signal %d, cleaning up...\n", sig);
        // Problem 3: printf() is NOT async-signal-safe
        printf("%s", message);
        free(message);  // Problem 4: free() is NOT async-signal-safe
    }

    // Problem 5: This might not be atomic on all systems
    keep_running = 0;
}

int main() {
    // Register signal handler
    signal(SIGINT, sigint_handler);

    printf("Calculator - Press Ctrl+C to exit\n");
    printf("Enter two numbers to add (or 0 0 to continue): ");

    while (keep_running) {
        double num1, num2;

        if (scanf("%lf %lf", &num1, &num2) == 2) {
            printf("Sum: %.2f\n", num1 + num2);
            printf("Enter two numbers to add: ");
        } else {
            // Clear input buffer
            while (getchar() != '\n');
            printf("Invalid input. Please enter two numbers: ");
        }
    }

    printf("Program terminated.\n");
    return 0;
}
```

### Step 2: Code Review with Copilot

Ask Copilot Chat these specific questions:

1. **General Review**: "Review this C code for any bugs or issues"
1. **Signal Safety**: "Is this signal handler implementation safe? What problems do you see?"
1. **Specific Functions**: "What's wrong with calling malloc() and printf() in a signal handler?"
1. **Best Practices**: "How should I properly implement this signal handler?"

### Step 3: Fix the Issues

Based on Copilot's feedback, implement the corrected version:

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Global variable to control the main loop
volatile sig_atomic_t keep_running = 1;

// CORRECTED signal handler - async-signal-safe
void sigint_handler(int sig) {
    // Only async-signal-safe functions allowed here
    const char message[] = "Caught SIGINT, exiting...\n";
    write(STDERR_FILENO, message, sizeof(message) - 1);

    // This is safe - sig_atomic_t assignment is atomic
    keep_running = 0;
}

// Rest of the corrected implementation...
```

## What You'll Learn
- Signal safety concepts in C programming
- Which functions are async-signal-safe and which are not
- How Copilot can identify subtle system-level bugs
- Proper signal handler implementation
- The importance of understanding system-level constraints

## Common Issues Copilot Should Identify

1. **malloc()/free() in signal handler**: Not async-signal-safe, can cause deadlocks
1. **printf()/sprintf() in signal handler**: Not async-signal-safe, can corrupt output
1. **Improper signal handler registration**: Should use sigaction() instead of signal()
1. **Race conditions**: Accessing non-atomic variables unsafely
1. **Buffer management**: Unsafe string operations

## Success Criteria
- [ ] Copilot identifies the malloc() issue
- [ ] Copilot explains why printf() is problematic in signal handlers
- [ ] You understand the concept of async-signal-safe functions
- [ ] You can implement a corrected version
- [ ] Copilot suggests using write() instead of printf() for signal handlers

## Advanced Challenges

### Challenge 1: Multiple Signal Types
Extend the code to handle multiple signals (SIGTERM, SIGUSR1) and ask Copilot to review:

```c
void sigusr1_handler(int sig) {
    // What should go here? Ask Copilot!
}

void sigterm_handler(int sig) {
    // What should go here? Ask Copilot!
}
```

### Challenge 2: Thread Safety
Add pthread usage and ask Copilot about signal handling in multithreaded programs:

```c
#include <pthread.h>

void* worker_thread(void* arg) {
    // Thread function - how does this interact with signals?
    // Ask Copilot about signal masks and pthread_sigmask()
}
```

### Challenge 3: Complete Rewrite
Ask Copilot Chat: "Rewrite this program using modern best practices for signal handling"

## Key Concepts to Discuss with Copilot

1. **Async-Signal-Safe Functions**: What makes a function safe to call from a signal handler?
1. **sigaction() vs signal()**: Why is sigaction() preferred?
1. **Signal Masks**: How to properly block signals during critical sections
1. **Self-Pipe Trick**: Alternative approach for complex signal handling
1. **signalfd() (Linux)**: Modern signal handling approaches

## Real-World Applications
This type of bug is common in:
- System daemons and services
- Network servers
- Real-time applications
- Embedded systems
- Any C/C++ application that needs graceful shutdown

## Reflection Questions
After completing this exercise:
1. What other functions might be problematic in signal handlers?
1. How would you test for signal safety issues?
1. What are the trade-offs between simple and complex signal handling?
1. How does Copilot's knowledge of system programming compare to higher-level languages?

## Additional Testing
Compile and run your code to see the difference:
```bash
gcc -o calculator calculator.c
./calculator
# Try pressing Ctrl+C multiple times quickly - problematic version may hang
```

## Resources for Further Learning
Ask Copilot about:
- The complete list of async-signal-safe functions (POSIX.1-2008)
- Signal handling best practices in modern C
- Alternatives like signalfd(), eventfd(), or self-pipe trick
