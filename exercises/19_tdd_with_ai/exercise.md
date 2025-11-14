# Test-Driven Development (TDD) with AI: Red-Green-Refactor

## Learning Objective
Learn how to practice Test-Driven Development using AI assistance. Understand the red-green-refactor cycle, write tests before implementation, and use AI to generate code that passes your specifications.

## What is TDD?

Test-Driven Development is a software development approach where you:
1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests green

With AI assistance, you can focus on writing clear test specifications, and let the AI help implement the functionality.

## Prerequisites
- Python 3.10+ or JavaScript/TypeScript
- pytest (Python) or Jest (JavaScript)
- Basic understanding of testing concepts
- GitHub Copilot or similar AI assistant

---

## Part 1: TDD Fundamentals

### The TDD Cycle

```txt
+-------------+
|  Write Test |  <- Start here (Red)
|   (Fails)   |
+------+------+
       |
       |
+------+------+
|Implement Min|  <- Make it pass (Green)
|   Code      |
+------+------+
       |
       |
+------+------+
|  Refactor   |  <- Improve (Refactor)
|  & Improve  |
+------+------+
       |
       +----------+
                  |
       +----------+----------+
       | More functionality? |
       |   Yes -> New Test   |
       |   No  -> Done       |
       +---------------------+
```

### Exercise 1.1: Your First TDD Cycle

**Scenario**: Build a password validator

#### Step 1 - RED: Write the test first

```python
# test_password_validator.py
import pytest
from password_validator import PasswordValidator

def test_password_must_be_at_least_8_characters():
    """Test that password requires minimum 8 characters."""
    validator = PasswordValidator()

    # Should fail
    assert validator.validate("abc123") == False
    assert validator.get_errors() == ["Password must be at least 8 characters"]

    # Should pass
    assert validator.validate("abc12345") == True
    assert validator.get_errors() == []

# Run this test - it should FAIL because we haven't written PasswordValidator yet
```

#### Step 2 - GREEN: Use AI to implement minimal code

Prompt for AI:

```python
# Create a PasswordValidator class that makes the test pass
# Requirements from test:
# - validate(password) method that returns bool
# - get_errors() method that returns list of error messages
# - Must check password is at least 8 characters
# - Keep it simple - only implement what the test requires

class PasswordValidator:
    # Let AI implement
```

#### Step 3 - REFACTOR: Improve the code

Once tests pass, ask AI:

```python
# Refactor this PasswordValidator for better code quality:
# - Add type hints
# - Add docstrings
# - Improve variable names
# - Consider edge cases (None, empty string)
# Keep all tests passing!

# Paste the working code here for refactoring
```

---

## Part 2: Building a Feature Test-First

### Project: String Calculator Kata

A classic TDD exercise. Build it step-by-step with tests first.

#### Iteration 1: Basic Addition

**Test First:**

```python
# test_string_calculator.py
import pytest
from string_calculator import StringCalculator

class TestStringCalculator:
    def setup_method(self):
        self.calc = StringCalculator()

    def test_empty_string_returns_zero(self):
        """Empty string should return 0."""
        assert self.calc.add("") == 0

    def test_single_number_returns_that_number(self):
        """Single number should return that number."""
        assert self.calc.add("1") == 1
        assert self.calc.add("5") == 5

    def test_two_numbers_comma_delimited_returns_sum(self):
        """Two numbers separated by comma should return their sum."""
        assert self.calc.add("1,2") == 3
        assert self.calc.add("10,20") == 30

# Run tests - they should fail (Red)
```

**Implement:**

```python
# Now ask AI to implement StringCalculator that passes these tests
# Prompt: "Create StringCalculator class that passes the above tests"
```

#### Iteration 2: Handle Multiple Numbers

**Test First:**

```python
def test_multiple_numbers_returns_sum(self):
    """Multiple numbers should return their sum."""
    assert self.calc.add("1,2,3") == 6
    assert self.calc.add("1,2,3,4,5") == 15
    assert self.calc.add("10,20,30,40") == 100

# Run tests - should fail
```

**Implement:**
Ask AI to modify the `add` method to handle any amount of numbers.

#### Iteration 3: Handle Newlines as Delimiters

