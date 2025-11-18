# Prompt Engineering: Mastering AI Communication

## Learning Objective
Learn how to craft effective prompts to get the best results from AI coding assistants. Understand different prompting techniques, when to use them, and how to iteratively refine prompts for optimal code generation.

## Instructions
1. Work through each prompting technique with practical examples
1. Compare results from different prompt styles
1. Learn to identify and fix poorly written prompts
1. Develop intuition for effective AI communication
1. Build a personal prompt library for common tasks

## Why Prompt Engineering Matters

The quality of AI-generated code depends heavily on how you ask. A well-crafted prompt can mean the difference between:
- Getting exactly what you need vs. multiple iterations
- Secure, production-ready code vs. vulnerable prototypes
- Following best practices vs. anti-patterns
- Clear, maintainable code vs. confusing implementations

---

## Part 1: Basic Prompt Principles

### Principle 1: Be Specific and Clear

**Bad Prompt:**

```txt
Write a function to sort data
```

**Good Prompt:**

```python
# Write a function to sort a list of dictionaries by a specified key
# The function should:
# - Accept a list of dictionaries and a key name as parameters
# - Support both ascending and descending order
# - Handle missing keys gracefully by placing those items at the end
# - Return a new sorted list without modifying the original
# - Include type hints and a docstring
def sort_dicts_by_key(data: list[dict], key: str, reverse: bool = False) -> list[dict]:
```

**Exercise 1.1:** Improve these vague prompts:

```python
# Bad: "Create a user class"
# Your improved version:

# Bad: "Function for API calls"
# Your improved version:

# Bad: "Parse JSON"
# Your improved version:
```

### Principle 2: Provide Context

**Bad Prompt:**
```python
# Calculate total
def calculate_total(items):
```

**Good Prompt:**
```python
# E-commerce shopping cart system
# Calculate the total price of items in a shopping cart
#
# Context:
# - Each item has: name, price, quantity, tax_rate
# - Apply tax per item based on item's tax_rate
# - Apply discount codes if present (percentage or fixed amount)
# - Round to 2 decimal places
#
# Example item: {"name": "Widget", "price": 29.99, "quantity": 2, "tax_rate": 0.08}
def calculate_cart_total(items: list[dict], discount_code: str = None) -> float:
```

**Exercise 1.2:** Add appropriate context to these prompts:

```python
# Incomplete: "Validate email"
# Add context about: format requirements, domain restrictions, error messages

# Incomplete: "Cache function results"
# Add context about: cache size, eviction policy, thread safety

# Incomplete: "Parse log file"
# Add context about: log format, what to extract, error handling
```

### Principle 3: Specify Format and Style

**Bad Prompt:**

```txt
Create a configuration loader
```

**Good Prompt:**

```python
# Create a configuration loader class following these requirements:
#
# Architecture:
# - Singleton pattern for global access
# - Support YAML and JSON config files
# - Environment variable override capability
# - Validation using dataclasses
#
# Code Style:
# - Use Python 3.10+ features (match/case, type unions)
# - Follow PEP 8 naming conventions
# - Include comprehensive docstrings (Google style)
# - Add type hints for all methods
# - Use pathlib for file operations
#
# Error Handling:
# - Raise ConfigError for missing required fields
# - Log warnings for deprecated config keys
# - Provide helpful error messages with context

class ConfigLoader:
    """Configuration loader with validation and environment override support."""
```

**Exercise 1.3:** Create detailed prompts for:
1. A logging utility that should follow specific patterns
2. A database connection pool with particular requirements
3. A data validation decorator with custom behavior

---

## Part 2: Advanced Prompting Techniques

### Technique 1: Few-Shot Learning (Examples)

Provide examples of input/output to guide the AI's understanding.

### Example: String Transformation

```python
# Create a function that converts strings to title case following these rules:
#
# Examples:
# "hello world" -> "Hello World"
# "the quick-brown fox" -> "The Quick-Brown Fox"
# "API_KEY" -> "API Key"
# "camelCaseString" -> "Camel Case String"
# "snake_case_value" -> "Snake Case Value"
# "kebab-case-name" -> "Kebab Case Name"
#
# Rules inferred from examples:
# - Capitalize first letter of each word
# - Treat underscores, hyphens, and camelCase boundaries as word separators
# - Replace separators with spaces
# - Handle acronyms (consecutive capitals) as single words

def smart_title_case(text: str) -> str:
```

