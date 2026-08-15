# services.py
"""Refactored service layer extracted from before/user_manager.py.

This is a structural sketch showing how the god class splits into focused
collaborators; the method bodies are deliberately elided.
"""
# mypy: disable-error-code="return"

class EmailService:
    def send_welcome_email(self, user_email: str, user_name: str):
        # Focused on email sending only
        pass


class UserService:
    def __init__(self, repository, validator, email_service, cache):
        self.repository = repository
        self.validator = validator
        self.email_service = email_service
        self.cache = cache

    def create_user(self, data: dict) -> int:
        self.validator.validate_email(data['email'])
        # ... orchestrates the operations
        # pylint: disable=unnecessary-pass  # body elided in the sketch