**Test First:**

```python
def test_newline_as_delimiter(self):
    """Newlines can be used as delimiters."""
    assert self.calc.add("1\n2,3") == 6
    assert self.calc.add("1\n2\n3") == 6
    assert self.calc.add("10\n20,30") == 60

# Run tests - should fail
```

**Implement:**
Ask AI to support both comma and newline delimiters.

#### Iteration 4: Negative Numbers Throw Exception

**Test First:**

```python
def test_negative_numbers_throw_exception(self):
    """Negative numbers should throw exception with the negative number in message."""
    with pytest.raises(ValueError, match="Negatives not allowed: -1"):
        self.calc.add("1,-1,2")

    with pytest.raises(ValueError, match="Negatives not allowed: -1, -2"):
        self.calc.add("1,-1,2,-2")

# Run tests - should fail
```

**Implement:**
Ask AI to add validation for negative numbers.

#### Iteration 5: Numbers Bigger Than 1000 Should Be Ignored

**Test First:**

```python
def test_numbers_bigger_than_1000_ignored(self):
    """Numbers bigger than 1000 should be ignored."""
    assert self.calc.add("2,1001") == 2
    assert self.calc.add("1000,1001,2") == 1002

# Run tests - should fail
```

**Implement:**
Ask AI to filter out numbers > 1000.

#### Iteration 6: Custom Delimiter

**Test First:**

```python
def test_custom_delimiter(self):
    """Support custom delimiter specified in format: //[delimiter]\n[numbers]"""
    assert self.calc.add("//;\n1;2") == 3
    assert self.calc.add("//|\n1|2|3") == 6
    assert self.calc.add("//sep\n1sep2sep3") == 6

# Run tests - should fail
```

**Implement:**
Ask AI to parse custom delimiter syntax.

---

## Part 3: TDD for Real-World Features

### Project: Shopping Cart System

Build a shopping cart using TDD principles.

#### Feature 1: Add Items to Cart

**Test First:**

```python
# test_shopping_cart.py
import pytest
from shopping_cart import ShoppingCart, Product

class TestShoppingCart:
    def setup_method(self):
        self.cart = ShoppingCart()
        self.product1 = Product("Widget", 10.00)
        self.product2 = Product("Gadget", 20.00)

    def test_new_cart_is_empty(self):
        """New cart should have zero items."""
        assert self.cart.item_count() == 0
        assert self.cart.total() == 0.0

    def test_add_single_item(self):
        """Adding an item should increase count and total."""
        self.cart.add_item(self.product1, quantity=1)

        assert self.cart.item_count() == 1
        assert self.cart.total() == 10.00

    def test_add_multiple_items(self):
        """Adding multiple items should accumulate."""
        self.cart.add_item(self.product1, quantity=2)
        self.cart.add_item(self.product2, quantity=1)

        assert self.cart.item_count() == 3
        assert self.cart.total() == 40.00

    def test_add_same_item_twice_combines_quantity(self):
        """Adding same item twice should combine quantities."""
        self.cart.add_item(self.product1, quantity=1)
        self.cart.add_item(self.product1, quantity=2)

        assert self.cart.item_count() == 3
        assert self.cart.total() == 30.00

# Implement Product and ShoppingCart to make tests pass
```

#### Feature 2: Remove Items

**Test First:**

```python
def test_remove_item_completely(self):
    """Removing all quantity of an item should remove it from cart."""
    self.cart.add_item(self.product1, quantity=2)
    self.cart.remove_item(self.product1, quantity=2)

    assert self.cart.item_count() == 0
    assert self.cart.total() == 0.0

def test_remove_partial_quantity(self):
    """Removing partial quantity should reduce count."""
    self.cart.add_item(self.product1, quantity=5)
    self.cart.remove_item(self.product1, quantity=2)

    assert self.cart.item_count() == 3
    assert self.cart.total() == 30.00

def test_remove_item_not_in_cart_raises_error(self):
    """Removing item not in cart should raise error."""
    with pytest.raises(ValueError, match="Product not in cart"):
        self.cart.remove_item(self.product1, quantity=1)

def test_remove_more_than_available_raises_error(self):
    """Removing more quantity than available should raise error."""
    self.cart.add_item(self.product1, quantity=2)

    with pytest.raises(ValueError, match="Not enough quantity"):
        self.cart.remove_item(self.product1, quantity=3)

# Implement remove_item method
```

