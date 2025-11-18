# Effective Context Strategies: Mastering AI-Assisted Development

## Learning Objective
Master advanced context engineering techniques to dramatically improve AI coding assistant effectiveness. Learn proven strategies for structuring context, managing multi-file projects, and building context systems that scale.

## What Makes Context "Effective"?

Effective context is:
- **Relevant**: Contains only what's needed
- **Structured**: Organized logically
- **Complete**: Includes all necessary information
- **Concise**: No unnecessary noise
- **Actionable**: Leads to concrete results

---

## Part 1: The Context Hierarchy

### Understanding Context Layers

Different tasks need different context levels:

```
Level 1: IMMEDIATE CONTEXT (Always include)
├── Current file/function
├── Direct dependencies
└── Error messages

Level 2: ARCHITECTURAL CONTEXT (Include when needed)
├── Project structure
├── Design patterns
├── Coding standards
└── Technology stack

Level 3: DOMAIN CONTEXT (Include for complex logic)
├── Business rules
├── Data models
├── Workflows
└── User requirements

Level 4: HISTORICAL CONTEXT (Rarely include)
├── Why decisions were made
├── Previous implementations
├── Known issues
└── Migration history
```

### Exercise 1.1: Context Layering Practice

For each scenario, determine which context layers to include:

**Scenario A**: "Fix this bug where users can't log in"
```python
# What context layers do you need?
# Mark: ✓ or ✗

[ ] Current login function
[ ] Authentication service
[ ] Error message
[ ] Project structure
[ ] Database schema
[ ] Why we chose this auth library
[ ] Old authentication code
[ ] Business requirements doc
```

**Scenario B**: "Add a new payment method"
```python
# What context layers do you need?
# Mark: ✓ or ✗

[ ] Current payment processing code
[ ] Existing payment methods
[ ] Payment gateway API docs
[ ] Project structure
[ ] Business rules for payments
[ ] Why we chose this payment gateway
[ ] Migration from old system
[ ] Complete git history
```

**Scenario C**: "Refactor this function for better performance"
```python
# What context layers do you need?
# Mark: ✓ or ✗

[ ] The function itself
[ ] Performance benchmarks
[ ] Where it's called from
[ ] Similar optimized functions
[ ] Entire project structure
[ ] Business requirements
[ ] Code review history
[ ] All related test files
```

---

## Part 2: Context Composition Patterns

### Pattern 1: The Sandwich Method

Structure context like a sandwich:

```
TOP BUN: Goal/Question (What you want)
├── Clear, specific question
└── Expected outcome

FILLING: Context (What AI needs to know)
├── Relevant code
├── Related examples
├── Constraints
└── Requirements

BOTTOM BUN: Constraints (Important boundaries)
├── What NOT to do
├── Required patterns
└── Performance/security needs
```

**Example**:

```python
"""
TOP BUN: Goal
========
Add email validation to user registration that:
- Validates format
- Checks for disposable email domains
- Sends confirmation link

FILLING: Context
===============
Current user model:
"""
class User(BaseModel):
    email: str
    username: str
    password_hash: str
    is_verified: bool = False

"""
Our validation pattern (example):
"""
class PasswordValidator:
    def validate(self, password: str) -> ValidationResult:
        if len(password) < 8:
            return ValidationResult(valid=False, error="Too short")
        if not any(c.isupper() for c in password):
            return ValidationResult(valid=False, error="Need uppercase")
        return ValidationResult(valid=True)

"""
BOTTOM BUN: Constraints
=======================
- Use our ValidationResult pattern (shown above)
- Don't use external libraries for validation
- Must handle async email sending
- Block these disposable domains: [list]
"""

# Now implement EmailValidator class:
```

### Pattern 2: The Example-Driven Context

Provide a working example, then ask for similar:

```python
"""
EXAMPLE: How we implement services in this project
"""

class UserService:
    """Service for user operations."""

    def __init__(self, repo: UserRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    async def create_user(self, data: UserCreate) -> User:
        """Create a new user."""
        try:
            # Validate
            if await self.repo.email_exists(data.email):
                raise ValueError("Email already exists")

            # Create
            user = await self.repo.create(data)

            # Log
            self.logger.info(f"User created: {user.id}")

            return user

        except Exception as e:
            self.logger.error(f"User creation failed: {e}")
            raise

"""
NOW CREATE: ProductService following the exact same pattern
Should have:
- create_product(data: ProductCreate) -> Product
- Validation: check if product code exists
- Logging on success/failure
- Proper error handling
"""

class ProductService:
    # AI will follow the pattern precisely
    pass
```

