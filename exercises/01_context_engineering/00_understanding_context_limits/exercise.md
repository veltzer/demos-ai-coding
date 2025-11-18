# Understanding Context Limits: Working Within AI Boundaries

## Learning Objective
Learn how AI coding assistants handle context windows, understand token limits, and develop strategies to work effectively within these constraints. Master the art of providing just enough context without overwhelming the AI or hitting token limits.

## What is Context in AI Coding?

Context refers to all the information an AI assistant can "see" and use when generating responses:
- Current file content
- Open files in your editor
- Selected code snippets
- Chat history
- Project structure information
- Previously read files

## Understanding Token Limits

### What are Tokens?

Tokens are the basic units AI models use to process text. Roughly:
- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

Examples:
```txt
"Hello world" = 2 tokens
"function calculateTotal() {" = 5 tokens
"// This is a comment" = 5 tokens
```

### Common Token Limits

Different AI tools have different context windows:

| Tool | Context Window | Equivalent |
|------|----------------|------------|
| GPT-4 Turbo | 128K tokens | ~96,000 words or ~300 pages |
| Claude Sonnet 3.5 | 200K tokens | ~150,000 words or ~460 pages |
| GitHub Copilot | 8K tokens | ~6,000 words or ~18 pages |
| Claude Code | 200K tokens | ~150,000 words or ~460 pages |

### Why Limits Matter

1. **Performance**: Larger contexts take longer to process
2. **Cost**: More tokens = higher API costs
3. **Focus**: Too much context dilutes relevance
4. **Accuracy**: AI can lose track in very large contexts

---

## Part 1: Experiencing Context Limits

### Exercise 1.1: Measure Your Context

Create a Python script to estimate token usage:

```python
# token_counter.py
# Ask Copilot: "Create a script to estimate tokens in a file"

def estimate_tokens(text: str) -> int:
    """
    Rough estimation: 1 token ≈ 4 characters
    More accurate would use tiktoken library
    """
    return len(text) // 4

def analyze_file(filepath: str):
    """Analyze token usage of a file."""
    with open(filepath, 'r') as f:
        content = f.read()

    tokens = estimate_tokens(content)
    lines = content.count('\n')
    chars = len(content)

    print(f"File: {filepath}")
    print(f"Lines: {lines}")
    print(f"Characters: {chars}")
    print(f"Estimated tokens: {tokens}")
    print(f"Equivalent to ~{tokens // 1000}K tokens")

    # Warn if large
    if tokens > 4000:
        print("⚠️  Warning: This file is quite large for context")
    if tokens > 8000:
        print("❌ Critical: This file may exceed some AI context limits")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
        print("Usage: python token_counter.py <filepath>")
```

**Task**: Run this on various files in your project to understand their size.

### Exercise 1.2: Context Overflow

**Goal**: Deliberately exceed context limits to see what happens.

1. Create a large file with repetitive content:

```python
# generate_large_file.py
# Creates a file that's too large for context

def generate_large_code():
    """Generate a large Python file."""
    with open('large_file.py', 'w') as f:
        f.write("# This is a very large file\n\n")

        # Generate 1000 similar functions
        for i in range(1000):
            f.write(f"""
def function_{i}():
    '''Function number {i}'''
    x = {i}
    y = {i} * 2
    z = x + y
    return z

""")

        print("Generated large_file.py with ~1000 functions")
        print("This file is approximately 50K tokens")

generate_large_code()
```

2. Try to ask Copilot to analyze or refactor this entire file
3. Observe what happens:
   - Does it process the whole file?
   - Does it give an error?
   - Does it only process part of it?

**Reflection Questions**:
- What was the AI's response?
- Did you hit a limit?
- How did the AI handle it?

### Exercise 1.3: Context Window Experiment

Compare how different amounts of context affect responses.

Create three scenarios:

**Scenario A: Minimal Context**
```python
# Only show this function
def calculate_discount(price, customer_type):
    # Ask Copilot to implement this
    pass
```

