import os
import sys

# Ensure the project root is in the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.menu_item import MenuItem
from app.models.order_item import OrderItem
from app.models.inventory import InventoryItem, InventoryLog


def cleanup_menu():
    """Delete all menu items and associated order/inventory records from database."""
    app = create_app()
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "(unknown)")
        print(f"Database: {uri}")

        order_item_count = OrderItem.query.count()
        if order_item_count > 0:
            print(f"Deleting {order_item_count} order items (child records)...")
            OrderItem.query.delete()
            db.session.commit()
            print(f"Deleted {order_item_count} order items.")

        log_count = InventoryLog.query.count()
        if log_count > 0:
            print(f"Deleting {log_count} inventory logs...")
            InventoryLog.query.delete()
            db.session.commit()
            print(f"Deleted {log_count} inventory logs.")

        inventory_count = InventoryItem.query.count()
        if inventory_count > 0:
            print(f"Deleting {inventory_count} inventory items...")
            InventoryItem.query.delete()
            db.session.commit()
            print(f"Deleted {inventory_count} inventory items.")

        count = MenuItem.query.count()
        if count == 0:
            print("No menu items to delete. Database is already clean.")
            return

        print(f"Deleting {count} menu items...")
        MenuItem.query.delete()
        db.session.commit()
        print(f"Successfully deleted {count} menu items.")
        print("Add new items via admin: /admin/menu")


if __name__ == "__main__":
    cleanup_menu()
