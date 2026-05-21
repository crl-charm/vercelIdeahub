import os
import sys

# Ensure the project root is in the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User

def reset_admin():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(username="admin").first()
        if admin:
            print("Found existing 'admin' user. Resetting password...")
            admin.set_password("Admin123!@#$")
            # Clear lockout fields if any
            admin.failed_login_attempts = 0
            admin.locked_until = None
            db.session.commit()
            print("Password for 'admin' has been successfully reset to: Admin123!@#$")
        else:
            print("'admin' user not found. Creating new 'admin' user...")
            admin = User(
                full_name="System Admin",
                username="admin",
                role="admin",
                job_role="admin"
            )
            admin.set_password("Admin123!@#$")
            db.session.add(admin)
            db.session.commit()
            print("User 'admin' created successfully with password: Admin123!@#$")

if __name__ == "__main__":
    reset_admin()
