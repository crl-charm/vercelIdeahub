import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import Admin, User

app = create_app()
with app.app_context():
    print('=== Admin rows ===')
    admins = Admin.query.order_by(Admin.id).all()
    for a in admins:
        print(f'Admin id={a.id} username={a.username}')

    print('\n=== User rows for username "admin" ===')
    admin_users = User.query.filter_by(username='admin').all()
    for u in admin_users:
        print(f'User id={u.id} username={u.username} is_active={u.is_active}')

    print('\n=== Counts ===')
    total_admins = Admin.query.count()
    total_users = User.query.count()
    print(f'total_admins={total_admins} total_users={total_users}')

    # Check FK-dependent tables for orphaned or null references
    conn = db.session.connection()
    def run_sql(q):
        res = conn.execute(db.text(q)).fetchall()
        return res

    print('\n=== Orphaned FK checks ===')
    checks = {
        'daily_sales_reports (generated_by NULL or missing user)': "SELECT id, generated_by FROM daily_sales_reports WHERE generated_by IS NULL OR generated_by NOT IN (SELECT id FROM users)",
        'expenses (logged_by_user broken)': "SELECT id, logged_by FROM expenses WHERE logged_by IS NULL OR logged_by NOT IN (SELECT id FROM users)",
        'payables (created_by broken)': "SELECT id, created_by FROM payables WHERE created_by IS NULL OR created_by NOT IN (SELECT id FROM users)",
        'receivables (created_by broken)': "SELECT id, created_by FROM receivables WHERE created_by IS NULL OR created_by NOT IN (SELECT id FROM users)",
        'soft_balances (generated_by broken)': "SELECT id, generated_by FROM soft_balances WHERE generated_by IS NULL OR generated_by NOT IN (SELECT id FROM users)",
    }

    for label, q in checks.items():
        rows = run_sql(q)
        print(f'\n{label}: {len(rows)} rows')
        for r in rows[:10]:
            print(r)

    print('\n=== Sample daily_sales_reports rows count total ===')
    total_ds = run_sql('SELECT COUNT(*) FROM daily_sales_reports')[0][0]
    print('daily_sales_reports total rows =', total_ds)

    print('\nDiagnostic complete.')