**Exercise 2.1:** Create few-shot prompts for:

```python
# A. Date formatter with multiple input formats
# Provide 5 example conversions showing different input formats
# Input examples:
#   "2024-01-15" ->
#   "01/15/2024" ->
#   "Jan 15, 2024" ->
#   "15-01-2024" ->
#   "2024.01.15" ->
# Your function:


# B. URL slug generator
# Provide 5 examples showing edge cases
# Input examples:
#   "Hello World!" ->
#   "C++ Programming Guide" ->
#   "10 Tips & Tricks" ->
#   "   Extra   Spaces   " ->
#   "Uber cafe resume" ->
# Your function:


# C. File size formatter
# Provide examples for different scales
# Input examples:
#   512 ->
#   1024 ->
#   1048576 ->
#   1073741824 ->
#   1536 ->
# Your function:
```

### Technique 2: Chain of Thought Prompting

Ask the AI to explain its reasoning before providing the solution.

**Example:**

```python
# Problem: Find the longest common substring between two strings
#
# Think through this step-by-step:
# 1. What algorithm should we use? (Consider time complexity)
# 2. What edge cases need handling?
# 3. How should we handle case sensitivity?
# 4. What data structures would be most efficient?
# 5. Are there any optimization opportunities?
#
# After analyzing the above, implement the function:

def longest_common_substring(str1: str, str2: str, case_sensitive: bool = True) -> str:
    """
    Find the longest common substring.

    First, explain your chosen approach and why:


    Then implement below:
    """
```

**Exercise 2.2:** Create chain-of-thought prompts for:

```python
# A. Implement a LRU cache
# Guide the reasoning:
# - What data structures should we use?
# - How do we track recency?
# - What's the time complexity requirement?
# - Thread safety considerations?


# B. Design a rate limiter
# Guide the reasoning:
# - Token bucket vs sliding window?
# - Storage mechanism?
# - Distributed vs single-instance?
# - How to handle clock skew?


# C. Implement depth-first search
# Guide the reasoning:
# - Recursive vs iterative?
# - How to avoid cycles?
# - Memory considerations?
# - How to collect the path?
```

### Technique 3: Constraint-Based Prompting

Explicitly state what to avoid or requirements that must be met.

**Example:**
```python
# Create a password validation function
#
# MUST HAVE:
# - Minimum 12 characters
# - At least one uppercase, lowercase, number, special char
# - No dictionary words (use a common password list)
# - No repeated characters more than 2 times
# - Return detailed feedback on all failures
#
# MUST NOT:
# - Use regex alone (combine with other validation)
# - Allow common patterns (123, abc, qwerty)
# - Store or log the actual password
# - Use deprecated hashlib methods
#
# PERFORMANCE:
# - Must validate in under 10ms for typical passwords
# - Avoid expensive operations in validation
#
# SECURITY:
# - Constant-time comparison where applicable
# - No information leakage about existing passwords

def validate_password(password: str, username: str = None) -> tuple[bool, list[str]]:
```

**Exercise 2.3:** Create constraint-based prompts for:

```python
# A. File upload handler
# MUST HAVE: Size limits, type checking, virus scan, unique naming
# MUST NOT: Execute uploads, store in web root, trust client MIME type
# PERFORMANCE: Stream large files, async processing
# SECURITY: Path traversal prevention, sanitization


# B. SQL query builder
# MUST HAVE: Parameterized queries, support for joins, pagination
# MUST NOT: Allow string concatenation, execute DDL, bypass escaping
# PERFORMANCE: Query plan consideration, index hints
# SECURITY: SQL injection prevention, least privilege


# C. Session management
# MUST HAVE: Secure tokens, expiration, refresh capability
# MUST NOT: Use predictable IDs, store sensitive data, fixed session
# PERFORMANCE: Fast lookup, efficient storage
# SECURITY: CSRF protection, secure cookies, rotation
```

### Technique 4: Role-Based Prompting

Frame the AI as an expert in a specific domain.

**Example:**

```python
# You are a senior security engineer reviewing code for vulnerabilities.
# Analyze this authentication function and:
# 1. Identify all security issues
# 1. Explain the attack vectors
# 1. Provide a secure implementation
# 1. Add security test cases
#
# Code to review:
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    if result:
        session['user_id'] = username
        return True
    return False

# Your expert analysis:
# 1. Issues found:
#
# 1. Attack vectors:
#
# 1. Secure implementation:
#
# 1. Test cases:
```

