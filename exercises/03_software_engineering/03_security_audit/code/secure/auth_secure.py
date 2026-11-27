"""Hardened counterpart to vulnerable/broken_auth.py: bcrypt, a password policy,
rate limiting, account lockout, two-factor codes, session timeout and an audit log."""

import logging
import secrets
import sqlite3
import time
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import bcrypt
import pyotp
from flask import Flask, jsonify, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

if TYPE_CHECKING:
    from flask.wrappers import Response

app = Flask(__name__)

# Generate a strong secret key
app.secret_key = secrets.token_hex(32)

# Setup rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Security audit log
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler('audit.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

# Application errors, as opposed to the audit trail
logger = logging.getLogger(__name__)

# Track failed login attempts
failed_attempts: dict[str, dict[str, float]] = {}  # In production, use Redis

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 900  # 15 minutes
SESSION_MINUTES = 30


class PasswordPolicy:
    """Password complexity requirements."""
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True

    @staticmethod
    def validate(password: str) -> tuple[bool, str]:
        """Validate password against policy."""
        if len(password) < PasswordPolicy.MIN_LENGTH:
            return False, f"Password must be at least {PasswordPolicy.MIN_LENGTH} characters"

        if PasswordPolicy.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        if PasswordPolicy.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        if PasswordPolicy.REQUIRE_DIGIT and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        if PasswordPolicy.REQUIRE_SPECIAL and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"

        return True, ""


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash (constant time)."""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        # bcrypt raises ValueError for a stored hash it cannot parse
        return False


def is_account_locked(username: str) -> bool:
    """Check if account is locked due to failed attempts."""
    if username not in failed_attempts:
        return False

    attempts = failed_attempts[username]
    if attempts['count'] >= MAX_FAILED_ATTEMPTS:
        if time.time() - attempts['last_attempt'] < LOCKOUT_SECONDS:
            return True
        # The lockout is over: unlock the account
        del failed_attempts[username]

    return False


def record_failed_attempt(username: str) -> None:
    """Record a failed login attempt."""
    if username not in failed_attempts:
        failed_attempts[username] = {'count': 0, 'last_attempt': 0}

    failed_attempts[username]['count'] += 1
    failed_attempts[username]['last_attempt'] = time.time()


@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register() -> tuple[Response, int]:
    """Register a new user."""
    data = request.get_json()

    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip()

    # Validate inputs
    if not username or not password or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate password policy
    valid, message = PasswordPolicy.validate(password)
    if not valid:
        return jsonify({'error': message}), 400

    # Hash password
    password_hash = hash_password(password)

    # Generate TOTP secret for 2FA
    totp_secret = pyotp.random_base32()

    conn = sqlite3.connect('app.db')
    try:
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already exists'}), 400

        # Insert user
        cursor.execute(
            """INSERT INTO users (username, password_hash, email, totp_secret, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (username, password_hash, email, totp_secret, datetime.now(UTC).isoformat())
        )
        conn.commit()

        audit_logger.info("User registered: %s from %s", username, request.remote_addr)

        return jsonify({
            'message': 'Registration successful',
            'totp_secret': totp_secret  # Show once for 2FA setup
        }), 201

    except sqlite3.Error:
        logger.exception("Database error during registration")
        return jsonify({'error': 'Registration failed'}), 500

    finally:
        conn.close()


@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Authenticate user with username, password, and TOTP."""
    data = request.get_json()

    username = data.get('username', '').strip()
    password = data.get('password', '')
    totp_code = data.get('totp_code', '')

    # Check if account is locked
    if is_account_locked(username):
        audit_logger.warning(
            "Login attempt on locked account: %s from %s", username, request.remote_addr
        )
        return jsonify({'error': 'Account temporarily locked. Try again later.'}), 403

    conn = sqlite3.connect('app.db')
    try:
        cursor = conn.cursor()

        # Get user (constant time to prevent username enumeration)
        cursor.execute(
            "SELECT id, password_hash, totp_secret, is_active FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        # Always verify password even if user doesn't exist (timing attack prevention)
        if user is None:
            # Perform dummy hash verification
            verify_password(password, hash_password("dummy"))
            record_failed_attempt(username)
            audit_logger.warning(
                "Failed login attempt for non-existent user: %s from %s", username, request.remote_addr
            )
            return jsonify({'error': 'Invalid credentials'}), 401

        user_id, password_hash, totp_secret, is_active = user

        # Check if account is active
        if not is_active:
            audit_logger.warning(
                "Login attempt on inactive account: %s from %s", username, request.remote_addr
            )
            return jsonify({'error': 'Account is inactive'}), 403

        # Verify password
        if not verify_password(password, password_hash):
            record_failed_attempt(username)
            audit_logger.warning(
                "Failed login attempt (wrong password): %s from %s", username, request.remote_addr
            )
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify TOTP
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(totp_code, valid_window=1):
            record_failed_attempt(username)
            audit_logger.warning(
                "Failed login attempt (wrong TOTP): %s from %s", username, request.remote_addr
            )
            return jsonify({'error': 'Invalid 2FA code'}), 401

        # Successful login - drop whatever the session held before it
        # (prevent session fixation). Flask's cookie session has no ID to
        # regenerate; with a server-side store (Flask-Session), issue a new one.
        session.clear()

        # Set session data
        session['user_id'] = user_id
        session['username'] = username
        session['login_time'] = datetime.now(UTC).isoformat()

        # Clear failed attempts
        failed_attempts.pop(username, None)

        audit_logger.info(
            "Successful login: %s from %s", username, request.remote_addr
        )

        return jsonify({'message': 'Login successful'}), 200

    except sqlite3.Error:
        logger.exception("Database error during login")
        return jsonify({'error': 'Login failed'}), 500

    finally:
        conn.close()


@app.route('/logout', methods=['POST'])
def logout() -> tuple[Response, int]:
    """Logout user and invalidate session."""
    username = session.get('username', 'unknown')
    session.clear()

    audit_logger.info(
        "User logged out: %s from %s", username, request.remote_addr
    )

    return jsonify({'message': 'Logged out successfully'}), 200


@app.before_request
def check_session_timeout() -> tuple[Response, int] | None:
    """Check for session timeout (30 minutes)."""
    if 'login_time' in session:
        login_time = datetime.fromisoformat(session['login_time'])
        if datetime.now(UTC) - login_time > timedelta(minutes=SESSION_MINUTES):
            session.clear()
            return jsonify({'error': 'Session expired'}), 401
    return None
