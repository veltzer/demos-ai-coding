# Test suite for the TDD exercise. Run it with pytest from the code/
# directory, where `src` is importable; pylint lints from the repo root
# and cannot resolve that, and setup_method is standard pytest style.
# The tests are written first and reference methods PasswordValidator does not
# have yet - that is the point of the exercise, so no-member is expected here.
# pylint: disable=missing-module-docstring,import-error,attribute-defined-outside-init
# pylint: disable=no-member

from src.password_validator import PasswordValidator

def test_password_must_be_at_least_8_characters():
    """Test that password requires minimum 8 characters."""
    validator = PasswordValidator()

    # Should fail
    assert not validator.validate("abc123")
    assert validator.get_errors() == ["Password must be at least 8 characters"]

    # Should pass
    assert validator.validate("abc12345")
    assert validator.get_errors() == []

# Run this test - it should FAIL because we haven't written PasswordValidator yet
