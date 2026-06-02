from app import db

class SpaceType(db.Model):
    __tablename__ = "space_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    rate_per_minute = db.Column(db.Numeric(10,4))
    description = db.Column(db.String(255), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)  # None = unlimited