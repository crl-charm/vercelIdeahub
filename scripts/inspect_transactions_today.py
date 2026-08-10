import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.models import Transaction
from datetime import date

app = create_app()
with app.app_context():
    today = date.today()
    from app import db
    from sqlalchemy import func
    rows = Transaction.query.filter(func.date(Transaction.created_at) == today).all()
    print('today', today, 'count', len(rows))
    for tx in rows[:10]:
        print(tx.id, tx.total_bill, tx.payment_method, tx.created_at)
