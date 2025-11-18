# Learning Code Patterns and Best Practices with Copilot

## Learning Objective
Learn how Copilot can help you discover and implement common coding patterns and best practices.

## Instructions
1. Create a new Python file called `file_manager.py`
1. Implement file operations using different approaches
1. Let Copilot suggest improvements and alternative patterns
1. Compare different implementations

## Your Task

### Part 1: Basic File Operations
Start by writing a comment for a basic file reading function:

```python
# Function to read a text file and return its contents
# Should handle file not found errors gracefully
def read_file(filename):
```

Let Copilot complete this function, then try these variations:

```python
# Function to read file using context manager (with statement)
def read_file_safe(filename):

# Function to read file with custom encoding
def read_file_with_encoding(filename, encoding='utf-8'):

# Function to read file line by line for large files
def read_file_lines(filename):
```

### Part 2: Error Handling Patterns
Let Copilot help you implement different error handling approaches:

```python
# Read file with try-except and return None on error
def read_file_or_none(filename):

# Read file with try-except and return default value on error
def read_file_or_default(filename, default=""):

# Read file with custom exception handling
def read_file_with_logging(filename):
```

### Part 3: Configuration Management
Start this pattern and let Copilot suggest the implementation:

```python
import json

# Class to manage application configuration
# Should load from JSON file and provide easy access to settings
class ConfigManager:
    def __init__(self, config_file):
        # Let Copilot suggest the initialization

    def get(self, key, default=None):
        # Let Copilot suggest how to get configuration values

    def update(self, key, value):
        # Let Copilot suggest how to update configuration

    def save(self):
        # Let Copilot suggest how to save changes back to file
```

## What You'll Learn
- Common Python patterns for file handling
- Different approaches to error handling
- Context managers and their benefits
- Configuration management patterns
- How Copilot suggests idiomatic Python code

## Success Criteria
- [ ] You have multiple working approaches to file reading
- [ ] You understand the trade-offs between different error handling methods
- [ ] Your ConfigManager class works correctly
- [ ] You can identify which patterns are most appropriate for different use cases

## Comparison Exercise
Create a simple test to compare the different file reading approaches:

```python
# Test file (create a sample.txt with some content)
test_files = ['sample.txt', 'nonexistent.txt']

print("Testing different file reading approaches:")
for filename in test_files:
    print(f"\nTesting with {filename}:")
    # Test each of your file reading functions here
```

## Advanced Challenge
Ask Copilot to help you implement:

1. **Async File Operations**

```python
# Async function to read file without blocking
async def read_file_async(filename):
```

1. **File Watcher Pattern**

```python
# Class that watches a file for changes
class FileWatcher:
    def __init__(self, filename, callback):
```

1. **Batch File Processor**

```python
# Function to process multiple files with progress tracking
def process_files_batch(file_list, processor_function):
```

## Reflection Questions
After completing this exercise, consider:
1. Which file reading pattern do you prefer and why?
1. How did Copilot's suggestions differ from what you might have written?
1. What new Python patterns did you discover?
1. When would you use each error handling approach?