#### Feature 3: Apply Discounts

**Test First:**

```python
def test_apply_percentage_discount(self):
    """Apply percentage discount to total."""
    self.cart.add_item(self.product1, quantity=2)  # $20
    self.cart.apply_discount(percentage=10)

    assert self.cart.total() == 18.00

def test_apply_fixed_discount(self):
    """Apply fixed amount discount."""
    self.cart.add_item(self.product1, quantity=2)  # $20
    self.cart.apply_discount(amount=5.00)

    assert self.cart.total() == 15.00

def test_discount_cannot_make_total_negative(self):
    """Discount should not make total negative."""
    self.cart.add_item(self.product1, quantity=1)  # $10
    self.cart.apply_discount(amount=20.00)

    assert self.cart.total() == 0.00

def test_only_one_discount_allowed(self):
    """Applying second discount should replace first."""
    self.cart.add_item(self.product1, quantity=2)  # $20
    self.cart.apply_discount(percentage=10)  # $18
    self.cart.apply_discount(percentage=20)  # Should be 20% of $20, not $18

    assert self.cart.total() == 16.00

# Implement discount functionality
```

#### Feature 4: Tax Calculation

**Test First:**

```python
def test_calculate_tax(self):
    """Calculate tax on cart total."""
    self.cart.add_item(self.product1, quantity=2)  # $20
    self.cart.set_tax_rate(0.08)  # 8% tax

    assert self.cart.subtotal() == 20.00
    assert self.cart.tax() == 1.60
    assert self.cart.total() == 21.60

def test_tax_applied_after_discount(self):
    """Tax should be calculated on discounted total."""
    self.cart.add_item(self.product1, quantity=2)  # $20
    self.cart.apply_discount(percentage=10)  # $18
    self.cart.set_tax_rate(0.08)  # 8% tax

    assert self.cart.subtotal() == 18.00
    assert self.cart.tax() == 1.44
    assert self.cart.total() == 19.44

# Implement tax calculations
```

---

## Part 4: TDD with Edge Cases

### Project: Date Range Parser

**Test First - Happy Path:**

```python
# test_date_range_parser.py
import pytest
from datetime import date
from date_range_parser import DateRangeParser

class TestDateRangeParser:
    def setup_method(self):
        self.parser = DateRangeParser()

    def test_parse_iso_date_range(self):
        """Parse ISO format date range."""
        start, end = self.parser.parse("2024-01-01 to 2024-01-31")

        assert start == date(2024, 1, 1)
        assert end == date(2024, 1, 31)

    def test_parse_relative_range_this_week(self):
        """Parse 'this week' to date range."""
        start, end = self.parser.parse("this week")

        # Should return Monday to Sunday of current week
        assert start.weekday() == 0  # Monday
        assert end.weekday() == 6    # Sunday
        assert (end - start).days == 6

    def test_parse_relative_range_last_month(self):
        """Parse 'last month' to date range."""
        start, end = self.parser.parse("last month")

        # Should return first and last day of previous month
        assert start.day == 1
        # End should be last day of previous month
```

**Test First - Edge Cases:**

```python
def test_invalid_date_format_raises_error(self):
    """Invalid date format should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid date format"):
        self.parser.parse("not a date")

def test_start_date_after_end_date_raises_error(self):
    """Start date after end date should raise ValueError."""
    with pytest.raises(ValueError, match="Start date must be before end date"):
        self.parser.parse("2024-12-31 to 2024-01-01")

def test_empty_string_raises_error(self):
    """Empty string should raise ValueError."""
    with pytest.raises(ValueError, match="Date range cannot be empty"):
        self.parser.parse("")

def test_none_input_raises_error(self):
    """None input should raise TypeError."""
    with pytest.raises(TypeError, match="Date range must be a string"):
        self.parser.parse(None)

def test_partial_date_range_raises_error(self):
    """Incomplete date range should raise ValueError."""
    with pytest.raises(ValueError):
        self.parser.parse("2024-01-01 to")

# Implement robust parser with proper error handling
```

