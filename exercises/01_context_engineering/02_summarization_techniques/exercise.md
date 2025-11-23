# Summarization Techniques: The Art of Context Compression

## Learning Objective
Master the critical skill of summarizing code, architecture, and systems to provide AI with efficient, high-quality context. Learn when to summarize versus when to show full detail, and develop systematic approaches to context compression.

## Why Summarization Matters

### The Context Economy Problem

You have limited tokens. Every project decision is:
- **Show full code**: Consume many tokens, risk hitting limits
- **Summarize**: Save tokens, but might lose crucial details
- **Skip entirely**: Save maximum tokens, but AI lacks context

**Summarization is the solution**: Convey maximum meaning with minimum tokens.

### Real-World Example

**Without Summarization** (2000 tokens):

```python
# [Full UserRepository - 200 lines]
# [Full ProductRepository - 200 lines]
# [Full OrderRepository - 200 lines]
# [Full PaymentRepository - 200 lines]
# [Full all their models - 400 lines]
# [Full all their tests - 600 lines]

# Now I need to add ShippingRepository...
```

**With Summarization** (200 tokens):

```python
"""
CONTEXT: Repository Pattern in Use

We have 4 repositories following this pattern:
- UserRepository: CRUD + email_exists() + find_by_email()
- ProductRepository: CRUD + search() + by_category()
- OrderRepository: CRUD + by_user() + by_status()
- PaymentRepository: CRUD + by_order() + by_status()

All inherit from BaseRepository[T] with:
- get(id) -> T
- create(data) -> T
- update(id, data) -> T
- delete(id) -> bool
- list(filters) -> List[T]

Example (for reference):
"""
class UserRepository(BaseRepository[User]):
    async def email_exists(self, email: str) -> bool:
        return await self.session.query(User).filter_by(email=email).exists()

"""
NOW CREATE: ShippingRepository following this exact pattern
Should have: by_order(), by_status(), mark_delivered()
"""
```

**Result**: 90% token reduction, AI still has everything it needs.

---

## Part 1: Types of Summarization

### Type 1: Architectural Summarization

Summarize system structure and relationships.

**Full Detail** (500 tokens):

```txt
project/
+-- api/
|   +-- __init__.py
|   +-- main.py
|   +-- dependencies.py
|   +-- routes/
|   |   +-- __init__.py
|   |   +-- users.py
|   |   +-- products.py
|   |   +-- orders.py
|   |   +-- auth.py
+-- services/
|   +-- __init__.py
|   +-- user_service.py
|   +-- product_service.py
|   +-- order_service.py
|   +-- auth_service.py
+-- repositories/
|   +-- __init__.py
|   +-- base.py
|   +-- user_repo.py
|   +-- product_repo.py
|   +-- order_repo.py
+-- models/
|   +-- __init__.py
|   +-- user.py
|   +-- product.py
|   +-- order.py
+-- tests/
    +-- test_users.py
    +-- test_products.py
    +-- test_orders.py

[Plus descriptions of each file...]
```

**Summarized** (100 tokens):

```txt
Architecture: 3-tier pattern
- API layer (FastAPI routes) -> Services -> Repositories -> DB
- Each resource: User, Product, Order
- Each has: API endpoint + Service + Repository + Model + Tests
- Dependencies flow: API -> Service -> Repo (injected)
```

### Type 2: Code Functionality Summarization

Summarize what code does, not how.

**Full Code** (300 tokens):

```python
def process_payment(self, order_id: int, payment_data: dict) -> PaymentResult:
    """Process payment for an order."""
    # Validate order exists
    order = self.order_repo.get(order_id)
    if not order:
        raise OrderNotFoundError(f"Order {order_id} not found")

    # Check order status
    if order.status != OrderStatus.PENDING:
        raise InvalidOrderStateError(f"Order {order_id} not pending")

    # Validate payment amount
    if payment_data['amount'] != order.total:
        raise PaymentAmountMismatchError("Amount doesn't match order total")

    # Process with payment gateway
    try:
        gateway_response = self.payment_gateway.charge(
            amount=payment_data['amount'],
            card=payment_data['card'],
            metadata={'order_id': order_id}
        )
    except GatewayError as e:
        self.logger.error(f"Gateway error: {e}")
        raise PaymentProcessingError("Payment gateway failed")

    # Update order status
    if gateway_response.success:
        order.status = OrderStatus.PAID
        order.payment_id = gateway_response.transaction_id
        self.order_repo.update(order)
        self.logger.info(f"Order {order_id} paid successfully")
        return PaymentResult(success=True, transaction_id=gateway_response.transaction_id)
    else:
        self.logger.warning(f"Payment declined: {gateway_response.error}")
        return PaymentResult(success=False, error=gateway_response.error)
```

