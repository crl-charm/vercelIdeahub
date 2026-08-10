import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.admin import Admin
from app.models.user import User


def recreate_admin(username: str, password: str, create_shadow: bool = True) -> None:
    app = create_app()
    with app.app_context():
        existing_admins = Admin.query.filter_by(username=username).all()
        existing_users = User.query.filter_by(username=username).all()

        for admin in existing_admins:
            db.session.delete(admin)
        for user in existing_users:
            db.session.delete(user)

        if existing_admins or existing_users:
            db.session.commit()
            print(f"Deleted {len(existing_admins)} old admin(s) and {len(existing_users)} old user(s).")

        new_admin = Admin(full_name="System Admin", username=username)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Created new admin account '{username}' with the provided password.")

        if create_shadow:
            shadow_user = User(
                full_name=new_admin.full_name,
                username=new_admin.username,
                role="admin",
                job_role="admin",
                is_active=False,
            )
            shadow_user.password = new_admin.password
            shadow_user.failed_login_attempts = new_admin.failed_login_attempts
            shadow_user.locked_until = new_admin.locked_until
            shadow_user.last_login = new_admin.last_login
            shadow_user.password_changed_at = new_admin.password_changed_at
            shadow_user.created_at = new_admin.created_at
            db.session.add(shadow_user)
            db.session.commit()
            print("Created matching shadow User row for admin login mapping.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recreate the admin account and optional shadow user.")
    parser.add_argument("--username", default="admin", help="Admin username to recreate")
    parser.add_argument(
        "--password",
        default="Admin123321!@#$",
        help="New admin password",
    )
    parser.add_argument(
        "--no-shadow",
        action="store_true",
        help="Do not create a matching shadow User row",
    )
    args = parser.parse_args()

    recreate_admin(args.username, args.password, create_shadow=not args.no_shadow)
