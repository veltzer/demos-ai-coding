# user_manager.py - A 500-line god class
#
# This is the "before" half of a refactoring exercise: a god class the reader
# is asked to split into focused collaborators. It is an excerpt, not a
# runnable module, so the six services it constructs are never imported. The
# class doing too much is the lesson, not a defect to fix here.
# ruff: noqa: F821
# pylint: disable=undefined-variable,missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-instance-attributes,too-few-public-methods


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
        if '@' not in data['email']:
            raise ValueError("Invalid email")

        # Check if user exists
        existing = self.db.query("SELECT * FROM users WHERE email = ?", data['email'])
        if existing:
            raise ValueError("User exists")

        # Hash password
        # Buried mid-method rather than at the top - another smell to spot.
        import hashlib  # pylint: disable=import-outside-toplevel
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
        # Assigned and then dropped on the floor - one of the smells the
        # reader is meant to spot, so it is kept rather than cleaned up.
        session_id = self.session_store.create(user_id)  # noqa: F841  # pylint: disable=unused-variable

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
