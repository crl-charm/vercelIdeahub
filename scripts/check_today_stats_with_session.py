import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin_user = User.query.filter_by(role='admin').first()
    if not admin_user:
        print('No admin user found')
        sys.exit(1)

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['account_type'] = 'admin'
            sess['username'] = admin_user.username
            sess['role'] = 'admin'
        resp = client.get('/admin/daily-balance/api/today-stats')
        print('status', resp.status_code)
        try:
            print(resp.get_json())
        except Exception:
            print(resp.get_data(as_text=True))
