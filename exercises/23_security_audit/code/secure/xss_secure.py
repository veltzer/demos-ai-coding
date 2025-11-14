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
