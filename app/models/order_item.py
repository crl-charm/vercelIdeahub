from app import db

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id", ondelete="SET NULL"), nullable=True)

    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10,2))
    status = db.Column(db.String(20), nullable=False, default="preparing")

    order = db.relationship("Order", backref="items")
    menu_item = db.relationship("MenuItem")