---

## Part 5: TDD with Mock Objects

### Project: Weather Service Client

**Test First - Using Mocks:**

```python
# test_weather_client.py
import pytest
from unittest.mock import Mock, patch
from weather_client import WeatherClient
from weather_client import APIException, NetworkException

class TestWeatherClient:
    def setup_method(self):
        self.client = WeatherClient(api_key="test_key")

    @patch('weather_client.requests.get')
    def test_get_current_temperature_success(self, mock_get):
        """Test successful temperature retrieval."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "temperature": 72.5,
            "conditions": "sunny"
        }
        mock_get.return_value = mock_response

        # Act
        temp = self.client.get_current_temperature("New York")

        # Assert
        assert temp == 72.5
        mock_get.assert_called_once()

    @patch('weather_client.requests.get')
    def test_api_error_raises_exception(self, mock_get):
        """Test that API errors are handled properly."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIException, match="API returned status 500"):
            self.client.get_current_temperature("New York")

    @patch('weather_client.requests.get')
    def test_network_timeout_raises_exception(self, mock_get):
        """Test that network timeouts are handled."""
        # Arrange
        import requests
        mock_get.side_effect = requests.Timeout("Connection timeout")

        # Act & Assert
        with pytest.raises(NetworkException, match="Network timeout"):
            self.client.get_current_temperature("New York")

    @patch('weather_client.requests.get')
    def test_invalid_json_response_raises_exception(self, mock_get):
        """Test that invalid JSON is handled."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIException, match="Invalid response format"):
            self.client.get_current_temperature("New York")

    @patch('weather_client.requests.get')
    def test_cache_prevents_duplicate_requests(self, mock_get):
        """Test that repeated requests use cache."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 72.5}
        mock_get.return_value = mock_response

        # Act
        temp1 = self.client.get_current_temperature("New York")
        temp2 = self.client.get_current_temperature("New York")

        # Assert
        assert temp1 == temp2
        mock_get.assert_called_once()  # Only called once due to caching

# Implement WeatherClient with caching and error handling
```

---

## Part 6: Property-Based Testing

Use hypothesis for property-based testing.

```python
# test_string_utils.py
import pytest
from hypothesis import given, strategies as st
from string_utils import reverse_string, is_palindrome, title_case

class TestStringUtils:
    @given(st.text())
    def test_reverse_string_twice_returns_original(self, text):
        """Reversing a string twice should return the original."""
        assert reverse_string(reverse_string(text)) == text

    @given(st.text())
    def test_reverse_string_length_unchanged(self, text):
        """Reversing should not change string length."""
        assert len(reverse_string(text)) == len(text)

    @given(st.text(min_size=1))
    def test_palindrome_of_palindrome(self, text):
        """Any string concatenated with its reverse is a palindrome."""
        palindrome = text + reverse_string(text)
        assert is_palindrome(palindrome)

    @given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))))
    def test_title_case_first_char_uppercase(self, text):
        """Title case should have uppercase first character if alphabetic."""
        if text and text[0].isalpha():
            result = title_case(text)
            assert result[0].isupper()

    @given(st.lists(st.integers()))
    def test_sort_is_idempotent(self, lst):
        """Sorting a sorted list should not change it."""
        from string_utils import sort_list
        sorted_once = sort_list(lst)
        sorted_twice = sort_list(sorted_once)
        assert sorted_once == sorted_twice

# Implement functions that satisfy these properties
```

---

## Part 7: TDD Best Practices with AI

### Practice 1: Test Names Tell a Story

**Good Test Names:**

```python
# Clear and descriptive
def test_user_cannot_login_with_incorrect_password():
    pass

def test_cart_total_includes_shipping_when_under_minimum():
    pass

def test_expired_token_returns_401_unauthorized():
    pass

# Bad Test Names:
def test_login():  # Too vague
    pass

def test_case_1():  # Meaningless
    pass

def test_it_works():  # Not specific
    pass
```

### Practice 2: Arrange-Act-Assert Pattern

