import os
import sys

# Ensure the project root is in the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.admin import Admin

def reset_admin():
    app = create_app()
    with app.app_context():
        admin = Admin.query.filter_by(username="admin").first()
        if admin:
            print("Found existing 'admin' admin account. Resetting password...")
            admin.set_password("Admin123!@#$")
            admin.failed_login_attempts = 0
            admin.locked_until = None
            db.session.commit()
            active_user_admin = User.query.filter_by(username="admin", is_active=True).first()
            if active_user_admin:
                active_user_admin.is_active = False
                db.session.commit()
            print("Password for admin has been successfully reset to: Admin123!@#$")
        else:
            existing_user_admin = User.query.filter_by(username="admin", is_active=True).first()
            if existing_user_admin:
                print("Migrating existing 'admin' user record to Admin table...")
                admin = Admin(
                    full_name=existing_user_admin.full_name,
                    username=existing_user_admin.username,
                    created_at=existing_user_admin.created_at,
                )
                admin.password = existing_user_admin.password
                admin.failed_login_attempts = existing_user_admin.failed_login_attempts
                admin.locked_until = existing_user_admin.locked_until
                admin.last_login = existing_user_admin.last_login
                admin.password_changed_at = existing_user_admin.password_changed_at
                existing_user_admin.is_active = False
                db.session.add(admin)
                db.session.add(existing_user_admin)
                db.session.commit()
                print("Migrated old admin user record and reset password.")
            else:
                print("'admin' admin account not found. Creating new admin account...")
                admin = Admin(full_name="System Admin", username="admin")
                admin.set_password("Admin123!@#$")
                db.session.add(admin)
                db.session.commit()
                print("Admin account created successfully with password: Admin123!@#$")

if __name__ == "__main__":
    reset_admin()
