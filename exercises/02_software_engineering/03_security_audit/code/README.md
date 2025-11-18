# Security Audit & Hardening - Code Files

This directory contains vulnerable code examples and their secure implementations.

## Directory Structure

```txt
code/
+-- vulnerable/      # Insecure code (for learning only!)
|   +-- sql_injection.py        # SQL injection vulnerability
|   +-- xss.py                  # Cross-site scripting
|   +-- broken_auth.py          # Weak authentication
+-- secure/          # Secure implementations
|   +-- sql_injection_secure.py # Parameterized queries
|   +-- xss_secure.py           # Input sanitization
|   +-- auth_secure.py          # Secure authentication
+-- tests/           # Security tests
    +-- test_security.py        # Automated security checks
```

## WARNING

**NEVER use code from the `vulnerable/` directory in production!**

These examples are for educational purposes only to understand security vulnerabilities.

## How to Use

1. **Study vulnerable code** - Understand the vulnerability
1. **Learn the exploit** - See how it can be attacked
1. **Review secure code** - Learn the fix
1. **Run security tests** - Verify security measures

## Running Security Tests

```bash
# Install security tools
pip install bandit safety pytest

# Run security scanner
bandit -r .

# Run security tests
pytest tests/test_security.py

# Check dependencies
safety check
```

See the main `exercise.md` file for OWASP Top 10 and security best practices.
