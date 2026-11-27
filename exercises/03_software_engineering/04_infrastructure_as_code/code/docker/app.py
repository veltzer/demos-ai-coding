"""Minimal Flask app used as the payload for the Docker/IaC exercise."""

import os
from typing import TYPE_CHECKING

from flask import Flask, jsonify

if TYPE_CHECKING:
    from flask.wrappers import Response

app = Flask(__name__)

@app.route('/')
def hello() -> Response:
    return jsonify({
        'message': 'Hello from Docker!',
        'environment': os.getenv('ENV', 'development')
    })

@app.route('/health')
def health() -> tuple[Response, int]:
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
