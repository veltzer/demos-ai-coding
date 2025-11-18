# Context-Aware Code Generation with Copilot

## Learning Objective
Learn how Copilot uses existing code context to generate relevant and consistent code.

## Instructions
1. Create a new Python file called `todo_app.py`
1. Start by defining a data structure for todos
1. Implement a few functions, then let Copilot suggest similar ones
1. Observe how Copilot maintains consistency with your existing code style

## Your Task
Build a simple todo list manager. Start with this foundation:

```python
# Todo List Manager
todos = []

def add_todo(task: str, priority: str = "medium"):
    """Add a new todo item with task and priority."""
    todo = {
        "id": len(todos) + 1,
        "task": task,
        "priority": priority,
        "completed": False
    }
    todos.append(todo)
    print(f"Added todo: {task}")
```

Now let Copilot help you implement these additional functions by starting with their signatures:

```python
def remove_todo(todo_id: int):
    """Remove a todo by its ID."""
    # Let Copilot implement this

def mark_completed(todo_id: int):
    """Mark a todo as completed by its ID."""
    # Let Copilot implement this

def list_todos(filter_by: str = "all"):
    """List todos. Filter can be 'all', 'completed', or 'pending'."""
    # Let Copilot implement this

def get_todos_by_priority(priority: str):
    """Get all todos with specified priority."""
    # Let Copilot implement this
```

## What You'll Learn
- How Copilot uses existing code patterns to generate consistent code
- The importance of establishing conventions early in your codebase
- How data structure choices influence subsequent suggestions
- Context awareness in code generation

## Success Criteria
- [ ] Copilot generates functions that work with your existing data structure
- [ ] The coding style remains consistent across functions
- [ ] Functions handle the todo list appropriately
- [ ] Error handling follows similar patterns

## Advanced Challenge
After implementing the basic functions, try starting this function signature and see how Copilot completes it:

```python
def search_todos(keyword: str):
    """Search for todos containing the keyword in their task."""
    # Let Copilot suggest the implementation
```

## Test Your Todo App
```python
# Test the todo app
add_todo("Learn Copilot", "high")
add_todo("Write documentation", "medium")
add_todo("Review code", "low")
list_todos()
mark_completed(1)
list_todos("completed")
```