**Exercise 2.4:** Create role-based prompts for:

```python
# A. As a performance optimization expert
# Review and optimize this data processing function:
def process_data(items):
    result = []
    for item in items:
        if item['active']:
            processed = expensive_operation(item)
            if processed not in result:
                result.append(processed)
    return result


# B. As a code reviewer focused on maintainability
# Review this function for clarity and maintainability:
def f(x, y, z=None):
    a = x if y else y if x else z
    b = [i for i in range(len(x)) if x[i] != y[i]]
    return (a, b)


# C. As a testing expert
# Design comprehensive tests for this edge-case-prone function:
def parse_date_range(date_string):
    # Supports formats like:
    # "2024-01-15 to 2024-01-20"
    # "Jan 15-20, 2024"
    # "last week", "this month", "Q1 2024"
    pass
```

### Technique 5: Iterative Refinement

Start broad, then add requirements incrementally.

**Example - Step 1:**

```python
# Create a basic todo list class
class TodoList:
```

**Step 2 - Add requirements:**
```python
# Enhance the TodoList class to:
# - Support priority levels (low, medium, high)
# - Allow due dates
# - Track completion status
# - Include tags for categorization
```

**Step 3 - Add persistence:**
```python
# Add persistence to TodoList:
# - Save to JSON file
# - Load from file on initialization
# - Auto-save on changes
# - Handle file corruption gracefully
```

**Step 4 - Add search:**
```python
# Add search capabilities:
# - Search by text in title/description
# - Filter by priority, status, tags
# - Sort by various criteria
# - Return results with highlighting
```

**Exercise 2.5:** Practice iterative refinement:

Start with a basic HTTP client, then incrementally add:
1. Basic GET/POST functionality
2. Authentication (Bearer token, Basic auth)
3. Retry logic with exponential backoff
4. Response caching
5. Request/response interceptors
6. Async/await support
7. File upload/download with progress
8. WebSocket support

Document your prompts for each iteration.

---

## Part 3: Domain-Specific Prompts

### Web Development

```python
# Create a React component for a data table
#
# Requirements:
# - TypeScript with strict mode
# - Server-side pagination (10 items per page)
# - Sortable columns (controlled)
# - Filterable with debounced search
# - Row selection with Ctrl/Shift support
# - Accessible (ARIA labels, keyboard navigation)
# - Responsive (mobile-friendly)
# - Loading and error states
# - Empty state with custom message
#
# Props interface:
# - data: Array of objects
# - columns: Column definitions with sorting, filtering
# - onPageChange, onSort, onFilter callbacks
# - loading, error states
#
# Follow these patterns:
# - Use React hooks (useState, useEffect, useMemo)
# - Implement proper TypeScript generics
# - Extract reusable hooks (useDebounce, useSelection)
# - Add JSDoc comments
# - Include usage example

// Your component here:
```

### Data Science / ML

```python
# Create a data preprocessing pipeline for a machine learning model
#
# Context: Predicting customer churn with tabular data
#
# Features:
# - Numerical: age, tenure, monthly_charges, total_charges
# - Categorical: gender, contract_type, payment_method
# - Target: churn (binary)
#
# Requirements:
# - Handle missing values (different strategies per column type)
# - Scale numerical features (StandardScaler)
# - Encode categorical features (OneHotEncoder for nominal, OrdinalEncoder for ordinal)
# - Handle imbalanced classes (SMOTE)
# - Create feature engineering (e.g., charges_per_tenure)
# - Split into train/validation/test (60/20/20)
# - Support sklearn pipeline for reproducibility
# - Add data validation checks
# - Log preprocessing steps and statistics
#
# Return:
# - Processed dataframes
# - Fitted transformers (for inference)
# - Feature importance scores
# - Data quality report

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd

def create_preprocessing_pipeline(df: pd.DataFrame) -> tuple:
```

### DevOps / Infrastructure

```python
# Create a Kubernetes deployment configuration
#
# Application: Python FastAPI service
#
# Requirements:
# - Deployment with 3 replicas
# - Rolling update strategy (maxUnavailable: 1, maxSurge: 1)
# - Resource limits: 512Mi memory, 500m CPU
# - Resource requests: 256Mi memory, 250m CPU
# - Health checks: liveness and readiness probes
#   - Liveness: HTTP GET /health every 10s
#   - Readiness: HTTP GET /ready every 5s
# - Environment variables from ConfigMap and Secret
# - Service: ClusterIP on port 80 -> container port 8000
# - Ingress: TLS enabled, path /api/v1
# - HorizontalPodAutoscaler: 3-10 pods, 70% CPU target
# - PodDisruptionBudget: min available 2
# - ServiceAccount with specific permissions
# - Network policies: allow ingress from ingress-nginx only
#
# Use YAML format with proper labels and annotations
# Include comments explaining critical sections

---
# Your Kubernetes manifests:
```

