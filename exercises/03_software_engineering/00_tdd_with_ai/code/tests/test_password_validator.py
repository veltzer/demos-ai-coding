import pytest
from src.password_validator import PasswordValidator

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