```python
def test_adding_item_to_cart_increases_total():
    # Arrange - Set up test data
    cart = ShoppingCart()
    product = Product("Widget", price=10.00)

    # Act - Perform the action
    cart.add_item(product, quantity=2)

    # Assert - Verify the outcome
    assert cart.total() == 20.00
```

### Practice 3: One Assertion Per Test (Generally)

```python
# Prefer this:
def test_empty_cart_has_zero_items():
    cart = ShoppingCart()
    assert cart.item_count() == 0

def test_empty_cart_has_zero_total():
    cart = ShoppingCart()
    assert cart.total() == 0.0

# Over this:
def test_empty_cart():
    cart = ShoppingCart()
    assert cart.item_count() == 0
    assert cart.total() == 0.0
    assert cart.is_empty() == True
    # If first assertion fails, you don't know about the others
```

### Practice 4: Test Behavior, Not Implementation

```python
# Good - Tests behavior
def test_user_is_notified_when_order_ships():
    order = Order()
    order.ship()

    assert order.status == "shipped"
    assert notification_was_sent_to(order.customer_email)

# Bad - Tests implementation details
def test_ship_method_calls_email_service():
    order = Order()
    order.ship()

    assert order._email_service.send.called == True  # Internal detail
```

---

## Part 8: Advanced TDD Scenarios

### Scenario 1: API Rate Limiter

**Full TDD Implementation:**

```python
# test_rate_limiter.py
import pytest
import time
from rate_limiter import RateLimiter, RateLimitExceeded

class TestRateLimiter:
    def test_allows_requests_within_limit(self):
        """Should allow requests within rate limit."""
        limiter = RateLimiter(max_requests=3, time_window=1)

        assert limiter.try_request("user1") == True
        assert limiter.try_request("user1") == True
        assert limiter.try_request("user1") == True

    def test_blocks_requests_exceeding_limit(self):
        """Should block requests exceeding rate limit."""
        limiter = RateLimiter(max_requests=3, time_window=1)

        limiter.try_request("user1")
        limiter.try_request("user1")
        limiter.try_request("user1")

        assert limiter.try_request("user1") == False

    def test_allows_requests_after_window_expires(self):
        """Should allow requests after time window expires."""
        limiter = RateLimiter(max_requests=2, time_window=0.5)

        limiter.try_request("user1")
        limiter.try_request("user1")
        assert limiter.try_request("user1") == False

        time.sleep(0.6)  # Wait for window to expire
        assert limiter.try_request("user1") == True

    def test_different_users_have_separate_limits(self):
        """Each user should have independent rate limits."""
        limiter = RateLimiter(max_requests=2, time_window=1)

        limiter.try_request("user1")
        limiter.try_request("user1")

        # user1 exhausted, but user2 should still work
        assert limiter.try_request("user2") == True
        assert limiter.try_request("user2") == True

    def test_get_remaining_requests(self):
        """Should return number of remaining requests."""
        limiter = RateLimiter(max_requests=5, time_window=1)

        assert limiter.get_remaining("user1") == 5

        limiter.try_request("user1")
        assert limiter.get_remaining("user1") == 4

        limiter.try_request("user1")
        limiter.try_request("user1")
        assert limiter.get_remaining("user1") == 2

    def test_get_time_until_reset(self):
        """Should return seconds until rate limit resets."""
        limiter = RateLimiter(max_requests=1, time_window=10)

        limiter.try_request("user1")
        time_until_reset = limiter.get_time_until_reset("user1")

        assert 9 <= time_until_reset <= 10

# Now implement RateLimiter to pass all tests
```

### Scenario 2: Retry Logic with Exponential Backoff

**Test-Driven Implementation:**