### Database Design

```sql
-- Design a database schema for a social media platform
--
-- Requirements:
-- 1. Users
--    - Authentication (email, password hash)
--    - Profile (bio, avatar, settings)
--    - Verification status
--
-- 2. Posts
--    - Text content (max 500 chars)
--    - Media attachments (multiple images/videos)
--    - Visibility (public, friends, private)
--    - Edit history
--
-- 3. Relationships
--    - Follow/unfollow
--    - Block users
--    - Friend requests
--
-- 4. Interactions
--    - Likes (users can unlike)
--    - Comments (nested, max 3 levels)
--    - Shares/retweets
--
-- 5. Notifications
--    - Real-time delivery
--    - Read/unread status
--    - Preference settings
--
-- Technical requirements:
-- - Use PostgreSQL features (JSON, arrays, full-text search)
-- - Add appropriate indexes for common queries
-- - Implement soft deletes where appropriate
-- - Add timestamps (created_at, updated_at)
-- - Use UUIDs for primary keys
-- - Add check constraints for data integrity
-- - Create views for common queries
-- - Add triggers for derived data
--
-- Consider:
-- - Query performance for feeds (show posts from followed users)
-- - Notification fan-out (user with 1M followers posts)
-- - Privacy (users shouldn't see blocked users' content)
-- - Data retention policies

-- Your schema:
```

---

## Part 4: Debugging and Refactoring Prompts

### Finding Bugs

```python
# Analyze this code for bugs and issues:
#
# Review for:
# 1. Logic errors
# 2. Edge cases
# 3. Performance issues
# 4. Security vulnerabilities
# 5. Memory leaks
# 6. Race conditions
#
# For each issue found, provide:
# - Description of the bug
# - Why it's a problem
# - How to reproduce
# - Fixed code
# - Test case to prevent regression

def transfer_funds(from_account, to_account, amount):
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        return True
    return False

# Your analysis:
```

### Refactoring

```python
# Refactor this code following SOLID principles
#
# Current issues to address:
# - God class (does too much)
# - Tight coupling
# - No dependency injection
# - Hard to test
# - Violates single responsibility
#
# Refactor to:
# - Separate concerns into focused classes
# - Use dependency injection
# - Add interfaces/protocols
# - Make it testable
# - Follow SOLID principles
# - Improve naming
#
# Original code:

class UserManager:
    def __init__(self):
        self.db = MySQL()
        self.cache = Redis()
        self.email = SMTP()

    def create_user(self, data):
        # Validate data
        if not data['email'] or '@' not in data['email']:
            raise Exception("Invalid email")

        # Check if exists
        existing = self.db.query("SELECT * FROM users WHERE email = ?", data['email'])
        if existing:
            raise Exception("User exists")

        # Hash password
        import hashlib
        data['password'] = hashlib.md5(data['password'].encode()).hexdigest()

        # Insert into DB
        user_id = self.db.insert("users", data)

        # Clear cache
        self.cache.delete("users:*")

        # Send welcome email
        self.email.send(
            to=data['email'],
            subject="Welcome!",
            body="Thanks for signing up!"
        )

        return user_id

# Your refactored code:
```

---

## Part 5: Testing and Documentation Prompts

### Test Generation

```python
# Generate comprehensive tests for this function
#
# Include:
# - Unit tests for all paths
# - Edge cases (empty input, None, special characters)
# - Error cases (invalid input, exceptions)
# - Integration tests (if applicable)
# - Performance tests (if applicable)
# - Property-based tests (if applicable)
#
# Use pytest with:
# - Parametrize for multiple cases
# - Fixtures for setup
# - Mocks for external dependencies
# - Clear test names (test_<scenario>_<expected>)
#
# For each test:
# - Add a docstring explaining what it tests
# - Use arrange-act-assert pattern
# - Include assertions for all relevant conditions

def calculate_discount(price: float, customer_type: str, coupon_code: str = None) -> float:
    """
    Calculate discounted price based on customer type and coupon.

    Customer types:
    - 'regular': no discount
    - 'premium': 10% off
    - 'vip': 20% off

    Coupon codes:
    - 'SAVE10': additional 10% off
    - 'SAVE20': additional 20% off
    - Invalid codes are ignored
    """
    # Implementation here...
    pass

# Your comprehensive test suite:
```

