import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

app = create_app()
with app.test_client() as client:
    # Manually set a session with user_id pointing to Admin.id (1)
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        # intentionally leave out account_type/username to simulate legacy cookie
    resp = client.post('/admin/daily-balance/api/soft-balances', json={'balance_date': '2026-08-11', 'period': 'AM', 'notes': 'test'})
    print('status', resp.status_code)
    try:
        print('json', resp.get_json())
    except Exception:
        print('response text:', resp.get_data(as_text=True))
