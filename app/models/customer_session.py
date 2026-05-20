from datetime import datetime
from app import db

class CustomerSession(db.Model):
    __tablename__ = "customer_sessions"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=True)
    course = db.Column(db.String(100), nullable=True)
    number_of_people = db.Column(db.Integer, nullable=False, default=1)
    space_type_id = db.Column(db.Integer, db.ForeignKey("space_types.id"), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="active", nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default="cash")
    amount_tendered = db.Column(db.Numeric(10, 2), nullable=True)

    space_type = db.relationship("SpaceType", backref="sessions")