### Documentation

```python
# Add comprehensive documentation to this code
#
# Include:
# 1. Module docstring
# 2. Class docstring with usage examples
# 3. Method docstrings (Google style)
# 4. Type hints
# 5. Inline comments for complex logic
# 6. README section with quick start
# 7. API documentation
#
# Docstring should include:
# - Brief description
# - Detailed explanation
# - Args with types and descriptions
# - Returns with type and description
# - Raises with exception types
# - Examples (doctest format)
# - Notes about edge cases

class DataCache:
    def __init__(self, max_size=100, ttl=3600):
        self._cache = {}
        self._timestamps = {}
        self._max_size = max_size
        self._ttl = ttl

    def get(self, key, default=None):
        if key in self._cache:
            if time.time() - self._timestamps[key] < self._ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return default

    def set(self, key, value):
        if len(self._cache) >= self._max_size:
            oldest = min(self._timestamps, key=self._timestamps.get)
            del self._cache[oldest]
            del self._timestamps[oldest]
        self._cache[key] = value
        self._timestamps[key] = time.time()

# Add your documentation:
```

---

## Part 6: Practical Exercises

### Exercise 6.1: Authentication System

Create prompts to build a complete authentication system with:
- User registration with email verification
- Login with JWT tokens
- Password reset flow
- OAuth integration (Google, GitHub)
- Rate limiting
- Session management
- Two-factor authentication
- Security audit logging

Write your prompts incrementally, starting with the most basic functionality.

### Exercise 6.2: File Processing Pipeline

Create prompts to build a file processing system:
- Watch directory for new files
- Validate file format
- Parse different formats (CSV, JSON, XML, Excel)
- Transform data (clean, normalize, enrich)
- Load into database
- Error handling and retry
- Progress reporting
- Parallel processing

### Exercise 6.3: REST API

Create prompts to build a RESTful API:
- CRUD operations for a resource
- Pagination and filtering
- Sorting and searching
- Authentication middleware
- Input validation
- Error handling
- API documentation (OpenAPI)
- Rate limiting
- Caching
- Logging

### Exercise 6.4: CLI Tool

Create prompts for a command-line tool:
- Argument parsing with subcommands
- Configuration file support
- Interactive mode
- Progress bars and spinners
- Colored output
- Error handling
- Help documentation
- Auto-completion
- Plugins support

---

## Part 7: Anti-Patterns and Common Mistakes

### Mistake 1: Being Too Vague

**Don't:**

```txt
Write a function
```

**Do:**

```python
# Write a function that converts Celsius to Fahrenheit
# Input: float (temperature in Celsius)
# Output: float (temperature in Fahrenheit)
# Formula: F = C * 9/5 + 32
def celsius_to_fahrenheit(celsius: float) -> float:
```

### Mistake 2: Assuming Context

**Don't:**
```python
# Fix the bug
def calculate_total(items):
```

**Do:**
```python
# Bug: The function doesn't handle negative quantities correctly
# Expected: Negative quantities should raise ValueError
# Current: Negative quantities pass through and produce wrong totals
#
# Example of bug:
# calculate_total([{"price": 10, "quantity": -1}])  # Returns -10, should raise error
#
# Fix the function to validate that all quantities are positive before calculation
def calculate_total(items):
```

### Mistake 3: No Success Criteria

**Don't:**
```python
# Optimize this function
def search_data(data, query):
```

**Do:**
```python
# Optimize this function to handle 1M+ records
# Current performance: ~5 seconds for 100K records
# Target performance: <100ms for 1M records
#
# Constraints:
# - Must maintain same functionality
# - Cannot use external databases
# - Memory usage should stay under 512MB
#
# Consider:
# - Indexing strategies
# - Early termination
# - Better data structures
# - Caching common queries
def search_data(data, query):
```

### Mistake 4: Ignoring Error Handling

**Don't:**
```python
# Read file and parse JSON
def load_config():
```