**Summarized** (50 tokens):

```python
def process_payment(order_id, payment_data) -> PaymentResult:
    """
    Process payment: validates order exists + is pending + amount matches,
    charges via payment gateway, updates order status if successful.
    Returns PaymentResult(success, transaction_id/error).
    """
```

### Type 3: Pattern Summarization

Summarize repeated patterns across codebase.

**Full Examples** (1000 tokens):

```python
# Example 1: UserService
class UserService:
    def __init__(self, repo: UserRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    async def create(self, data: UserCreate) -> User:
        try:
            self.logger.info(f"Creating user: {data.email}")
            # validation...
            user = await self.repo.create(data)
            self.logger.info(f"User created: {user.id}")
            return user
        except Exception as e:
            self.logger.error(f"User creation failed: {e}")
            raise

# Example 2: ProductService
class ProductService:
    def __init__(self, repo: ProductRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    async def create(self, data: ProductCreate) -> Product:
        try:
            self.logger.info(f"Creating product: {data.name}")
            # validation...
            product = await self.repo.create(data)
            self.logger.info(f"Product created: {product.id}")
            return product
        except Exception as e:
            self.logger.error(f"Product creation failed: {e}")
            raise

# [3 more similar examples...]
```

**Summarized** (100 tokens):

```python
"""
SERVICE PATTERN (used by all 5 services):

class XyzService:
    def __init__(self, repo: XyzRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    async def create(self, data: XyzCreate) -> Xyz:
        try:
            self.logger.info(f"Creating...")
            result = await self.repo.create(data)
            self.logger.info(f"Created: {result.id}")
            return result
        except Exception as e:
            self.logger.error(f"Creation failed: {e}")
            raise

All services follow this: inject repo + logger, log before/after, catch/log errors.
"""
```

### Type 4: Data Model Summarization

Summarize models and their relationships.

**Full Models** (600 tokens):

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Numeric(10, 2))
    status = Column(Enum(OrderStatus))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

# [3 more full model definitions...]
```

**Summarized** (100 tokens):

```python
"""
DATA MODELS:

User: id, email, username, password_hash, name, timestamps
  +-> Orders (one-to-many)
  +-> Addresses (one-to-many)

Order: id, user_id, total, status, timestamps
  +-> User (many-to-one)
  +-> OrderItems (one-to-many)
  +-> Payment (one-to-one)

Product: id, name, price, inventory, timestamps
  +-> OrderItems (one-to-many)

All use SQLAlchemy ORM with standard columns + relationships.
For full schema: models/__init__.py
"""
```

### Exercise 1.1: Practice Different Summarization Types

You have a complex authentication system. Practice each type:

**Given**: A full authentication system with:
- 5 files (models, services, middleware, utils, config)
- 800 lines total
- JWT tokens, refresh tokens, password reset, email verification

**Task A**: Write architectural summary (under 100 tokens)

**Task B**: Write functionality summary for each major component (under 50 tokens each)

**Task C**: Write pattern summary (under 100 tokens)

**Task D**: Write data model summary (under 75 tokens)

**Compare**: Which type of summary is most useful for different tasks?

---

## Part 2: When to Summarize vs. Show Detail

### The Decision Matrix

| Scenario | Summarize | Show Detail |
|----------|-----------|-------------|
| Establishing context | v | |
| Showing pattern to follow | | v |
| Multiple similar files | v | |
| Where bug occurs | | v |
| Architecture overview | v | |
| Code to be modified | | v |
| Unrelated dependencies | v | |
| Related examples | | v |
| Historical context | v | |
| Specific error location | | v |

### Strategy: Hierarchical Context

Provide summary first, detail second:

```python
"""
LEVEL 1: HIGH-LEVEL SUMMARY
===========================
E-commerce API with 3 main flows:
- Authentication (JWT-based)
- Product catalog (search, filter, categories)
- Order processing (cart -> checkout -> payment)

LEVEL 2: COMPONENT SUMMARY
===========================
Auth: Login/logout/refresh + email verification + password reset
Products: CRUD + search (Elasticsearch) + inventory management
Orders: Cart management + checkout + payment (Stripe) + order tracking

LEVEL 3: SPECIFIC DETAIL (relevant to your task)
=================================================
Payment Processing (what you're working on):
"""

# Now show full payment processing code
class PaymentProcessor:
    # Full implementation details...
