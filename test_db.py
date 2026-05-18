import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    app = create_app()
    print("App created successfully")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    with app.app_context():
        print("App context entered")
        from app import db

        # Try to describe the users table
        result = db.session.execute(db.text("DESCRIBE users"))
        columns = [row[0] for row in result.fetchall()]
        print(f"User table columns: {columns}")

        # Check for admin user
        result = db.session.execute(db.text("SELECT id, username, failed_login_attempts, locked_until FROM users WHERE username = 'admin'"))
        user_row = result.fetchone()
        if user_row:
            print(f"Admin user found: {user_row}")
        else:
            print("No admin user found")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()