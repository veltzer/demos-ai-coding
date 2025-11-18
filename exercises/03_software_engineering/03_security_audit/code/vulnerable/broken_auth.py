# DANGEROUS - Multiple authentication issues
import hashlib
from flask import Flask, request, session
import sqlite3

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
