# TDD with AI - Code Files

This directory contains code files referenced in the exercise.

## Directory Structure

```txt
code/
+-- tests/           # Test files (write these first!)
|   +-- test_password_validator.py
|   +-- test_string_calculator.py
|   +-- test_shopping_cart.py
+-- src/             # Implementation files (write after tests)
    +-- password_validator.py
    +-- string_calculator.py
    +-- shopping_cart.py
```

## How to Use

1. **Read the test file first** (e.g., `tests/test_password_validator.py`)
1. **Run the test** - it should fail (Red phase)
1. **Implement the code** in the corresponding `src/` file to make it pass (Green phase)
1. **Refactor** the code while keeping tests green

## Running Tests

```bash
# From the code directory
pytest tests/

# Run specific test file
pytest tests/test_password_validator.py

# Run with coverage
pytest --cov=src tests/
```

## Example Workflow

```bash
# 1. RED - Run failing test
pytest tests/test_password_validator.py

# 2. GREEN - Implement minimal code to pass
# Edit src/password_validator.py

# 3. Verify tests pass
pytest tests/test_password_validator.py

# 4. REFACTOR - Improve code
# Edit src/password_validator.py, re-run tests
```

See the main `exercise.md` file for detailed instructions.