### Pattern 3: The Progressive Context Build

Build context incrementally through the conversation:

```txt
Message 1:
"I'm building a REST API with FastAPI"

Message 2:
"Here's my user model: [paste]
I need to add authentication"

Message 3:
"We want to use JWT tokens.
Here's our current config setup: [paste]"

Message 4:
"And here's how we handle dependencies: [paste]
Now implement the auth endpoints"
```

### Exercise 2.1: Apply Context Patterns

Choose a task and apply all three patterns:

**Your Task**: Add a comment system to a blog application

**Task A**: Use Sandwich Method
```python
# Write your context using the sandwich structure
# TOP BUN: Goal
# FILLING: Context
# BOTTOM BUN: Constraints
```

**Task B**: Use Example-Driven
```python
# Provide an example of a similar feature (e.g., likes system)
# Then ask for comments system following the pattern
```

**Task C**: Use Progressive Build
```python
# Plan 4-5 messages that gradually build context
# Message 1: [...]
# Message 2: [...]
# Message 3: [...]
# etc.
```

**Compare**: Which pattern worked best for your task?

---

## Part 3: Multi-File Context Management

### Challenge: Working Across Multiple Files

When your task spans multiple files, context management becomes critical.

### Strategy 1: The Interface-First Approach

Start with interfaces/types, then implementations:

```typescript
// Step 1: Show interfaces
"""
Our interfaces:
"""

// types.ts
interface User {
  id: string;
  email: string;
  role: 'admin' | 'user';
}

interface AuthService {
  login(email: string, password: string): Promise<User>;
  logout(): Promise<void>;
  getCurrentUser(): Promise<User | null>;
}

"""
Step 2: Now implement AuthService
Follow these patterns: [paste pattern example]
"""

// Implementation happens with clear interface context
```

### Strategy 2: The Breadcrumb Trail

Leave breadcrumbs between related files:

```python
# file1.py
class UserRepository:
    """
    Repository for user data access.

    Related files:
    - models.py: User model definition
    - services.py: UserService uses this repository
    - api.py: API endpoints use UserService
    """
    pass

# When asking AI about any of these files,
# the comments provide context navigation
```

### Strategy 3: The Context Map

Create a context map document:

```markdown
# Context Map: User Management Feature

## File Structure
```
user_management/
├── models.py          # User, Role models
├── repositories.py    # UserRepository, RoleRepository
├── services.py        # UserService
├── api.py            # FastAPI endpoints
└── validators.py     # Input validation
```

## Key Relationships
- API → Service → Repository → Model
- Validators used by API layer
- Services handle business logic
- Repositories handle data access

## When to include each file:
- Working on API: Include services.py, validators.py
- Working on Service: Include repositories.py, models.py
- Working on Repository: Include models.py only
- Working on Validators: Include models.py only

## Design Patterns
- Repository pattern for data access
- Service layer for business logic
- Dependency injection everywhere
- Type hints on all functions
```

### Exercise 3.1: Multi-File Context Practice

**Scenario**: You're adding a new feature that touches multiple files.

**Setup**: Create a small project structure:
```
blog/
├── models/
│   ├── user.py
│   └── post.py
├── services/
│   ├── user_service.py
│   └── post_service.py
├── api/
│   ├── users.py
│   └── posts.py
└── tests/
    └── test_posts.py
```

**Task**: Add "post likes" feature

**Step 1**: Create a context map (use template above)

**Step 2**: Determine which files need changes:
```python
# Files to modify:
# [ ] models/post.py - add like_count field
# [ ] services/post_service.py - add like/unlike methods
# [ ] api/posts.py - add like/unlike endpoints
# [ ] tests/test_posts.py - add tests
```

**Step 3**: For each file change, determine minimal context needed

**Step 4**: Execute changes in logical order with appropriate context

---

## Part 4: Context Templates for Common Tasks

### Template 1: Adding a New API Endpoint

