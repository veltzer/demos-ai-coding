# DANGEROUS - DO NOT USE
"""Intentionally SQL-injectable Flask app. Audit target - do not deploy."""

import sqlite3
from flask import Flask, request

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
