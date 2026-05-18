from datetime import datetime, date
from decimal import Decimal
from app import db


class StaffPerformanceLog(db.Model):
    __tablename__ = "staff_performance_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    customers_served = db.Column(db.Integer, nullable=False, default=0)
    admin_note = db.Column(db.Text, nullable=True)
    score = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="performance_logs")

    def calculate_score(self) -> Decimal:
        # Score based on customers served: 1 point per customer
        score = Decimal(str(self.customers_served)) * Decimal("1.0")
        return score.quantize(Decimal("0.01"))