```

### The 80/20 Rule

For most tasks:
- 80% of context = summarized
- 20% of context = full detail (the part being worked on)

**Example**:

```python
"""
PROJECT CONTEXT (summarized - 80%):
- FastAPI backend, PostgreSQL DB, Redis cache
- 15 API endpoints across 4 domains
- Repository pattern for data access
- JWT auth on protected routes
- Pytest for testing

RELEVANT DETAIL (full code - 20%):
Working on: User profile update endpoint
"""

# Show full detail only for:
# 1. Current endpoint
# 2. User model
# 3. User repository
# 4. Related validation

# Summarize everything else
```

### Exercise 2.1: Apply 80/20 Rule

**Scenario**: Adding a new feature to existing project

**Given**:
- 25 files in project
- Adding "product reviews" feature
- Touches 4 files, references 6 others

**Task**:
1. Identify which 20% needs full detail
2. Summarize the 80%
3. Structure context using hierarchical approach
4. Stay under 1000 tokens total

**Measure**:
- Token count: _____
- 80/20 ratio achieved: Yes/No
- Is anything missing: _____

---

## Part 3: Summarization Techniques

### Technique 1: The Signature Summary

Show just function signatures with docstrings:

**Full Implementation** (200 tokens):

```python
class UserService:
    async def create_user(self, data: UserCreate) -> User:
        # 20 lines of implementation
        pass

    async def update_user(self, id: int, data: UserUpdate) -> User:
        # 25 lines of implementation
        pass

    async def delete_user(self, id: int) -> bool:
        # 15 lines of implementation
        pass

    async def verify_email(self, token: str) -> bool:
        # 30 lines of implementation
        pass
```

**Signature Summary** (50 tokens):

```python
class UserService:
    async def create_user(self, data: UserCreate) -> User:
        """Create user, hash password, send verification email."""

    async def update_user(self, id: int, data: UserUpdate) -> User:
        """Update user, validate permissions, log change."""

    async def delete_user(self, id: int) -> bool:
        """Soft delete user, anonymize PII, cancel subscriptions."""

    async def verify_email(self, token: str) -> bool:
        """Verify email token, mark user verified, send welcome email."""
```

### Technique 2: The Example-Only Summary

Show one full example, summarize the rest:

```python
"""
We have 5 API endpoints following this pattern.

FULL EXAMPLE (one only):
"""

@router.post("/users", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        user = await service.create(data)
        return UserResponse.from_orm(user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

"""
OTHER ENDPOINTS (summarized):
- POST /products - Create product (same pattern)
- POST /orders - Create order (same pattern)
- POST /reviews - Create review (same pattern)
- POST /addresses - Create address (same pattern)

All follow: validate input, call service, return response, handle errors.
"""
```

### Technique 3: The Diff Summary

When showing changes, summarize old, show new:

```python
"""
BEFORE (summarized):
- Used session-based auth with Flask-Login
- Sessions stored in Redis
- 30-day expiration
- No refresh mechanism

AFTER (detailed):
"""

# New JWT-based authentication
class JWTAuthService:
    def generate_tokens(self, user: User) -> TokenPair:
        """Generate access (15min) and refresh (30day) tokens."""
        access_token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=15)},
            self.secret_key
        )
        refresh_token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=30)},
            self.secret_key
        )
        return TokenPair(access=access_token, refresh=refresh_token)
```

### Technique 4: The Dependency Tree Summary

Show relationships without implementation:

```python
"""
DEPENDENCY TREE:

API Endpoints
  +-> Services
       +-> Repositories
            +-> Database Models

Example flow: POST /users
  +-> UserService.create()
       +-> UserRepository.create()
            +-> User model -> database

All layers use dependency injection.
Services inject repositories, APIs inject services.
"""
```

### Technique 5: The Stats Summary

Use numbers to convey scope:

```python
"""
CODEBASE STATS:
- 47 API endpoints (12 public, 35 protected)
- 23 database models
- 15 service classes
- 18 repository classes
- 156 unit tests (94% coverage)
- 45 integration tests

Patterns used:
- Repository (18 classes)
- Service Layer (15 classes)
- Factory (8 classes)
- Dependency Injection (everywhere)
"""
```

### Exercise 3.1: Master All Techniques

**Task**: Take a real project (yours or open source) and create summaries using each technique:

1. **Signature Summary**: Main classes/functions
1. **Example-Only**: Show one, summarize rest
1. **Diff Summary**: Recent major change
1. **Dependency Tree**: System relationships
1. **Stats Summary**: Codebase metrics

**Compare**: Which technique works best for which situation?

---

## Part 4: Automated Summarization

### Tool 1: Script-Based Summarization

Create tools to generate summaries:

```python
# summarize_project.py
"""Generate project summary for AI context."""

