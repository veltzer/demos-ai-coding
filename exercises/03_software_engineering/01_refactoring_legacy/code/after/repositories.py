# repositories.py
class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.query("SELECT * FROM users WHERE email = ?", email)

    def create(self, user_data: dict) -> int:
        return self.db.insert("users", user_data)