```python
# test_retry_handler.py
import pytest
from unittest.mock import Mock
from retry_handler import retry_with_backoff, MaxRetriesExceeded

class TestRetryHandler:
    def test_succeeds_on_first_attempt(self):
        """Should return immediately if operation succeeds."""
        operation = Mock(return_value="success")

        result = retry_with_backoff(operation, max_retries=3)

        assert result == "success"
        assert operation.call_count == 1

    def test_retries_on_failure(self):
        """Should retry failed operation."""
        operation = Mock(side_effect=[Exception("fail"), "success"])

        result = retry_with_backoff(operation, max_retries=3)

        assert result == "success"
        assert operation.call_count == 2

    def test_exponential_backoff_delays(self):
        """Should use exponential backoff between retries."""
        operation = Mock(side_effect=[
            Exception("fail"),
            Exception("fail"),
            "success"
        ])

        start_time = time.time()
        result = retry_with_backoff(
            operation,
            max_retries=3,
            initial_delay=0.1,
            backoff_factor=2
        )
        elapsed = time.time() - start_time

        # First retry: 0.1s, second retry: 0.2s = ~0.3s total
        assert 0.25 <= elapsed <= 0.4
        assert result == "success"

    def test_raises_after_max_retries(self):
        """Should raise MaxRetriesExceeded after all attempts fail."""
        operation = Mock(side_effect=Exception("persistent failure"))

        with pytest.raises(MaxRetriesExceeded) as exc_info:
            retry_with_backoff(operation, max_retries=3)

        assert operation.call_count == 3
        assert "persistent failure" in str(exc_info.value)

    def test_custom_exception_filter(self):
        """Should only retry on specific exceptions."""
        from requests import Timeout, HTTPError

        operation = Mock(side_effect=HTTPError("404"))

        # Should not retry on HTTPError 404
        with pytest.raises(HTTPError):
            retry_with_backoff(
                operation,
                max_retries=3,
                retry_exceptions=(Timeout,)  # Only retry Timeout
            )

        assert operation.call_count == 1

# Implement retry_with_backoff decorator/function
```

---

## Part 9: TDD Anti-Patterns to Avoid

### Anti-Pattern 1: Testing Implementation Details

**Bad:**
```python
def test_user_repository_uses_correct_sql():
    """Don't test SQL queries directly."""
    repo = UserRepository()
    query = repo._build_query()  # Accessing internal method
    assert "SELECT * FROM users" in query  # Testing implementation
```

**Good:**
```python
def test_user_repository_returns_active_users():
    """Test the behavior, not how it's done."""
    repo = UserRepository()
    users = repo.get_active_users()
    assert all(user.is_active for user in users)
```

### Anti-Pattern 2: Fragile Tests (Too Many Mocks)

**Bad:**
```python
def test_order_processing():
    # Too many mocks = fragile test
    mock_db = Mock()
    mock_email = Mock()
    mock_payment = Mock()
    mock_inventory = Mock()
    mock_shipping = Mock()
    mock_logger = Mock()
    # ... test becomes unmaintainable
```

**Good:**

```python
def test_order_processing():
    # Use test doubles for external dependencies only
    payment_service = FakePaymentService()
    order_processor = OrderProcessor(payment_service)

    order = order_processor.process(valid_order_data)

    assert order.status == "processed"
```

### Anti-Pattern 3: Tests That Don't Test Anything

**Bad:**

```python
def test_user_creation():
    user = User("john", "john@example.com")
    # No assertions! Test passes but doesn't verify anything
```

**Good:**

```python
def test_user_creation():
    user = User("john", "john@example.com")

    assert user.username == "john"
    assert user.email == "john@example.com"
    assert user.is_active == True
```

---

## Part 10: Complete TDD Project

### Project: Todo List API

Build a complete RESTful API using TDD.

#### Step 1: Model Tests

```python
# test_todo.py
import pytest
from datetime import datetime
from models import Todo

class TestTodo:
    def test_create_todo_with_required_fields(self):
        todo = Todo(title="Buy milk")

        assert todo.title == "Buy milk"
        assert todo.completed == False
        assert isinstance(todo.created_at, datetime)
        assert todo.id is not None

    def test_cannot_create_todo_without_title(self):
        with pytest.raises(ValueError, match="Title is required"):
            Todo(title="")

    def test_mark_todo_as_completed(self):
        todo = Todo(title="Task")
        todo.mark_completed()

        assert todo.completed == True
        assert todo.completed_at is not None

    def test_mark_todo_as_incomplete(self):
        todo = Todo(title="Task")
        todo.mark_completed()
        todo.mark_incomplete()

        assert todo.completed == False
        assert todo.completed_at is None

# Implement Todo model
```

#### Step 2: Repository Tests

