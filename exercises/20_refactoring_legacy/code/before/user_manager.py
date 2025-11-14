# user_manager.py - A 500-line god class
class UserManager:
    def __init__(self):
        self.db = MySQLConnection()
        self.cache = RedisConnection()
        self.email_service = SMTPService()
        self.logger = Logger()
        self.session_store = SessionStore()
        self.file_storage = S3Storage()

    def create_user(self, data):
        # Validate email
        if not '@' in data['email']:
            raise ValueError("Invalid email")

        # Check if user exists
        existing = self.db.query("SELECT * FROM users WHERE email = ?", data['email'])
        if existing:
            raise ValueError("User exists")

        # Hash password
        import hashlib
        hashed = hashlib.md5(data['password'].encode()).hexdigest()
        data['password'] = hashed

        # Insert into database
        user_id = self.db.insert("users", data)

        # Clear cache
        self.cache.delete_pattern("users:*")

        # Send welcome email
        self.email_service.send(
            to=data['email'],
            subject="Welcome!",
            body=self.generate_welcome_email(data)
        )

        # Create session
        session_id = self.session_store.create(user_id)

        # Upload default avatar
        avatar_url = self.file_storage.upload_default_avatar(user_id)
        self.db.update("users", user_id, {"avatar_url": avatar_url})

        # Log action
        self.logger.info(f"User created: {user_id}")

        return user_id

    def login_user(self, email, password):
        # ... another 50 lines of mixed concerns
        pass

    def update_profile(self, user_id, data):
        # ... another 50 lines
        pass

    def delete_user(self, user_id):
        # ... another 50 lines
        pass

    def reset_password(self, email):
        # ... another 50 lines
        pass

    def generate_welcome_email(self, user_data):
        # ... email template logic
        pass

    # ... 10 more methods mixing all concerns