**Do:**
```python
# Read configuration file and parse JSON
#
# Error handling requirements:
# - FileNotFoundError: Create default config and log warning
# - JSONDecodeError: Log error with line number, raise ConfigError
# - PermissionError: Raise with helpful message about file permissions
# - Return validated config or raise ConfigError with details
#
# Default config: {"timeout": 30, "retries": 3, "debug": False}
def load_config(config_path: str = "config.json") -> dict:
```

### Mistake 5: No Examples

**Don't:**
```python
# Parse command line arguments
def parse_args():
```

**Do:**
```python
# Parse command line arguments
#
# Expected formats:
# python script.py --input file.txt --output result.txt --verbose
# python script.py -i file.txt -o result.txt -v
# python script.py file.txt  # Uses defaults for output and verbose
#
# Arguments:
# --input, -i: Input file path (required)
# --output, -o: Output file path (default: output.txt)
# --verbose, -v: Enable verbose logging (flag, default: False)
# --help, -h: Show help message
#
# Return: Namespace object with parsed arguments
def parse_args():
```

---

## Part 8: Building a Prompt Library

Create a personal library of prompts for common tasks. Here's a template:

```markdown
# Prompt Library

## Data Validation

### Email Validator
```python
# Create a comprehensive email validation function
#
# Requirements:
# - RFC 5322 compliant (basic)
# - Check for valid domain
# - Optionally verify domain has MX records
# - Return tuple: (is_valid: bool, error_message: str)
#
# Invalid cases:
# - Missing @ symbol
# - Multiple @ symbols
# - Invalid characters
# - Domain without TLD
# - IP address domains (optionally allow)
#
# Valid cases:
# - user@domain.com
# - user.name+tag@domain.co.uk
# - user@subdomain.domain.com
```

### URL Validator
```python
# [Your template]
```

## API Integration

### REST Client Template

```python
# [Your template]
```

### GraphQL Client Template

```python
# [Your template]
```

## File Operations

### CSV Processor Template

```python
# [Your template]
```

### JSON Schema Validator Template

```python
# [Your template]
```

---

## Part 9: Prompt Optimization Checklist

Before submitting a prompt, check:

**Clarity:**
- [ ] Is the goal clearly stated?
- [ ] Are requirements unambiguous?
- [ ] Are technical terms defined if needed?

**Context:**
- [ ] Have I provided relevant background?
- [ ] Are there examples or use cases?
- [ ] Is the current state explained if refactoring?

**Constraints:**
- [ ] Are performance requirements specified?
- [ ] Are there security considerations?
- [ ] Are dependencies or limitations mentioned?

**Format:**
- [ ] Have I specified the desired code style?
- [ ] Are naming conventions mentioned?
- [ ] Is documentation level specified?

**Testability:**
- [ ] Can success be measured?
- [ ] Are edge cases mentioned?
- [ ] Are error cases defined?

**Completeness:**
- [ ] Are all inputs/outputs defined?
- [ ] Is error handling addressed?
- [ ] Are non-functional requirements included?

---

## Part 10: Advanced Techniques

### Technique: Negative Prompting

Tell the AI what NOT to do:

```python
# Create a secure file upload handler
#
# DO NOT:
# - Trust client-provided MIME types
# - Store files in web-accessible directory
# - Use original filenames without sanitization
# - Execute or eval uploaded content
# - Skip virus scanning
# - Allow unlimited file sizes
# - Use predictable file paths
#
# DO:
# - Verify file type by content (magic bytes)
# - Generate random filenames
# - Store outside web root
# - Scan for malware
# - Limit file size (10MB max)
# - Use secure temp directory
# - Implement rate limiting per user
# - Log all uploads with user info

def handle_file_upload(file, user_id):
```

### Technique: Comparative Prompting

Ask for comparison of approaches:

```python
# Implement a cache with expiration
#
# Compare these approaches:
# 1. Dictionary with timestamps
# 2. OrderedDict with LRU
# 3. Using functools.lru_cache
# 4. Using a decorator pattern
#
# For each approach, explain:
# - Pros and cons
# - Performance characteristics
# - Memory usage
# - Thread safety
# - Best use cases
#
# Then implement the best approach for a web API cache
# with requirements:
# - 1000 item limit
# - 5 minute expiration
# - Thread-safe
# - < 10ms lookup time
```

### Technique: Evolutionary Prompting

Build complexity gradually with feedback:

```python
# Version 1: Basic implementation
# Create a simple LRU cache with get/put operations

# [AI provides implementation]