**Scenario B: Medium Context**
```python
# Show related code
CUSTOMER_TYPES = {
    'regular': 0.0,
    'premium': 0.1,
    'vip': 0.2
}

def calculate_discount(price, customer_type):
    # Ask Copilot to implement this
    pass

def apply_seasonal_bonus(discount):
    # Summer sale adds 5%
    return discount + 0.05
```

**Scenario C: Maximum Context**
```python
# Show entire module with database, logging, validation, etc.
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class CustomerDatabase:
    # 50+ lines of database code
    pass

class DiscountValidator:
    # 30+ lines of validation
    pass

CUSTOMER_TYPES = {
    'regular': 0.0,
    'premium': 0.1,
    'vip': 0.2
}

SEASONAL_DISCOUNTS = {
    'winter': 0.15,
    'spring': 0.10,
    'summer': 0.20,
    'fall': 0.10
}

def calculate_discount(price, customer_type):
    # Ask Copilot to implement this
    pass

# Plus 100+ more lines of related code
```

**Task**: Ask Copilot to implement `calculate_discount()` in each scenario.

**Compare**:
- Which gave the best result?
- Which was most accurate?
- Did maximum context actually help?

---

## Part 2: Context Management Strategies

### Strategy 1: Selective File Opening

**Bad Practice** ❌
```txt
Opening 20 files in your editor hoping AI uses them all
```

**Good Practice** ✅
```txt
Open only 2-3 most relevant files:
1. The file you're editing
2. The interface/base class
3. A similar working example
```

### Strategy 2: Code Comments as Context

**Bad Practice** ❌
```python
def process_data(data):
    # TODO: implement this
    pass
```

**Good Practice** ✅
```python
def process_data(data):
    """
    Process customer transaction data.

    Expected input format:
    {
        'customer_id': int,
        'amount': float,
        'timestamp': datetime,
        'items': [{'id': int, 'quantity': int}]
    }

    Should:
    1. Validate all required fields
    2. Calculate total with tax
    3. Apply customer discount
    4. Log transaction
    5. Return processed result

    Raises:
        ValueError: If data is invalid
        DatabaseError: If save fails
    """
    pass
```

### Strategy 3: Context Chunking

For large refactoring tasks, break into chunks:

**Bad Approach** ❌
```txt
"Refactor this entire 2000-line file to use dependency injection"
```

**Good Approach** ✅
```txt
Step 1: "Refactor the database access methods (lines 100-200)"
Step 2: "Refactor the business logic methods (lines 300-450)"
Step 3: "Update the API handlers to use new structure (lines 500-600)"
```

### Exercise 2.1: Implement Context Chunking

You have a large legacy file that needs refactoring. Practice chunking:

```python
# legacy_code.py - 1500 lines

# Section 1: Database code (lines 1-300)
# Section 2: Business logic (lines 301-600)
# Section 3: API handlers (lines 601-900)
# Section 4: Utilities (lines 901-1200)
# Section 5: Tests (lines 1201-1500)
```

**Task**:
1. Identify logical sections
2. Refactor one section at a time
3. Keep track of changes
4. Ensure sections still work together

**Tips**:
- Work on the most independent section first
- Use clear commit messages for each chunk
- Test after each chunk

---

## Part 3: Advanced Context Techniques

### Technique 1: Context Priming

Set up context before asking questions:

```python
# First, establish the pattern
"""
In this project, we follow these patterns:

1. All database access goes through repositories
2. Business logic lives in service classes
3. API handlers are thin wrappers
4. We use dependency injection
5. All methods have type hints

Example of our pattern:
"""

# repository.py
class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).get(user_id)

# service.py
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, user_id: int) -> User:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
        return user

# Now ask: "Create a ProductRepository and ProductService following our patterns"
```

### Technique 2: Reference Examples

Provide a working example as context:

