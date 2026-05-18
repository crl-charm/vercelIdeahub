from app import db
from datetime import datetime

class SpacePriceHistory(db.Model):
    __tablename__ = "space_price_history"

    id = db.Column(db.Integer, primary_key=True)
    space_type_id = db.Column(db.Integer, db.ForeignKey("space_types.id"), nullable=False)
    old_price = db.Column(db.Numeric(10, 4), nullable=True)  # Previous price, None if first time
    new_price = db.Column(db.Numeric(10, 4), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    space_type = db.relationship("SpaceType")
    changed_by = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "space_type_id": self.space_type_id,
            "space_name": self.space_type.name if self.space_type else "Unknown",
            "old_price": float(self.old_price) if self.old_price else None,
            "new_price": float(self.new_price),
            "changed_at": self.changed_at.isoformat(),
            "changed_by": self.changed_by.full_name if self.changed_by else "System",
        }
