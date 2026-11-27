# tests/test_security.py
#
# Security test suite for the audit exercise. It tests the hardened `app.py`
# the learner writes in the code/ directory, and is run from there; until that
# file exists the suite cannot be collected.
# Several tests are intentionally left as stubs for the reader to complete.

import importlib

# The learner's `app` module is not part of the exercise skeleton, so it is
# imported dynamically: the type checker cannot be asked to resolve it.
app = importlib.import_module("app").app


class TestSecurityHeaders:
    """Test security headers are present."""

    def test_csp_header(self) -> None:
        """Test Content-Security-Policy header."""
        with app.test_client() as client:
            response = client.get('/')
            assert 'Content-Security-Policy' in response.headers

    def test_xss_protection_header(self) -> None:
        """Test X-XSS-Protection header."""
        with app.test_client() as client:
            response = client.get('/')
            assert response.headers.get('X-XSS-Protection') == '1; mode=block'

    def test_clickjacking_protection(self) -> None:
        """Test X-Frame-Options header."""
        with app.test_client() as client:
            response = client.get('/')
            assert response.headers.get('X-Frame-Options') == 'DENY'

class TestInputValidation:
    """Test input validation."""

    def test_sql_injection_prevention(self) -> None:
        """Test SQL injection is prevented."""
        with app.test_client() as client:
            # Try SQL injection
            response = client.get('/user?id=1 OR 1=1')
            assert response.status_code == 400

    def test_xss_prevention(self) -> None:
        """Test XSS is prevented."""
        with app.test_client() as client:
            response = client.get('/search?query=<script>alert(1)</script>')
            # Check that script is escaped
            assert b'<script>' not in response.data

class TestAuthentication:
    """Test authentication security."""

    def test_rate_limiting(self) -> None:
        """Test login rate limiting."""
        with app.test_client() as client:
            # Try multiple failed logins
            for _ in range(15):
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

    def test_session_timeout(self) -> None:
        """Test session expires after timeout."""
        # Test implementation
