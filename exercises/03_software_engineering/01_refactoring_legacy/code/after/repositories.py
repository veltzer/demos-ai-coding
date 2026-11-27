
from typing import Any

# repositories.py
"""Data-access layer extracted from before/user_manager.py."""

class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.query("SELECT * FROM users WHERE email = ?", email)

    def create(self, user_data: dict[str, Any]) -> int:
        user_id: int = self.db.insert("users", user_data)
        return user_id
