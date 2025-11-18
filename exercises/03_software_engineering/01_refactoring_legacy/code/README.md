# Refactoring Legacy Code - Code Files

This directory contains legacy code examples and their refactored versions.

## Directory Structure

```txt
code/
+-- before/          # Legacy/problematic code
|   +-- user_manager.py         # God class example
|   +-- long_method.py          # Long method smell
|   +-- duplicated_code.py      # Code duplication
+-- after/           # Refactored clean code
    +-- validators.py           # Extracted validation logic
    +-- repositories.py         # Extracted data access
    +-- services.py             # Orchestration layer
```

## How to Use

1. **Study the "before" code** - Identify code smells
1. **Analyze issues** - What makes it hard to maintain?
1. **Review "after" code** - See the improved structure
1. **Practice refactoring** - Try refactoring similar code

## Refactoring Process

1. **Add tests first** (characterization tests)
1. **Make small changes** one at a time
1. **Run tests after each change**
1. **Commit frequently**

See the main `exercise.md` file for detailed instructions and more examples.