```python
# This is a working example:
class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway, logger: Logger):
        self.gateway = gateway
        self.logger = logger

    def process_payment(self, amount: float, card: Card) -> PaymentResult:
        """Process a payment transaction."""
        try:
            self.logger.info(f"Processing payment of ${amount}")

            # Validate
            if amount <= 0:
                raise ValueError("Amount must be positive")

            # Process
            result = self.gateway.charge(card, amount)

            # Log result
            if result.success:
                self.logger.info(f"Payment successful: {result.transaction_id}")
            else:
                self.logger.error(f"Payment failed: {result.error}")

            return result

        except Exception as e:
            self.logger.error(f"Payment processing error: {e}")
            raise

# Now create a RefundProcessor that follows the same pattern:
class RefundProcessor:
    # Ask Copilot to implement this following the PaymentProcessor pattern
    pass
```

### Technique 3: Progressive Context Building

Build context progressively through conversation:

```txt
User: "I need to add authentication to my API"
AI: [Gives general advice]

User: "We're using FastAPI with JWT tokens"
AI: [Gives FastAPI-specific advice]

User: "Here's our current user model: [paste code]"
AI: [Gives advice specific to your user model]

User: "And here's how we handle database sessions: [paste code]"
AI: [Gives complete, contextually perfect solution]
```

### Exercise 3.1: Context Priming Practice

**Scenario**: You're building a task management system and want AI to help add a new feature.

**Task**:
1. Create a context primer document:

```markdown
# Project Context: Task Management System

## Architecture
- Backend: FastAPI
- Database: PostgreSQL with SQLAlchemy ORM
- Auth: JWT tokens
- Testing: pytest

## Code Patterns

### Repository Pattern
```python
class BaseRepository:
    def __init__(self, session: Session):
        self.session = session
```

### Service Pattern
```python
class BaseService:
    def __init__(self, repo: Repository):
        self.repo = repo
```

### API Pattern
```python
@router.post("/tasks")
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    return task_service.create(task, current_user)
```

## Now implement: Comment system for tasks
```

2. Ask AI to implement the comment system
3. Compare with asking without context primer

**Measure**:
- How many iterations needed?
- How accurate was the first response?
- Did it follow your patterns?

---

## Part 4: Context Anti-Patterns

### Anti-Pattern 1: The Dump Truck 🚚

**Problem**: Pasting your entire codebase into chat

```txt
User: "Here's my entire project [pastes 10,000 lines]
       Fix the bug in the payment processing"
```

**Why Bad**:
- Exceeds token limits
- Dilutes relevant context
- Wastes processing time
- Often gets truncated

**Solution**: Be surgical
```txt
User: "I have a bug in payment processing. Here's the relevant code:
       [Paste 50 lines of payment code]
       [Paste 20 lines of related models]
       [Paste error message]

       What's wrong?"
```

### Anti-Pattern 2: Context Amnesia 🧠

**Problem**: Not realizing AI forgets context between sessions

```txt
Session 1:
User: "Here's my database schema [shares schema]"
AI: "Great, I understand your schema"

[Next day - new session]
Session 2:
User: "Add a new field to the users table"
AI: "I don't know your users table structure"
```

**Solution**: Re-establish context or use persistent workspace
```txt
Session 2:
User: "Quick reminder - here's our users table:
       [Paste table definition]

       Now add a 'last_login' field"
```

### Anti-Pattern 3: The Vague Request 🌫️

**Problem**: Not providing any context

```txt
User: "Create a login function"
AI: [Creates generic Python function]
User: "No, for my React app with Firebase"
AI: [Creates React function]
User: "No, with our custom auth system"
AI: [Finally creates what you need]
```

**Solution**: Front-load context
```txt
User: "Create a login function for our React app.
       We use Firebase Auth.
       Here's our AuthContext: [paste]
       Should redirect to /dashboard on success"
AI: [Creates exactly what you need, first time]
```

### Anti-Pattern 4: Context Pollution 🗑️

