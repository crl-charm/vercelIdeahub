import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.models import Payable, Receivable, Expense, DailySalesReport, User, Admin
app = create_app()
with app.app_context():
    print('Sample Payables (id, created_by):')
    for r in Payable.query.order_by(Payable.id.desc()).limit(10).all():
        print(r.id, r.created_by if hasattr(r, 'created_by') else None)
    print('\nSample Receivables (id, created_by):')
    for r in Receivable.query.order_by(Receivable.id.desc()).limit(10).all():
        print(r.id, r.created_by if hasattr(r, 'created_by') else None)
    print('\nSample Expenses (id, logged_by_user):')
    for r in Expense.query.order_by(Expense.id.desc()).limit(10).all():
        print(r.id, r.logged_by if hasattr(r, 'logged_by') else None)
    print('\nSample Daily Sales Reports (id, generated_by):')
    for r in DailySalesReport.query.order_by(DailySalesReport.id.desc()).limit(10).all():
        print(r.id, r.generated_by if hasattr(r, 'generated_by') else None)
    print('\nUsers (id, username, is_active):')
    for u in User.query.order_by(User.id).all():
        print(u.id, u.username, u.is_active)
    print('\nAdmins (id, username):')
    for a in Admin.query.order_by(Admin.id).all():
        print(a.id, a.username)