import os
from pathlib import Path
from collections import defaultdict

def count_files_by_type(directory: str) -> dict:
    """Count files by extension."""
    counts = defaultdict(int)
    for path in Path(directory).rglob('*'):
        if path.is_file():
            counts[path.suffix] += 1
    return dict(counts)

def analyze_python_files(directory: str) -> dict:
    """Analyze Python files for classes, functions."""
    stats = {
        'files': 0,
        'classes': 0,
        'functions': 0,
        'lines': 0
    }

    for path in Path(directory).rglob('*.py'):
        stats['files'] += 1
        with open(path) as f:
            content = f.read()
            stats['lines'] += len(content.split('\n'))
            stats['classes'] += content.count('class ')
            stats['functions'] += content.count('def ')

    return stats

def generate_summary(directory: str) -> str:
    """Generate project summary."""
    file_counts = count_files_by_type(directory)
    py_stats = analyze_python_files(directory)

    summary = f"""
PROJECT SUMMARY
===============

File Counts:
{chr(10).join(f'- {ext}: {count}' for ext, count in sorted(file_counts.items()))}

Python Code:
- Files: {py_stats['files']}
- Classes: {py_stats['classes']}
- Functions: {py_stats['functions']}
- Lines: {py_stats['lines']:,}

Structure:
{generate_tree(directory, max_depth=2)}
"""
    return summary

if __name__ == "__main__":
    print(generate_summary('.'))
```

### Tool 2: AST-Based Analysis

Use Python's AST to extract structure:

```python
import ast
from pathlib import Path

def extract_signatures(filepath: str) -> str:
    """Extract function/class signatures from Python file."""
    with open(filepath) as f:
        tree = ast.parse(f.read())

    signatures = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            signatures.append(f"class {node.name}:")
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = ', '.join(arg.arg for arg in item.args.args)
                    ret = ast.unparse(item.returns) if item.returns else 'None'
                    doc = ast.get_docstring(item) or "No docstring"
                    signatures.append(f"    def {item.name}({args}) -> {ret}:")
                    signatures.append(f'        """{doc}"""')

    return '\n'.join(signatures)

# Usage
summary = extract_signatures('services/user_service.py')
print(summary)
```

### Tool 3: Template-Based Summarization

Create templates for different contexts:

```python
# context_templates.py

ARCHITECTURE_TEMPLATE = """
ARCHITECTURE: {architecture_pattern}

STACK:
- Backend: {backend}
- Database: {database}
- Cache: {cache}
- Auth: {auth}

STRUCTURE:
{structure}

PATTERNS:
{patterns}
"""

CODE_TEMPLATE = """
FILE: {filepath}
PURPOSE: {purpose}
DEPENDENCIES: {dependencies}

PUBLIC API:
{public_methods}

INTERNAL HELPERS:
{internal_methods}
"""

FEATURE_TEMPLATE = """
FEATURE: {feature_name}
STATUS: {status}

FILES INVOLVED:
{files}

ENTRY POINTS:
{entry_points}

DEPENDENCIES:
{dependencies}

TESTS:
{tests}
"""

def generate_context(template_type: str, **kwargs) -> str:
    """Generate context from template."""
    templates = {
        'architecture': ARCHITECTURE_TEMPLATE,
        'code': CODE_TEMPLATE,
        'feature': FEATURE_TEMPLATE
    }
    return templates[template_type].format(**kwargs)
```

### Exercise 4.1: Build Summarization Tools

**Task**: Create a toolkit for your project:

1. **Project summarizer**: Stats + structure
1. **File summarizer**: Extract signatures
1. **Pattern detector**: Find repeated patterns
1. **Context generator**: Template-based contexts

**Requirements**:
- Should run in < 5 seconds
- Output < 500 tokens
- Capture essential information
- Easy to update

---

## Part 5: Summarization Anti-Patterns

### Anti-Pattern 1: The Over-Summarizer

**Problem**: Summarize so much that critical info is lost

```python
# BAD: Too vague
"""
We have a payment system. It processes payments.
"""

# GOOD: Specific enough
"""
Payment system: Stripe integration, supports cards + ACH.
Handles: charge, refund, dispute resolution.
Stores: Payment records + audit logs.
"""
```

### Anti-Pattern 2: The Inconsistent Summarizer

**Problem**: Different detail levels for similar things

```python
# BAD: Inconsistent
"""
UserService: Full 200-line implementation shown
ProductService: "Handles products" (vague)
OrderService: Signature only
PaymentService: Full 300-line implementation shown
"""

