from datetime import datetime, date
from decimal import Decimal
from app import db


class Receivable(db.Model):
    __tablename__ = "receivables"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_contact = db.Column(db.String(100), nullable=True)
    items_description = db.Column(db.Text, nullable=False)
    amount_owed = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=False)
    partial_paid = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("customer_sessions.id"), nullable=True)
    approved_by_staff = db.Column(db.String(100), nullable=True)
    paid_at = db.Column(db.DateTime, nullable=True)
    incurred_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_user = db.relationship("User", backref="receivables")
    session = db.relationship("CustomerSession", backref="receivables")