```python
"""
TASK: Add new API endpoint

CONTEXT:
========
Framework: [FastAPI/Django/Flask/etc]
Path: [/api/v1/resource]
Method: [GET/POST/PUT/DELETE]

Current Code:
-------------
[Paste similar endpoint as reference]

Data Models:
-----------
[Paste relevant models]

Business Logic:
--------------
[Paste or describe logic]

REQUIREMENTS:
============
- Input: [Format]
- Output: [Format]
- Authentication: [Yes/No, method]
- Validation: [Rules]
- Error Handling: [Cases]
- Rate Limiting: [Yes/No]

CONSTRAINTS:
===========
- Follow REST conventions
- Use our error response format
- Add OpenAPI documentation
- Include tests

IMPLEMENT: [Specific endpoint]
"""
```

### Template 2: Debugging

```python
"""
BUG REPORT

SYMPTOM:
========
[Exact error message or unexpected behavior]

CONTEXT:
========
Environment: [dev/staging/production]
When: [Always/Sometimes/Specific conditions]
Frequency: [Every time/Intermittent]

RELEVANT CODE:
=============
[Paste code where error occurs]
[Paste related code]

RECENT CHANGES:
==============
[Any recent modifications to related code]

WHAT I'VE TRIED:
===============
1. [First attempt]
2. [Second attempt]

EXPECTED BEHAVIOR:
=================
[What should happen]

ACTUAL BEHAVIOR:
===============
[What actually happens]

HELP ME: [Specific question about the bug]
"""
```

### Template 3: Refactoring

```python
"""
REFACTORING REQUEST

CURRENT STATE:
=============
[Paste code to be refactored]

PROBLEMS:
=========
1. [Problem 1]
2. [Problem 2]
3. [Problem 3]

DESIRED STATE:
=============
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

CONSTRAINTS:
===========
- Must maintain backward compatibility
- Cannot change public API
- Must pass existing tests
- Follow [Pattern Name] pattern

EXAMPLE OF DESIRED PATTERN:
===========================
[Paste example of good code following the pattern]

REFACTOR: [Specific component]
"""
```

### Template 4: Learning New Pattern

```python
"""
LEARNING: [Pattern Name]

WHAT I KNOW:
===========
[Describe your understanding]

WHAT I DON'T UNDERSTAND:
=======================
[Specific questions]

MY CURRENT CODE:
===============
[Paste current implementation]

PATTERN EXAMPLE I FOUND:
=======================
[Paste example from docs/blog]

HELP ME:
========
1. Explain the pattern in the context of my code
2. Show me how to refactor my code to use this pattern
3. Explain trade-offs and when to use this pattern
"""
```

### Exercise 4.1: Create Your Template Library

Create templates for your most common tasks:

1. **Identify**: What are your 5 most common AI assistance requests?
   - [ ] Task 1: _________________
   - [ ] Task 2: _________________
   - [ ] Task 3: _________________
   - [ ] Task 4: _________________
   - [ ] Task 5: _________________

2. **Template**: Create a context template for each

3. **Test**: Use each template on a real task

4. **Refine**: Improve based on results

5. **Library**: Save in a templates/ directory

---

## Part 5: Context Optimization Techniques

### Technique 1: Code Minimization

Remove unnecessary code from context:

**Before** ❌ (700 tokens):
```python
class UserService:
    """
    Service for handling user operations.

    This service provides comprehensive user management functionality
    including creation, retrieval, updating, and deletion of users.
    It implements validation, logging, and error handling.

    Attributes:
        repo: The user repository instance
        logger: Logger instance for debugging
        validator: Validator for user input
        cache: Cache instance for performance
    """

    def __init__(self, repo: UserRepository, logger: Logger):
        self.repo = repo
        self.logger = logger
        self.validator = UserValidator()
        self.cache = CacheService()

    async def get_user(self, user_id: int) -> User:
        """Retrieve a user by ID."""
        # Check cache first
        cached = await self.cache.get(f"user:{user_id}")
        if cached:
            return cached

        # Query database
        user = await self.repo.get(user_id)

        # Cache result
        if user:
            await self.cache.set(f"user:{user_id}", user, ttl=300)

        return user

    # [20 more methods...]
```

**After** ✅ (150 tokens):
```python
class UserService:
    def __init__(self, repo: UserRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    async def get_user(self, user_id: int) -> User:
        return await self.repo.get(user_id)

    # [Omitted: 20 other methods]
    # Full code: user_service.py:1-250

# Context: I need to add a delete_user method following our patterns
```

