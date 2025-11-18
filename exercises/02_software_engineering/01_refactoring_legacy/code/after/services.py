# services.py
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
        pass
