# Code review exercise

We are going to see if the AI finds a problem in our high level context
understanding of our code.

- Write a simple C application that asks the user for two number and prints
the sum of the numbers in a loop.
- Add a single handlers (Linux sig handler) to the code.
- Add a malloc(3) statement inside the signal handler.
- Now ask the AI to review your code.
- The AI should say that malloc(3) is problematic.