```python
# test_todo_repository.py
import pytest
from repository import TodoRepository
from models import Todo

class TestTodoRepository:
    def setup_method(self):
        self.repo = TodoRepository(":memory:")  # In-memory database

    def test_save_and_retrieve_todo(self):
        todo = Todo(title="Test task")
        saved_todo = self.repo.save(todo)

        retrieved = self.repo.find_by_id(saved_todo.id)

        assert retrieved.id == saved_todo.id
        assert retrieved.title == "Test task"

    def test_find_all_returns_all_todos(self):
        self.repo.save(Todo(title="Task 1"))
        self.repo.save(Todo(title="Task 2"))

        all_todos = self.repo.find_all()

        assert len(all_todos) == 2

    def test_delete_todo(self):
        todo = self.repo.save(Todo(title="Task"))
        self.repo.delete(todo.id)

        assert self.repo.find_by_id(todo.id) is None

    def test_update_todo(self):
        todo = self.repo.save(Todo(title="Original"))
        todo.title = "Updated"

        self.repo.update(todo)
        retrieved = self.repo.find_by_id(todo.id)

        assert retrieved.title == "Updated"

# Implement TodoRepository
```

#### Step 3: API Tests

```python
# test_api.py
import pytest
from flask import Flask
from api import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

class TestTodoAPI:
    def test_get_todos_empty_list(self, client):
        response = client.get('/api/todos')

        assert response.status_code == 200
        assert response.json == []

    def test_create_todo(self, client):
        response = client.post('/api/todos', json={
            'title': 'New task'
        })

        assert response.status_code == 201
        assert response.json['title'] == 'New task'
        assert response.json['completed'] == False

    def test_create_todo_without_title_fails(self, client):
        response = client.post('/api/todos', json={})

        assert response.status_code == 400
        assert 'title' in response.json['error']

    def test_get_todo_by_id(self, client):
        # Create a todo
        create_response = client.post('/api/todos', json={
            'title': 'Test task'
        })
        todo_id = create_response.json['id']

        # Get the todo
        response = client.get(f'/api/todos/{todo_id}')

        assert response.status_code == 200
        assert response.json['id'] == todo_id

    def test_get_nonexistent_todo_returns_404(self, client):
        response = client.get('/api/todos/999')

        assert response.status_code == 404

    def test_update_todo(self, client):
        # Create
        create_response = client.post('/api/todos', json={
            'title': 'Original'
        })
        todo_id = create_response.json['id']

        # Update
        response = client.put(f'/api/todos/{todo_id}', json={
            'title': 'Updated'
        })

        assert response.status_code == 200
        assert response.json['title'] == 'Updated'

    def test_mark_todo_completed(self, client):
        # Create
        create_response = client.post('/api/todos', json={
            'title': 'Task'
        })
        todo_id = create_response.json['id']

        # Complete
        response = client.patch(f'/api/todos/{todo_id}/complete')

        assert response.status_code == 200
        assert response.json['completed'] == True

    def test_delete_todo(self, client):
        # Create
        create_response = client.post('/api/todos', json={
            'title': 'Task'
        })
        todo_id = create_response.json['id']

        # Delete
        response = client.delete(f'/api/todos/{todo_id}')

        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f'/api/todos/{todo_id}')
        assert get_response.status_code == 404

# Implement Flask API
```

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Write tests before implementation
- [ ] Follow the red-green-refactor cycle
- [ ] Use AI to implement code that passes tests
- [ ] Write clear, descriptive test names
- [ ] Use arrange-act-assert pattern
- [ ] Test edge cases and error conditions
- [ ] Use mocks and test doubles appropriately
- [ ] Practice property-based testing
- [ ] Build complete features test-first
- [ ] Recognize and avoid TDD anti-patterns

## Reflection Questions

1. How did writing tests first change your approach to design?
1. What was challenging about TDD with AI assistance?
1. Did AI-generated code pass tests on the first try?
1. How did you refactor AI-generated code while keeping tests green?
1. What role did test names play in guiding implementation?

## Further Practice

- Implement bowling game kata
- Build URL shortener with TDD
- Create file system watcher with tests first
- Build authentication system using TDD
- Practice TDD with your next work project

Remember: **Tests are documentation that never goes out of date. Write them first!**
