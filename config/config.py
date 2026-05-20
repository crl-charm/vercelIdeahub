import os
import secrets

class Config:
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV != "production"

    # Security: production must set SECRET_KEY; dev uses env or .flask_secret file
    _secret_key = os.environ.get("SECRET_KEY")
    if not _secret_key and FLASK_ENV == "production":
        raise RuntimeError(
            "SECRET_KEY environment variable is required when FLASK_ENV=production"
        )
    if not _secret_key:
        _dev_key_file = os.path.join(os.path.dirname(__file__), ".flask_secret")
        if os.path.exists(_dev_key_file):
            with open(_dev_key_file, encoding="utf-8") as _f:
                _secret_key = _f.read().strip()
        else:
            _secret_key = secrets.token_hex(32)
            with open(_dev_key_file, "w", encoding="utf-8") as _f:
                _f.write(_secret_key)
    SECRET_KEY = _secret_key

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://root:@localhost/ideahub_pos"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com https://cdn.socket.io; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; img-src 'self' data: https:; connect-src 'self' ws: wss:;",
    }

    # File Upload Settings (Production-Ready)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max total request size
    UPLOAD_MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max per file
    ALLOWED_UPLOAD_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'menu')

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 24 hours

    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"

    # CORS Settings (restrictive)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')

    # Password Policy
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGITS = True
    PASSWORD_REQUIRE_SPECIAL = True

    # Account Lockout
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 900  # 15 minutes

