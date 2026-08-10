import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import MenuItem, MenuItemIngredient
from app.models.inventory import InventoryItem

app = create_app()
with app.app_context():
    print("--- MENU ITEMS ---")
    menu_items = MenuItem.query.all()
    for item in menu_items:
        print(f"ID: {item.id} | Name: {item.name} | Price: {item.price} | Category: {repr(item.category)} | Available: {item.is_available} | Status: {item.status}")

    print("\n--- RECIPE MAPPINGS ---")
    mappings = MenuItemIngredient.query.all()
    for m in mappings:
        print(f"ID: {m.id} | MenuItemID: {m.menu_item_id} | IngredientItemID: {m.ingredient_item_id} | ReqQty: {m.quantity_required} | Unit: {m.unit} | Ratio: {m.conversion_ratio}")

    print("\n--- INVENTORY ITEMS ---")
    invs = InventoryItem.query.all()
    for i in invs:
        print(f"ID: {i.id} | MenuItemID: {i.menu_item_id} | StockQty: {i.stock_qty} | Unit: {i.unit} | Threshold: {i.low_stock_threshold}")