### Technique 2: Reference Instead of Duplication

Don't paste the same code multiple times:

**Before** ❌:
```python
"""
Here's our authentication:
[500 lines of auth code]

Here's our authorization:
[500 lines of auth code - same file!]

Here's where the error happens:
[same code again with line number]
"""
```

**After** ✅:
```python
"""
Authentication/Authorization: auth.py (see lines 1-500)

Error occurs at line 247:
"""
if not user.has_permission(resource):
    raise PermissionError()
"""

Related: The permission checking logic (lines 180-200)
"""
```

### Technique 3: Smart Commenting

Add context through strategic comments:

```python
# When providing code to AI, add clarifying comments:

class PaymentProcessor:
    def process(self, payment: Payment) -> Result:
        # NOTE: payment.amount is in cents (integer)
        # NOTE: payment.currency follows ISO 4217 (e.g., "USD")
        # NOTE: This connects to Stripe API v2023-10-16

        # CONTEXT: We calculate fee as 2.9% + $0.30
        fee = int(payment.amount * 0.029 + 30)

        # IMPORTANT: Must validate amount > minimum (50 cents)
        if payment.amount < 50:
            return Result(success=False, error="Amount too low")

        # TODO: This is where I need help optimizing
        result = self._charge_card(payment.card, payment.amount + fee)

        return result
```

### Technique 4: Context Compression

Compress context by using summaries:

**Before** ❌ (5000 tokens):
```python
# [Full User model - 200 lines]
# [Full Order model - 300 lines]
# [Full Product model - 250 lines]
# [Full Payment model - 200 lines]
# [All their relationships and methods]
```

**After** ✅ (500 tokens):
```python
"""
Data Model Summary:
- User: id, email, name, role
- Order: id, user_id, total, status, items[]
- Product: id, name, price, inventory
- Payment: id, order_id, amount, status

Relationships:
- User has many Orders
- Order has many Products (through OrderItem)
- Order has one Payment

For full details, see: models/__init__.py
"""

# Now I need help with [specific task]
```

### Exercise 5.1: Context Optimization Challenge

Take this verbose context and optimize it:

**Original** (2000 tokens):
```python
# [Paste a very verbose context with:
#  - Excessive comments
#  - Repeated code
#  - Unnecessary imports
#  - Full file dumps
#  - Redundant examples]
```

**Your task**:
1. Reduce to under 500 tokens
2. Keep all essential information
3. Maintain clarity
4. Test: Does AI still understand?

**Measure**:
- Original tokens: _____
- Optimized tokens: _____
- Reduction: _____%
- Quality maintained: Yes/No

---

## Part 6: Context for Different AI Tools

Different tools need different context strategies:

### GitHub Copilot (Inline)

**Best Practices**:
- Relies heavily on current file
- Looks at nearby code
- Uses comments effectively
- Short context window

**Optimal Context**:
```python
# Copilot works best with:

# 1. Clear function signatures
def calculate_tax(amount: float, state: str) -> float:
    """Calculate sales tax based on state."""
    # Copilot will suggest implementation

# 2. Examples in same file
def calculate_shipping(weight: float) -> float:
    """Calculate shipping cost."""
    if weight < 1:
        return 5.00
    elif weight < 5:
        return 10.00
    else:
        return 15.00

def calculate_handling(weight: float) -> float:
    """Calculate handling fee."""
    # Copilot will follow similar pattern

# 3. Patterns established earlier
class UserRepository:
    def get(self, id: int) -> User: pass
    def create(self, data: UserCreate) -> User: pass

class ProductRepository:
    # Copilot will suggest same pattern
```

### Chat-based AI (Claude, ChatGPT)

**Best Practices**:
- Can handle longer context
- Benefits from structured prompts
- Can reference earlier conversation
- Good with complex requirements

**Optimal Context**:
```python
"""
Chat AI works best with:

STRUCTURED PROMPTS:
===================
Goal: [Clear statement]
Context: [Relevant code]
Requirements: [Bullet list]
Constraints: [Specific rules]

PROGRESSIVE BUILDING:
====================
Message 1: High-level requirements
Message 2: Add architectural context
Message 3: Provide specific code
Message 4: Ask for implementation

EXPLICIT RELATIONSHIPS:
======================
"File A depends on File B"
"Class X implements Interface Y"
"This follows the Z pattern"
"""
```