**Problem**: Including irrelevant files or code

```txt
# Asking about React component but including:
- package.json
- webpack config
- unrelated components
- test fixtures
- node_modules types
```

**Solution**: Only include what's needed
```txt
# Asking about React component, include:
- The component file
- Its props interface
- Related hooks/utilities
- Relevant type definitions
```

### Exercise 4.1: Identify Anti-Patterns

Review these requests and identify the anti-pattern:

**Request A**:
```txt
"Fix my code [pastes 5000 lines with no indication of where the bug is]"
```

**Request B**:
```txt
Session 1: "Here's my config: [detailed setup]"
Session 2 (next week): "Update the config" [provides no context]
```

**Request C**:
```txt
"Make it better" [no code, no context, no specifics]
```

**Task**: Rewrite each request following best practices.

---

## Part 5: Measuring Context Effectiveness

### Metrics to Track

1. **First-Try Success Rate**
   - Did AI give the right answer first try?
   - Track over time as you improve context

2. **Iteration Count**
   - How many back-and-forth messages needed?
   - Good context → fewer iterations

3. **Relevance Score**
   - Was the response on-target?
   - Did AI understand your constraints?

4. **Context Size vs. Quality**
   - More context ≠ better results
   - Find your sweet spot

### Exercise 5.1: Context Effectiveness Experiment

Track your interactions for one week:

```markdown
# Context Effectiveness Log

## Day 1
Request: "Add validation to user form"
Context Provided: Form component only
Result: Generic validation, didn't match our patterns
Iterations: 3
Success: No

Request: "Add validation to user form"
Context Provided: Form component + existing validation pattern + user schema
Result: Perfect, matched our style
Iterations: 1
Success: Yes

## Day 2
[Continue tracking...]
```

**Analyze**:
- What patterns emerge?
- What context always helps?
- What context never helps?
- What's your optimal context size?

---

## Part 6: Tools for Context Management

### Tool 1: Context Bookmarks

Create snippets of commonly needed context:

```python
# snippets/patterns.py

"""
CONTEXT SNIPPET: Our Repository Pattern

Use this when asking AI to create repositories
"""

from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get(self, id: int) -> Optional[T]:
        return self.session.query(self.model).get(id)

    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.session.query(self.model).offset(skip).limit(limit).all()
```

### Tool 2: Context Templates

Create templates for common scenarios:

```markdown
# Template: Adding New API Endpoint

## Current Context
Architecture: [FastAPI/Django/Flask/etc]
Auth: [JWT/OAuth/Session/etc]
Database: [PostgreSQL/MySQL/MongoDB/etc]

## Related Code
[Paste similar endpoint as example]

## Requirements
- Input: [Specify request format]
- Output: [Specify response format]
- Validation: [List rules]
- Auth: [Specify requirements]
- Error Handling: [Specify error cases]

## Question
[Your specific question]
```

### Tool 3: Context Analyzer

Create a tool to analyze your context before sending:

```python
# context_analyzer.py

def analyze_context(context: str) -> dict:
    """Analyze context quality."""
    tokens = len(context) // 4
    lines = context.count('\n')
    has_types = 'def ' in context and '->' in context
    has_examples = 'Example:' in context or '# Example' in context
    has_requirements = 'should' in context.lower() or 'must' in context.lower()

    return {
        'tokens': tokens,
        'lines': lines,
        'has_type_hints': has_types,
        'has_examples': has_examples,
        'has_requirements': has_requirements,
        'quality_score': calculate_score(tokens, has_types, has_examples, has_requirements)
    }

def calculate_score(tokens, types, examples, requirements):
    score = 0

    # Optimal size: 200-1000 tokens
    if 200 <= tokens <= 1000:
        score += 30
    elif tokens < 200:
        score += 10  # Too little context
    else:
        score += 20  # Too much context

    if types:
        score += 25
    if examples:
        score += 25
    if requirements:
        score += 20

    return score
```

