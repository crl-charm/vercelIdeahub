from app import db
from sqlalchemy import text

def add_security_fields():
    """Add security fields to users table"""
    try:
        # Add new columns for security features
        db.session.execute(text("""
            ALTER TABLE users
            ADD COLUMN failed_login_attempts INT DEFAULT 0,
            ADD COLUMN locked_until DATETIME NULL,
            ADD COLUMN last_login DATETIME NULL,
            ADD COLUMN password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        """))
        db.session.commit()
        print("Security fields added successfully")
    except Exception as e:
        print(f"Error adding security fields: {e}")
        db.session.rollback()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        add_security_fields()