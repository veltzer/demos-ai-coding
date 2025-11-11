# Function Signature Completion with Copilot

## Learning Objective
Learn how function signatures and docstrings help Copilot generate accurate function implementations.

## Instructions
1. Create a new Python file called `string_utils.py`
1. Write function signatures with descriptive names and type hints
1. Add docstrings explaining the function's purpose
1. Let Copilot complete the function bodies
1. Test the generated functions

## Your Task
Create the following function signatures and let Copilot implement them:

```python
def reverse_string(text: str) -> str:
    """
    Reverses the input string.

    Args:
        text: The string to reverse

    Returns:
        The reversed string
    """
    # Let Copilot complete this

def count_vowels(text: str) -> int:
    """
    Counts the number of vowels (a, e, i, o, u) in the input string.
    Case insensitive.

    Args:
        text: The string to analyze

    Returns:
        The number of vowels found
    """
    # Let Copilot complete this

def is_palindrome(text: str) -> bool:
    """
    Checks if a string reads the same forwards and backwards.
    Ignores spaces and case.

    Args:
        text: The string to check

    Returns:
        True if palindrome, False otherwise
    """
    # Let Copilot complete this
```

## What You'll Learn
- How function signatures guide Copilot's understanding
- The power of good docstrings for generating accurate code
- How type hints improve suggestion quality
- The importance of clear function naming

## Success Criteria
- [ ] All functions work as described in their docstrings
- [ ] Copilot generates logical implementations
- [ ] You understand how signatures influence suggestions
- [ ] Functions handle edge cases appropriately

## Test Your Functions
Add these test cases to verify your functions work:

```python
# Test cases
print(reverse_string("hello"))  # Should print "olleh"
print(count_vowels("Hello World"))  # Should print 3
print(is_palindrome("A man a plan a canal Panama"))  # Should print True
```