### Exercise 6.1: Build Your Context Toolkit

Create your personal context management toolkit:

1. **Pattern Library**: Save common patterns in your project
2. **Context Templates**: Create templates for common requests
3. **Quick Reference**: Document your architecture/decisions
4. **Example Repository**: Collect good examples of each pattern

**Structure**:
```
.context/
├── patterns/
│   ├── repository.py
│   ├── service.py
│   └── api.py
├── templates/
│   ├── new_feature.md
│   ├── bug_report.md
│   └── refactoring.md
├── examples/
│   ├── good_request.md
│   └── bad_request.md
└── architecture.md
```

---

## Part 7: Real-World Scenarios

### Scenario 1: Legacy Code Refactoring

You have a 3000-line legacy file to refactor. How do you manage context?

**Strategy**:
1. Create architecture document
2. Chunk into logical sections
3. Refactor one section at a time
4. Keep running context of changes

**Practice**:
```python
# Step 1: Document current structure
"""
CONTEXT: Legacy Refactoring

Current State:
- All code in one file (3000 lines)
- No classes, all functions
- Global state everywhere
- No type hints

Goal:
- Split into modules
- Use classes
- Eliminate global state
- Add type hints

Pattern to follow:
[Show modern pattern]

Refactoring Section 1 (lines 1-500): Database access
"""
```

### Scenario 2: Learning New Framework

You're learning a new framework. How do you build context efficiently?

**Strategy**:
1. Start with official examples
2. Build minimal working example
3. Gradually add complexity
4. Reference docs selectively

**Practice**:
```txt
User: "I'm learning FastAPI. Here's the basic example from docs:
       [paste official example]

       Now I want to add database support.
       My project uses PostgreSQL with SQLAlchemy.

       Can you show me how to integrate this,
       following FastAPI best practices?"
```

### Scenario 3: Debugging Production Issue

Production bug, need quick context for AI assistance:

**Strategy**:
1. Error message (exact text)
2. Relevant code (not all code)
3. Recent changes
4. Environment details

**Practice**:
```txt
User: "Production bug in payment processing:

Error:
```
KeyError: 'customer_id' in payment_processor.py line 145
```

Relevant code:
[Paste payment_processor.py lines 140-160]
[Paste related model]

Recent changes:
- Added new payment method last week
- Updated customer model yesterday

Environment:
- Python 3.11
- Production load: 1000 req/min

What's wrong and how to fix?"
```

---

## Success Criteria

After completing this exercise, you should:

- [ ] Understand token limits and how they affect AI responses
- [ ] Know how to measure context size
- [ ] Can identify too much vs. too little context
- [ ] Use context chunking for large tasks
- [ ] Provide effective code examples as context
- [ ] Avoid common context anti-patterns
- [ ] Build context progressively in conversations
- [ ] Create reusable context snippets
- [ ] Track and improve context effectiveness
- [ ] Have a personal context management toolkit

## Reflection Questions

1. How much context is "too much" for your typical tasks?
2. What types of context are most helpful for your work?
3. How has understanding context limits changed your approach?
4. What's your biggest context management challenge?
5. How can you make context provision more systematic?

## Further Learning

- Read about token counting algorithms (tiktoken)
- Study RAG (Retrieval-Augmented Generation)
- Learn about vector databases for context
- Explore context window optimization techniques
- Research how different AI models handle context

## Key Takeaways

1. **More ≠ Better**: Optimal context beats maximum context
2. **Be Selective**: Choose relevant context carefully
3. **Structure Matters**: Well-organized context works better
4. **Examples Help**: Good examples are worth 1000 words
5. **Iterate Intelligently**: Build context progressively
6. **Track Results**: Measure what works for you
7. **Create Systems**: Build reusable context patterns

Remember: Context engineering is a skill that improves with practice. The goal is to give AI just enough information to be helpful, but not so much that it gets lost in the noise!