# GOOD: Consistent level
"""
All services follow same pattern.

Example (UserService - full detail):
[Show complete implementation]

Others (same pattern):
- ProductService: CRUD + search + inventory
- OrderService: CRUD + by_user + by_status
- PaymentService: charge + refund + disputes
"""
```

### Anti-Pattern 3: The Premature Summarizer

**Problem**: Summarize before understanding scope

```python
# BAD: Summarized too early
User: "Help me fix a bug in payment processing"
You: "Our payment system uses Stripe [summary...]"
User: "No, the bug is in the refund flow specifically"
You: [Wish you'd asked first...]

# GOOD: Ask, then summarize appropriately
User: "Help me fix a bug in payment processing"
You: "Which part? (charge/refund/dispute/reporting)"
User: "Refund flow specifically"
You: [Now provide detailed refund code, summarize rest]
```

### Anti-Pattern 4: The Jargon Summarizer

**Problem**: Use abbreviations/acronyms without explanation

```python
# BAD: Unclear jargon
"""
System uses CQRS with ES, DDD patterns, deployed via K8s with Istio SM.
Auth via OAuth2 ROPC flow with PKCE. Data in PG with Flyway migrations.
"""

# GOOD: Clear explanation
"""
Architecture:
- CQRS (Command Query Responsibility Segregation) with Event Sourcing
- Domain-Driven Design patterns
- Deployed on Kubernetes with Istio service mesh
- OAuth2 Resource Owner Password flow + PKCE
- PostgreSQL database with Flyway migrations
"""
```

### Exercise 5.1: Fix Bad Summaries

**Task**: Here are 5 bad summaries. Fix each one:

**Bad Summary 1**: "We use microservices."

**Bad Summary 2**:

```txt
UserService: [200 lines]
ProductService: [300 lines]
OrderService: does order stuff
PaymentService: [250 lines]
```

**Bad Summary 3**: "Complex auth system with various flows and tokens."

**Bad Summary 4**: "Uses standard patterns. See code for details."

**Bad Summary 5**: "Built with React, Node, Docker, K8s, PG, Redis, Kafka, ES, Prometheus, Grafana."

---

## Part 6: Hierarchical Summarization

### The Pyramid Structure

Layer information from general to specific:

```txt
LAYER 1: SYSTEM OVERVIEW (50 tokens)
LAYER 2: DOMAIN BREAKDOWN (100 tokens)
LAYER 3: COMPONENT DETAILS (200 tokens)
LAYER 4: SPECIFIC CODE (500 tokens)
```

### Example: Hierarchical Context

```python
"""
=== LAYER 1: SYSTEM OVERVIEW ===
E-commerce platform: REST API for product catalog, shopping cart, checkout.
Tech: FastAPI, PostgreSQL, Redis, Stripe. Deployed on AWS ECS.

=== LAYER 2: DOMAIN BREAKDOWN ===
Four domains:
1. Catalog: Products, categories, search (Elasticsearch)
2. Cart: Session-based cart, quantity management, price calculation
3. Checkout: Address validation, tax calculation, order creation
4. Payment: Stripe integration, payment processing, refund handling

=== LAYER 3: COMPONENT DETAILS (for Checkout domain) ===
Checkout flow:
1. AddressValidator: Validates & normalizes shipping addresses (Google Maps API)
2. TaxCalculator: Calculates sales tax by state/zip (TaxJar API)
3. OrderCreator: Creates order records, reserves inventory
4. PaymentProcessor: Charges card via Stripe, handles failures

Each component: Service class + Repository + Tests

=== LAYER 4: SPECIFIC CODE (PaymentProcessor) ===
"""

class PaymentProcessor:
    """Handles payment processing via Stripe."""

    def __init__(
        self,
        stripe_client: StripeClient,
        order_repo: OrderRepository,
        logger: Logger
    ):
        self.stripe = stripe_client
        self.orders = order_repo
        self.logger = logger

    async def process_payment(
        self,
        order_id: int,
        payment_method: str
    ) -> PaymentResult:
        """
        Process payment for order.

        Steps:
        1. Validate order exists and is pending
        2. Create Stripe payment intent
        3. Charge payment method
        4. Update order status
        5. Handle failures with idempotency

        Returns PaymentResult with success/failure + transaction_id/error
        """
        # [Full implementation here...]
```

### When to Use Each Layer

**Layer 1**: Always include (orientation)
**Layer 2**: Include when working across domains
**Layer 3**: Include when working on specific domain
**Layer 4**: Only for code being modified/added

### Exercise 6.1: Build a Hierarchy

**Task**: Take a complex system and build a 4-layer hierarchy:

Requirements:
- Layer 1: Under 50 tokens
- Layer 2: Under 150 tokens
- Layer 3: Under 300 tokens
- Layer 4: Full detail for specific component

Test: Can someone understand the system by reading just Layer 1? Just Layers 1+2?

---

## Part 7: Domain-Specific Summarization

### Frontend Code Summarization

```javascript
// SUMMARY:
// React app, 3 main routes: Dashboard, Profile, Settings
// State: Redux (user, cart, preferences)
// API: Axios with custom hooks (useUser, useCart, useProducts)
// Styling: TailwindCSS + custom components
// Auth: JWT stored in localStorage, auto-refresh

// COMPONENT TREE:
// App
//   +- Header (nav, user menu)
//   +- Dashboard (products grid, filters, cart)
//   +- Profile (user info, orders, addresses)
//   +- Settings (preferences, password, notifications)

// FULL DETAIL (relevant component):
const Dashboard = () => {
  // Implementation...
};
```

### Backend API Summarization

```python
"""
API SUMMARY:
- 23 endpoints across 5 resources (users, products, orders, reviews, admin)
- All use FastAPI with Pydantic validation
- Auth: JWT required except /auth/* and GET /products/*
- Rate limiting: 100 req/min per IP, 1000/min per authenticated user
- Errors: Standard format {error: str, details: dict, code: str}

ENDPOINTS BY RESOURCE:
Users: register, login, profile (get/update), password (change/reset)
Products: list, search, get, create*, update*, delete* (*admin only)
Orders: create, list, get, cancel, track
Reviews: create, list (by product), get, update, delete
Admin: users (list/ban), orders (update status), analytics

FULL DETAIL (Orders endpoint):
"""

@router.post("/orders", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_user),
    cart: CartService = Depends(get_cart_service),
    order: OrderService = Depends(get_order_service)
):
    # Implementation...