### Specialized Copilots (Cursor, Tabnine)

**Best Practices**:
- Workspace-aware
- Can scan multiple files
- Learns from your codebase
- Context from project structure

**Optimal Context**:
```python
"""
Workspace-aware AI benefits from:

PROJECT STRUCTURE:
- Clear directory organization
- Consistent naming conventions
- README with architecture overview

CODE PATTERNS:
- Consistent patterns across files
- Clear separation of concerns
- Well-named files and functions

DOCUMENTATION:
- docstrings on classes/functions
- Architecture decision records
- Pattern libraries
"""
```

### Exercise 6.1: Tool-Specific Context

**Task**: Implement the same feature using different tools

**Feature**: Add email notification to order processing

**A. Using GitHub Copilot (inline)**:
```python
# Set up context in current file for Copilot
# What context do you provide?
```

**B. Using Claude/ChatGPT**:
```python
# Structure a chat prompt
# What context do you provide?
```

**C. Using Cursor (workspace-aware)**:
```python
# Set up project for Cursor
# What context do you provide?
```

**Compare**: Which tool needed what context?

---

## Part 7: Advanced Context Techniques

### Technique 1: Context Caching

For repeated tasks, cache context:

```python
# .ai-context/project-context.md
"""
PROJECT CONTEXT (use for all AI requests)

Architecture: Microservices with FastAPI
Database: PostgreSQL + Redis
Auth: JWT tokens
Deployment: Docker + Kubernetes

Common Patterns:
1. Repository pattern for data access
2. Service layer for business logic
3. API layer thin, delegates to services
4. All async with asyncio
5. Type hints everywhere

Code Style:
- Black formatter
- Maximum line length: 100
- Use dataclasses for DTOs
- Pydantic for validation

Testing:
- pytest for unit tests
- httpx for integration tests
- factories for test data

Use this context for all development tasks.
"""
```

### Technique 2: Context Inheritance

Create layered context that inherits:

```python
# base-context.md
"""
BASE CONTEXT (all projects)
- Python 3.11+
- Type hints required
- Async preferred
- Tests required
"""

# project-context.md
"""
PROJECT CONTEXT (inherits base)
INCLUDES: base-context.md

Additional for this project:
- FastAPI framework
- PostgreSQL database
- JWT authentication
"""

# feature-context.md
"""
FEATURE CONTEXT (inherits project)
INCLUDES: project-context.md

Additional for user management:
- User model: [details]
- Auth patterns: [details]
"""
```

### Technique 3: Context Versioning

Track context changes over time:

```python
# context-v1.md (initial)
"""
We use Flask
Database: MySQL
Auth: Session-based
"""

# context-v2.md (migration)
"""
MIGRATION IN PROGRESS
- Moving from Flask to FastAPI
- Database stays MySQL
- Auth becoming JWT

When working on:
- New code: Use FastAPI patterns
- Old code: Maintain Flask patterns
- Migration code: See migration-guide.md
"""

# context-v3.md (after migration)
"""
We use FastAPI
Database: MySQL
Auth: JWT
Old code: Archived in legacy/
"""
```

### Technique 4: Context Profiles

Create profiles for different scenarios:

```python
# profiles/new-feature.md
"""
CONTEXT PROFILE: New Feature

Include:
- Architecture overview
- Related features for reference
- Design patterns document
- Testing requirements

Exclude:
- Legacy code
- Deprecated patterns
- Migration history
"""

# profiles/bug-fix.md
"""
CONTEXT PROFILE: Bug Fix

Include:
- Error message/stack trace
- Code where error occurs
- Related code
- Recent changes
- Test cases that fail

Exclude:
- Unrelated features
- Architecture docs
- Design patterns
"""

# profiles/refactoring.md
"""
CONTEXT PROFILE: Refactoring

Include:
- Current code
- Target pattern/architecture
- Example of good code
- Tests to maintain
- Performance requirements

Exclude:
- Why old code was written
- Historical context
- Other features
"""
```

### Exercise 7.1: Build a Context System

**Task**: Create a complete context management system for a project

**Requirements**:
1. Base context document
2. 3+ context profiles
3. Context caching strategy
4. Version control for context
5. Documentation on when to use each

