# validators.py
class UserValidator:
    def validate_email(self, email: str) -> None:
        if not '@' in email:
            raise ValueError("Invalid email")

    def validate_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password too short")