# Version 2: Add features based on V1
# Enhance the cache to track hit/miss statistics
# Add a method to get current size
# Add a method to clear the cache

# [AI enhances]

# Version 3: Performance optimization
# Profile the implementation
# Identify bottlenecks
# Optimize for 100K operations/second

# [AI optimizes]

# Version 4: Production readiness
# Add comprehensive error handling
# Add logging
# Add metrics collection
# Add thread safety
# Add graceful degradation
```

---

## Part 11: Real-World Scenarios

### Scenario 1: Legacy Code Migration

```python
# You're migrating legacy Python 2.7 code to Python 3.11
#
# Original code issues:
# - Uses deprecated libraries
# - No type hints
# - Poor error handling
# - No tests
# - Unclear variable names
#
# Migration requirements:
# - Modernize to Python 3.11 (use new features)
# - Add type hints everywhere
# - Add comprehensive error handling
# - Write unit tests (pytest)
# - Refactor for clarity
# - Add docstrings
# - Maintain backward compatibility in API
#
# Original code:
import urllib2
import json

def get_data(url):
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    data = resp.read()
    return json.loads(data)

# Your modernized version:
```

### Scenario 2: Performance Critical Code

```python
# You're optimizing a data processing pipeline
#
# Context:
# - Processing 10GB of log files daily
# - Current time: 4 hours
# - Target time: < 30 minutes
# - Running on 16-core machine
# - 64GB RAM available
#
# Current bottlenecks (profiling data):
# - 60% time in parsing (regex heavy)
# - 25% time in database writes (one by one)
# - 10% time in data validation
# - 5% other
#
# Requirements:
# - Reduce processing time
# - Maintain data accuracy
# - Handle memory efficiently
# - Add progress reporting
# - Make it resumable (in case of failure)
#
# Consider:
# - Parallel processing
# - Batch operations
# - Better algorithms
# - Caching
# - Streaming vs loading all
#
# Original code:
def process_logs(log_file, db):
    with open(log_file) as f:
        for line in f:
            match = re.match(COMPLEX_REGEX, line)
            if match:
                data = validate(match.groups())
                db.insert("logs", data)

# Your optimized version:
```

### Scenario 3: Security Audit

```python
# You're conducting a security audit of authentication code
#
# Your role: Senior security engineer
#
# Audit for:
# - Injection vulnerabilities
# - Authentication bypasses
# - Session management issues
# - Password storage
# - Timing attacks
# - CSRF vulnerabilities
# - Rate limiting
# - Information disclosure
#
# For each issue:
# - Severity (critical/high/medium/low)
# - Exploitation scenario
# - Impact
# - Remediation
# - Test case
#
# Code to audit:
from flask import Flask, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = cursor.execute(query).fetchone()

    if result:
        session['username'] = username
        session['is_admin'] = result[3]
        return "Success"
    return "Failed"

# Your security audit report:
```

---

## Part 12: Meta-Prompting

Prompts about prompting:

```python
# Help me improve this prompt:
#
# Original prompt:
# "Write a function to process data"
#
# Context:
# - I'm building an ETL pipeline
# - Processing CSV files from S3
# - Loading into PostgreSQL
# - Need error handling and retries
#
# What's missing from my prompt?
# How can I make it more specific?
# What context should I add?
# What constraints should I specify?
#
# Provide an improved version of the prompt.
```

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Write clear, specific prompts that get good results on the first try
- [ ] Identify and fix vague or ambiguous prompts
- [ ] Choose the right prompting technique for the task
- [ ] Provide appropriate context and constraints
- [ ] Create prompts for different domains and complexity levels
- [ ] Iterate and refine prompts effectively
- [ ] Build a personal library of reusable prompts
- [ ] Recognize when a prompt needs more information
- [ ] Guide AI through complex, multi-step tasks
- [ ] Debug AI-generated code by improving prompts

## Reflection Questions

1. How has your approach to prompting changed?
1. Which techniques were most effective for you?
1. What patterns emerge in your best prompts?
1. How do you handle cases where the AI misunderstands?
1. What would you add to your prompt library?

## Further Learning

- Study prompts that generated excellent code
- Analyze failed prompts to understand why
- Share prompts with team members
- Build domain-specific prompt templates
- Experiment with combining techniques
- Practice prompt debugging (fixing bad output by improving prompt)

---

Remember: **The quality of the code you get is directly related to the quality of the prompt you write.** Invest time in crafting good prompts, and you'll save time in code reviews and debugging.