**Structure**:
```
.ai-context/
├── README.md              # How to use this system
├── base-context.md        # Always applicable
├── profiles/
│   ├── new-feature.md
│   ├── bug-fix.md
│   ├── refactoring.md
│   └── learning.md
├── examples/
│   ├── good-request.md
│   └── bad-request.md
└── versions/
    ├── v1-initial.md
    └── v2-current.md
```

**Test**: Use your system for 5 different tasks and refine.

---

## Part 8: Measuring Context Quality

### Quality Metrics

**1. Relevance Score**
```python
def calculate_relevance(context: str, task: str) -> float:
    """
    How relevant is context to task?
    1.0 = Perfect, all relevant
    0.5 = Half relevant, half noise
    0.0 = Completely irrelevant
    """
    relevant_items = count_relevant(context, task)
    total_items = count_total(context)
    return relevant_items / total_items
```

**2. Completeness Score**
```python
def calculate_completeness(context: str, task: str) -> float:
    """
    Does context have everything needed?
    1.0 = Everything needed
    0.5 = Missing half of needed info
    0.0 = Missing everything
    """
    required_items = list_required(task)
    provided_items = extract_items(context)
    return len(provided_items & required_items) / len(required_items)
```

**3. Efficiency Score**
```python
def calculate_efficiency(context: str) -> float:
    """
    Information density - no wasted tokens
    1.0 = Every token adds value
    0.5 = Half the tokens wasted
    0.0 = All noise
    """
    essential_tokens = count_essential(context)
    total_tokens = count_tokens(context)
    return essential_tokens / total_tokens
```

**4. Structure Score**
```python
def calculate_structure(context: str) -> float:
    """
    How well-organized is the context?
    1.0 = Perfect structure
    0.5 = Somewhat organized
    0.0 = Chaotic
    """
    has_sections = has_clear_sections(context)
    has_hierarchy = has_logical_hierarchy(context)
    has_summary = has_summary(context)
    return (has_sections + has_hierarchy + has_summary) / 3
```

**Overall Quality**:
```python
def context_quality_score(context: str, task: str) -> float:
    """Overall context quality score (0-100)."""
    relevance = calculate_relevance(context, task)
    completeness = calculate_completeness(context, task)
    efficiency = calculate_efficiency(context)
    structure = calculate_structure(context)

    # Weighted average
    score = (
        relevance * 0.35 +      # Most important
        completeness * 0.30 +   # Very important
        efficiency * 0.20 +     # Important
        structure * 0.15        # Nice to have
    )

    return score * 100  # Convert to 0-100 scale
```

### Exercise 8.1: Score Your Context

**Task**: Score context from your last 5 AI interactions

For each interaction:
1. Retrieve the context you provided
2. Score it using the metrics above
3. Identify weaknesses
4. Rewrite to improve score
5. Compare results

**Template**:
```markdown
## Interaction 1

### Original Context
[Paste context]

### Scores
- Relevance: __/10
- Completeness: __/10
- Efficiency: __/10
- Structure: __/10
- **Overall: __/100**

### Weaknesses
1. [Issue 1]
2. [Issue 2]

### Improved Context
[Rewritten context]

### New Scores
- Relevance: __/10
- Completeness: __/10
- Efficiency: __/10
- Structure: __/10
- **Overall: __/100**

### Improvement: +__points
```

---

## Part 9: Context Anti-Patterns (Advanced)

### Anti-Pattern 5: The Kitchen Sink 🚰

**Problem**: Including "everything just in case"

```python
# Asking about a login function but including:
"""
Here's my entire project:
- All 50 models
- All 30 services
- All 40 API endpoints
- All configuration files
- All utility functions
- All tests
- All migrations
- All documentation
"""
```

**Fix**: Include only what's directly related
```python
"""
I need help with the login function.

Relevant code:
- Auth service (login method)
- User model (needed fields only)
- JWT utility (token generation)

That's it.
"""
```

### Anti-Pattern 6: The Time Traveler ⏰

**Problem**: Providing outdated context

```python
"""
Here's our old authentication code: [deprecated code]
We're migrating to: [new approach]
But some parts still use: [another old approach]
And we're planning to: [future approach]

What should I do?
"""
```

**Fix**: Provide current state only
```python
"""
Current authentication (as of today):
[Current code only]

Task: Add password reset feature
"""
```

### Anti-Pattern 7: The Mystery Novel 📚

**Problem**: Making AI guess what you want

