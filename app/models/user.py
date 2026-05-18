from datetime import datetime, timedelta
from app import db
import bcrypt
from flask import current_app


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="staff")
    job_role = db.Column(db.String(50), nullable=False, default="general")  # cashier, cook, general

    # Security fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Set password with validation"""
        self._validate_password_strength(password)
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")
        self.password_changed_at = datetime.utcnow()

    def check_password(self, password):
        """Check password and handle lockout"""
        if self.is_locked():
            return False
        if bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8")):
            self.reset_failed_attempts()
            self.last_login = datetime.utcnow()
            db.session.commit()
            return True
        else:
            self.increment_failed_attempts()
            db.session.commit()
            return False

    def is_locked(self):
        """Check if account is currently locked"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False

    def increment_failed_attempts(self):
        """Increment failed login attempts and lock if necessary"""
        self.failed_login_attempts += 1
        max_attempts = current_app.config.get('MAX_LOGIN_ATTEMPTS', 5)
        if self.failed_login_attempts >= max_attempts:
            lockout_duration = current_app.config.get('LOCKOUT_DURATION', 900)
            self.locked_until = datetime.utcnow() + timedelta(seconds=lockout_duration)

    def reset_failed_attempts(self):
        """Reset failed login attempts on successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None

    def _validate_password_strength(self, password):
        """Validate password meets security requirements"""
        config = current_app.config

        if len(password) < config.get('PASSWORD_MIN_LENGTH', 12):
            raise ValueError(f"Password must be at least {config.get('PASSWORD_MIN_LENGTH', 12)} characters long")

        if config.get('PASSWORD_REQUIRE_UPPERCASE', True) and not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")

        if config.get('PASSWORD_REQUIRE_LOWERCASE', True) and not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")

        if config.get('PASSWORD_REQUIRE_DIGITS', True) and not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")

        if config.get('PASSWORD_REQUIRE_SPECIAL', True) and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            raise ValueError("Password must contain at least one special character")