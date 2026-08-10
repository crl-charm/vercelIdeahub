import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

app = create_app()
with app.app_context():
    client = app.test_client()
    login_resp = client.post('/api/login', json={'username': 'admin', 'password': 'Admin123321!@#$'})
    print('login', login_resp.status_code, login_resp.get_json())
    profile_resp = client.get('/profile')
    print('profile', profile_resp.status_code)
    exp_resp = client.post('/admin/expenses/api/expenses', json={'category': 'utilities', 'description': 'Validation expense', 'amount': 1.23, 'expense_date': '2026-08-11'})
    print('expense', exp_resp.status_code, exp_resp.get_json())
    pay_resp = client.post('/admin/payables/api/payables', json={'creditor_name':'ValCred','items_description':'x','amount_owed':5.5,'due_date':'2026-08-20','incurred_date':'2026-08-11'})
    print('payable', pay_resp.status_code, pay_resp.get_json())
