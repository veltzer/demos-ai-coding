
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from repositories import UserRepository
    from validators import UserValidator

# services.py
"""Refactored service layer extracted from before/user_manager.py.

This is a structural sketch showing how the god class splits into focused
collaborators; the method bodies are deliberately elided.
"""

class EmailService:
    def send_welcome_email(self, user_email: str, user_name: str) -> None:
        # Focused on email sending only
        pass


class UserService:
    def __init__(self, repository: UserRepository, validator: UserValidator, email_service: EmailService, cache: Any) -> None:
        self.repository = repository
        self.validator = validator
        self.email_service = email_service
        self.cache = cache

    def create_user(self, data: dict[str, Any]) -> int:
        self.validator.validate_email(data['email'])
        # ... orchestrates the operations
  # body elided in the sketch
        return 0