```

### Database Schema Summarization

```sql
-- SCHEMA SUMMARY:
-- 12 tables, PostgreSQL 14
-- Normalized to 3NF
-- All tables: id (SERIAL PK), created_at, updated_at
-- Soft deletes: deleted_at (nullable)
-- Indexes: All FKs, email (unique), frequent filters

-- RELATIONSHIPS:
-- users 1:N orders
-- orders 1:N order_items N:1 products
-- orders 1:1 payments
-- users 1:N addresses
-- products N:M categories (product_categories)

-- KEY TABLES:
users: id, email, password_hash, role, is_active
products: id, name, description, price, inventory
orders: id, user_id, total, status, shipping_address_id
order_items: id, order_id, product_id, quantity, price
payments: id, order_id, amount, status, stripe_payment_id

-- FULL SCHEMA (orders table):
CREATE TABLE orders (
    -- Full DDL...
);
```

### Infrastructure Summarization

```yaml
# INFRASTRUCTURE SUMMARY:
# AWS ECS Fargate deployment
# - Production: us-east-1, 3 AZs, 6 tasks (2 per AZ)
# - Staging: us-east-1, 1 AZ, 2 tasks
#
# Components:
# - ALB: Routes to ECS, SSL termination
# - ECS: API containers (FastAPI), auto-scaling 2-10
# - RDS: PostgreSQL 14, Multi-AZ, 2 read replicas
# - ElastiCache: Redis cluster, 3 nodes
# - S3: Static assets, user uploads
# - CloudFront: CDN for S3
#
# Monitoring: CloudWatch + Prometheus + Grafana
# Logging: CloudWatch Logs, 30 day retention
# Secrets: AWS Secrets Manager
# CI/CD: GitHub Actions -> ECR -> ECS

# FULL DETAIL (ECS task definition):
{
  "family": "api-production",
  "taskRoleArn": "...",
  # Full task definition...
}
```

### Exercise 7.1: Domain-Specific Summaries

**Task**: Create summaries for each domain in your project:

1. Frontend (if applicable)
1. Backend/API
1. Database schema
1. Infrastructure/deployment

Requirements:
- Each summary: Under 200 tokens
- Include structure + key details
- Show one full example per domain

---

## Part 8: Measuring Summarization Quality

### Quality Metrics

#### 1. Compression Ratio

```python
compression_ratio = original_tokens / summary_tokens
# Good: 5:1 to 10:1
# Excellent: 10:1 to 20:1
```

#### 2. Information Retention

```python
# Can someone unfamiliar with the code answer these after reading summary?
questions = [
    "What architecture pattern is used?",
    "What are the main components?",
    "How do components interact?",
    "What technologies are involved?",
    "Where would feature X be implemented?"
]