```python
"""
Here's a bunch of code.
Something is wrong.
Can you find it?
"""
```

**Fix**: Be specific about the problem
```python
"""
Problem: Users can't log in after password reset

Symptoms:
- Reset email received
- New password set
- Login fails with "Invalid credentials"

Relevant code:
[Password reset function]
[Login function]
[Password hashing code]

Expected: Login should work with new password
Actual: Always fails
"""
```

### Anti-Pattern 8: The Assumption Trap 🪤

**Problem**: Assuming AI remembers previous context

```python
// Session 1 (Yesterday)
User: "Here's my React app structure: [details]"

// Session 2 (Today)
User: "Add a new component to the navbar"
AI: "I don't know your navbar structure"
User: "But I told you yesterday!"
```

**Fix**: Re-establish context
```python
// Session 2 (Today)
User: "Quick context: React app with navbar in src/components/Navbar.tsx

Current Navbar structure:
[Paste Navbar component]

Task: Add a user menu dropdown
"
```

### Exercise 9.1: Anti-Pattern Detection

Review these examples and identify the anti-pattern:

**Example A**:
```python
"""
I'm working on something and it's not working.
Here's all my code: [10,000 lines]
Help!
"""
```
Anti-pattern: _______________
Fix: _______________

**Example B**:
```python
"""
Remember that API we talked about last week?
Can you add authentication to it?
"""
```
Anti-pattern: _______________
Fix: _______________

**Example C**:
```python
"""
Here's my code from 2019: [old code]
Here's my code from 2020: [different code]
Here's my code from 2021: [another approach]
Here's my current code: [current code]
Here's what I'm planning: [future code]

Which one should I use?
"""
```
Anti-pattern: _______________
Fix: _______________

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Structure context using proven patterns
- [ ] Choose appropriate context levels for different tasks
- [ ] Optimize context for minimal token usage
- [ ] Create reusable context templates
- [ ] Manage multi-file context effectively
- [ ] Adapt context for different AI tools
- [ ] Build a personal context management system
- [ ] Measure and improve context quality
- [ ] Avoid all common context anti-patterns
- [ ] Achieve 80%+ first-try success rate with AI

## Real-World Application

Apply these strategies to:

1. **Daily Development**: Use templates for common tasks
2. **Code Reviews**: Provide context for AI-assisted reviews
3. **Debugging**: Structure bug reports for AI help
4. **Learning**: Build context for exploring new concepts
5. **Documentation**: Generate docs with proper context
6. **Refactoring**: Large-scale refactoring with chunked context

## Context Engineering Principles

### The 5 C's of Effective Context

1. **Clear**: Unambiguous goals and requirements
2. **Complete**: All necessary information included
3. **Concise**: No unnecessary information
4. **Consistent**: Follow patterns and structures
5. **Correct**: Accurate and up-to-date

### The Context Golden Ratio

For optimal results:
- 20% Goal/Question (what you want)
- 50% Relevant Code/Examples (what AI needs)
- 20% Constraints/Requirements (boundaries)
- 10% Background/Architecture (broader context)

## Final Exercise: Context Masterpiece

**Challenge**: Create the "perfect" context for a complex task

**Scenario**: Add a feature that spans multiple files, requires understanding of architecture, needs to follow patterns, and has specific requirements.

**Your Task**: Craft context that:
1. Scores 90+ on quality metrics
2. Uses appropriate patterns
3. Achieves first-try success
4. Stays under 1000 tokens
5. Could be reused as a template

**Submit**: Your context, the AI's response, and self-evaluation

## Reflection

1. How has your context engineering evolved?
2. What patterns work best for your projects?
3. Where do you still struggle?
4. What will you implement first?
5. How will you measure improvement?

## Further Learning

- Study RAG (Retrieval-Augmented Generation)
- Explore vector databases for context
- Learn prompt engineering techniques
- Research context compression algorithms
- Study how different models handle context

## Key Takeaways

1. **Structure matters more than size**
2. **Examples beat explanations**
3. **Progressive building beats big dumps**
4. **Tools need different strategies**
5. **Quality over quantity always**
6. **Measure to improve**
7. **Build systems, not one-offs**
8. **Iterate on your patterns**

Remember: Effective context engineering is about being a great communicator with AI, not about technical tricks. Clear, structured, relevant context gets results!
