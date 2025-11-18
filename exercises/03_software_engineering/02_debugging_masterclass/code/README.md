# Debugging Masterclass - Code Files

This directory contains buggy code and their fixed versions.

## Directory Structure

```txt
code/
+-- buggy/           # Code with bugs
|   +-- buggy_app.py            # Stack trace example
|   +-- find_duplicates.py      # Logic bug
|   +-- race_condition.py       # Threading bug
+-- fixed/           # Corrected code
    +-- buggy_app_fixed.py
    +-- find_duplicates_fixed.py
    +-- race_condition_fixed.py
```

## How to Use

1. **Run the buggy code** - Observe the error
1. **Read the error message** - Understand what failed
1. **Analyze the code** - Form hypothesis
1. **Compare with fixed version** - See the solution
1. **Practice debugging** - Find bugs in your own code

## Debugging Process

```bash
# 1. Run buggy code
python buggy/buggy_app.py

# 2. Read stack trace carefully

# 3. Use debugger
python -m pdb buggy/buggy_app.py

# 4. Compare with fixed version
diff buggy/buggy_app.py fixed/buggy_app_fixed.py
```

See the main `exercise.md` file for detailed debugging techniques.
