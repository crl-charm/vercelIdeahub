import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models.admin import Admin
from app.models.user import User

# Values extracted from database/ideahub_pos.sql (admins INSERT)
OLD_ADMIN = {
    'id': 1,
    'full_name': 'Admin',
    'username': 'admin',
    'created_at': '2026-04-28 11:41:20',
    'password': '$2b$12$h/6nkTgbAYZKGsbQLfe2tOp0C0bytAt19HYrkxkCEC1dU350oNDEW',
    'failed_login_attempts': 0,
    'locked_until': None,
    'last_login': '2026-08-10 13:23:43',
    'password_changed_at': '2026-05-21 14:06:50'
}


def apply_old_admin():
    app = create_app()
    with app.app_context():
        admin = Admin.query.filter_by(username=OLD_ADMIN['username']).first()
        if not admin:
            print('No admin row found; creating new Admin with id if possible.')
            admin = Admin(
                full_name=OLD_ADMIN['full_name'],
                username=OLD_ADMIN['username']
            )
            admin.password = OLD_ADMIN['password']
            admin.failed_login_attempts = OLD_ADMIN['failed_login_attempts']
            admin.locked_until = OLD_ADMIN['locked_until']
            admin.last_login = OLD_ADMIN['last_login']
            admin.password_changed_at = OLD_ADMIN['password_changed_at']
            db.session.add(admin)
            db.session.commit()
            print(f'Created Admin id={admin.id}')
        else:
            print(f'Updating existing Admin id={admin.id}')
            admin.full_name = OLD_ADMIN['full_name']
            admin.password = OLD_ADMIN['password']
            admin.failed_login_attempts = OLD_ADMIN['failed_login_attempts']
            admin.locked_until = OLD_ADMIN['locked_until']
            admin.last_login = OLD_ADMIN['last_login']
            admin.password_changed_at = OLD_ADMIN['password_changed_at']
            # created_at is often auto-managed; set via raw SQL if necessary
            db.session.add(admin)
            db.session.commit()
            print('Admin updated.')

        # Update or create shadow user
        user = User.query.filter_by(username=OLD_ADMIN['username']).first()
        if user:
            print(f'Updating shadow User id={user.id}')
            user.full_name = OLD_ADMIN['full_name']
            user.password = OLD_ADMIN['password']
            user.role = 'admin'
            user.job_role = 'admin'
            user.is_active = False
            db.session.add(user)
            db.session.commit()
            print('Shadow user updated.')
        else:
            print('Creating shadow User for admin')
            user = User(
                full_name=OLD_ADMIN['full_name'],
                username=OLD_ADMIN['username'],
                role='admin',
                job_role='admin',
                is_active=False
            )
            user.password = OLD_ADMIN['password']
            db.session.add(user)
            db.session.commit()
            print(f'Created shadow User id={user.id}')

if __name__ == '__main__':
    apply_old_admin()
