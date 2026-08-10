import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import Payable, Receivable, Expense, DailySalesReport

app = create_app()
with app.app_context():
    conn = db.session.connection()
    for table, col in [
        ('payables','created_by'),
        ('receivables','created_by'),
        ('expenses','logged_by'),
        ('daily_sales_reports','generated_by'),
        ('soft_balances','generated_by'),
    ]:
        try:
            res = conn.execute(db.text(f"SELECT COUNT(*) FROM {table} WHERE {col}=1")).scalar()
        except Exception as e:
            res = f'ERROR: {e}'
        print(f'{table}.{col} = 1 ->', res)