retention_score = correct_answers / total_questions
# Good: > 80%
```

### 3. Actionability

```python
# Can AI complete task with just the summary?
actionable = can_generate_new_code_matching_patterns(summary)
# Good: Yes for new features, No for bug fixes (need details)
```

### 4. Clarity

```python
# Is summary understandable without context?
# No jargon, clear structure, logical flow
clarity_score = readability_score(summary)
# Good: > 8/10
```

### Exercise 8.1: Measure Your Summaries

**Task**: Take 5 summaries you've created and measure:

```markdown
## Summary 1: [Description]

Original tokens: ___
Summary tokens: ___
Compression ratio: ___:1

Information retention test:
Q1: [Question] - Answer: ___ (Correct: Y/N)
Q2: [Question] - Answer: ___ (Correct: Y/N)
Q3: [Question] - Answer: ___ (Correct: Y/N)
Q4: [Question] - Answer: ___ (Correct: Y/N)
Q5: [Question] - Answer: ___ (Correct: Y/N)
Retention score: ___%

Actionable for task: [Task description]
AI can complete: Y/N

Clarity: __/10

Overall quality: __/100
```

---

## Part 9: Real-World Scenarios

### Scenario 1: Onboarding New Feature

**Challenge**: Add "wishlist" feature to e-commerce site

**Poor Approach**:

```txt
[Paste entire codebase - 10,000 lines]
"Add wishlist feature"
```

**Good Approach**:

```txt
CONTEXT: E-commerce API Summary
- 4 existing features: Products, Cart, Orders, Reviews
- All follow: Model -> Repository -> Service -> API pattern
- Auth: JWT required for user-specific data

EXAMPLE (Reviews - similar to wishlist):
class Review(Base):
    user_id, product_id, rating, comment

class ReviewService:
    create_review(), get_user_reviews(), get_product_reviews()

@router.post("/reviews")
async def create_review(...):
    # Validates user owns order with product
    # Creates review
    # Updates product rating

NOW CREATE: Wishlist following same pattern
- User can add/remove products
- View their wishlist
- Check if product in wishlist
- Same security (JWT required)
```

### Scenario 2: Debugging Production Issue

**Challenge**: API returning 500 errors on /orders endpoint

**Poor Approach**:

```txt
[Paste all API code, services, repositories - 5,000 lines]
"It's broken, fix it"
```

**Good Approach**:

```txt
BUG: /orders endpoint 500 errors

CONTEXT (summary):
- FastAPI app, PostgreSQL DB
- Orders flow: API -> OrderService -> OrderRepository -> DB
- Recent changes: Added inventory check before order creation

ERROR:

```txt
SQLAlchemy.exc.IntegrityError: null value in column "inventory_reserved_at"
violates not-null constraint

RELEVANT CODE (full detail):
[Paste OrderService.create_order() - 50 lines]
[Paste Order model - 30 lines]
[Paste recent migration - 20 lines]

QUESTION: Why is inventory_reserved_at null?
```

### Scenario 3: Code Review

**Challenge**: Review PR adding payment processing

**Poor Approach**:

```txt
[Paste all changed files - 800 lines]
"Review this"
```

**Good Approach**:

```txt
CODE REVIEW REQUEST

CONTEXT (summary):
- Adding Stripe payment processing
- Replaces mock payment system
- 4 files changed: models, services, API, tests

WHAT TO REVIEW:
1. Error handling (are all Stripe errors caught?)
2. Idempotency (what if payment succeeds but DB update fails?)
3. Security (is card data properly handled?)
4. Testing (are edge cases covered?)

FULL CODE:
[Paste payment_service.py - 200 lines]
[Paste payment models - 50 lines]
[Paste API endpoint - 100 lines]

Tests summary:
- test_successful_payment
- test_declined_card
- test_network_error
- test_insufficient_funds
[5 more test names...]
```

### Exercise 9.1: Apply to Real Scenarios

**Task**: Choose 3 scenarios from your work:

1. Adding a new feature
1. Fixing a production bug
1. Code review request

For each:
- Write context using summarization techniques
- Stay under 1000 tokens
- Include all necessary information
- Test with AI: Does it give good response?

---

## Part 10: Building a Summarization System

### Your Summarization Toolkit

Create reusable assets:

