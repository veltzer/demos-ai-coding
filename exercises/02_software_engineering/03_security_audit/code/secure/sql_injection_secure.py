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