```txt
.context/
+-- summaries/
|   +-- architecture.md       # System overview
|   +-- api_endpoints.md       # All endpoints summary
|   +-- data_models.md        # Schema summary
|   +-- services.md           # Service layer summary
|   +-- patterns.md           # Code patterns
|   +-- infrastructure.md     # Deployment summary
+-- templates/
|   +-- new_feature.md        # Template for new features
|   +-- bug_fix.md           # Template for bugs
|   +-- code_review.md       # Template for reviews
|   +-- refactoring.md       # Template for refactoring
+-- tools/
|   +-- summarize.py         # Generate summaries
|   +-- extract_signatures.py
|   +-- analyze_structure.py
+-- README.md                # How to use this system
```

### Automation Script

```python
# .context/tools/generate_context.py
"""
Generate context for AI interactions.

Usage:
    python generate_context.py new-feature "wishlist"
    python generate_context.py bug-fix "orders/500-error"
    python generate_context.py code-review "PR-123"
"""

import sys
from pathlib import Path

def generate_new_feature_context(feature_name: str) -> str:
    """Generate context for new feature."""
    arch = Path('.context/summaries/architecture.md').read_text()
    patterns = Path('.context/summaries/patterns.md').read_text()
    template = Path('.context/templates/new_feature.md').read_text()

    return template.format(
        architecture=arch,
        patterns=patterns,
        feature_name=feature_name
    )

def generate_bug_fix_context(bug_description: str) -> str:
    """Generate context for bug fix."""
    # Similar approach...
    pass

def generate_code_review_context(pr_number: str) -> str:
    """Generate context for code review."""
    # Similar approach...
    pass

if __name__ == "__main__":
    context_type = sys.argv[1]
    param = sys.argv[2]

    generators = {
        'new-feature': generate_new_feature_context,
        'bug-fix': generate_bug_fix_context,
        'code-review': generate_code_review_context
    }

    context = generators[context_type](param)
    print(context)
```

### Exercise 10.1: Build Your System

**Task**: Create a complete summarization system:

1. **Summaries folder**: Create summaries of your project
   - Architecture
   - API/endpoints
   - Data models
   - Patterns
   - Infrastructure

1. **Templates folder**: Create templates for common tasks
   - New feature
   - Bug fix
   - Code review
   - Refactoring

1. **Tools folder**: Create generation scripts
   - Project summarizer
   - Context generator
   - Signature extractor

1. **Documentation**: Write README explaining system

1. **Test**: Use system for 5 different tasks, iterate based on results

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Identify what needs summarization vs. full detail
- [ ] Apply 5+ different summarization techniques
- [ ] Achieve 5:1 to 20:1 compression ratios
- [ ] Maintain 80%+ information retention
- [ ] Create hierarchical summaries (4 layers)
- [ ] Summarize frontend, backend, database, infrastructure
- [ ] Avoid summarization anti-patterns
- [ ] Build automated summarization tools
- [ ] Measure summarization quality
- [ ] Have a reusable summarization system

## Key Principles

1. **Summarize 80%, detail 20%** - Most context should be compressed
1. **Hierarchy matters** - Layer from general to specific
1. **Consistency is key** - Similar things need similar treatment
1. **Patterns beat examples** - One pattern > five examples
1. **Actionability test** - Can AI act on this summary?
1. **Automate when possible** - Build tools, don't repeat work
1. **Measure and iterate** - Track what works, improve constantly

## Common Questions

**Q: How do I know if I over-summarized?**
A: If AI asks for clarification or produces wrong results, you lost critical info.

**Q: Should I always summarize?**
A: No. Small codebases (< 1000 lines) may not need summarization.

**Q: What's the ideal compression ratio?**
A: 10:1 is great. 20:1 is excellent. 50:1 probably lost too much.

**Q: How often should I update summaries?**
A: After major changes. Set a reminder to review monthly.

**Q: Can I use AI to generate summaries?**
A: Yes! But review and refine them. AI summaries are starting points.

## Further Learning

- Study information theory and compression
- Learn about knowledge graphs
- Explore documentation best practices
- Research cognitive load theory
- Study technical writing principles

## Final Exercise: Masterpiece Summary

**Challenge**: Create the perfect summary for a complex system

**Requirements**:
- Choose a real system (yours or open-source)
- Create 4-layer hierarchical summary
- Stay under 1500 tokens total
- Achieve 10:1+ compression ratio
- Maintain 90%+ information retention
- Test with AI on 3 different tasks
- All tasks succeed first try

**Deliverables**:
1. Original system overview (how many files/lines)
2. Your 4-layer summary
3. Compression ratio calculation
4. Information retention test results
5. AI task completion results
6. Reflection on what worked/didn't work

## Remember

**Summarization is not about hiding information - it's about highlighting what matters.**

The goal is to give AI (and humans) the most useful context in the least space. Master this skill and you'll multiply your effectiveness with AI coding assistants!
