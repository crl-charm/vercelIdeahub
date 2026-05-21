from __future__ import annotations

from decimal import Decimal

from app.models import MenuItem, SpaceType
from app.models.user import User
from app.models.management import Department
from app.models.finance import FinanceBudget
from app.models.idea import Idea


class DatabaseSeeder:
    """Populates lookup tables with defaults."""

    def __init__(self, db, app) -> None:
        self._db = db
        self._app = app

    def run(self, force: bool = False) -> None:
        db = self._db
        if force:
            MenuItem.query.delete()
            SpaceType.query.delete()
            db.session.commit()

        if SpaceType.query.count() == 0:
            db.session.add_all(
                [
                    SpaceType(name="Regular Lounge", rate_per_minute=Decimal("0.1667")),
                    SpaceType(name="Premium Lounge", rate_per_minute=Decimal("0.3333")),
                    SpaceType(name="Boardroom", rate_per_minute=Decimal("4.1667")),
                ]
            )
            db.session.commit()

        default_caps = {"Regular Lounge": 30, "Premium Lounge": 30}
        for name, cap in default_caps.items():
            space = SpaceType.query.filter_by(name=name).first()
            if space and (space.capacity is None or space.capacity == 0):
                space.capacity = cap
        db.session.commit()

        # Update existing menu items with old categories to standard ones
        category_mappings = {
            "MainDish - Silog": "Main Dish",
            "MainDish - Main Meals": "Main Dish",
            "MainDish - Modern Meals": "Main Dish",
            "Snacks - Pancit": "Snack",
            "Snacks - Fries & Sides": "Snack",
            "Snacks - Appetizers": "Snack",
            "Snacks - Desserts": "Snack",
            "Drinks - Coffee (Hot)": "Beverages",
            "Drinks - Coffee (Cold)": "Beverages",
            "Drinks - Juices": "Beverages",
            "Drinks - Soft Drinks": "Beverages",
        }
        for old_cat, new_cat in category_mappings.items():
            db.session.query(MenuItem).filter_by(category=old_cat).update({"category": new_cat})
        db.session.commit()

        existing_names = {name for (name,) in db.session.query(MenuItem.name).all()}
        seed_items = [
            ("Tapsilog", Decimal("95.00"), "Main Dish"),
            ("Longsilog", Decimal("95.00"), "Main Dish"),
            ("Hotsilog", Decimal("90.00"), "Main Dish"),
            ("Tocilog", Decimal("90.00"), "Main Dish"),
            ("Chicksilog", Decimal("105.00"), "Main Dish"),
            ("Spamsilog", Decimal("95.00"), "Main Dish"),
            ("Cornsilog", Decimal("85.00"), "Main Dish"),
            ("Bangsilog", Decimal("120.00"), "Main Dish"),
            ("Sisig Silog", Decimal("115.00"), "Main Dish"),
            ("Adobo", Decimal("60.00"), "Main Dish"),
            ("Fried Chicken", Decimal("110.00"), "Main Dish"),
            ("Grilled Liempo", Decimal("130.00"), "Main Dish"),
            ("Kare-Kare", Decimal("120.00"), "Main Dish"),
            ("Bulalo", Decimal("140.00"), "Main Dish"),
            ("Beef Caldereta", Decimal("125.00"), "Main Dish"),
            ("Burger", Decimal("50.00"), "Main Dish"),
            ("Chicken Sandwich", Decimal("85.00"), "Main Dish"),
            ("Sisig Bowl", Decimal("140.00"), "Main Dish"),
            ("Chicken Alfredo Bowl", Decimal("130.00"), "Main Dish"),
            ("Pesto Chicken Bowl", Decimal("120.00"), "Main Dish"),
            ("Pancit Canton", Decimal("75.00"), "Snack"),
            ("Pancit Bihon", Decimal("75.00"), "Snack"),
            ("Pancit Malabon", Decimal("95.00"), "Snack"),
            ("Fries", Decimal("35.00"), "Snack"),
            ("Garlic Fries", Decimal("55.00"), "Snack"),
            ("Onion Rings", Decimal("60.00"), "Snack"),
            ("Chicken Nuggets", Decimal("80.00"), "Snack"),
            ("Siomai", Decimal("70.00"), "Snack"),
            ("Kikiam", Decimal("65.00"), "Snack"),
            ("Lumpia Shanghai", Decimal("80.00"), "Snack"),
            ("Chicharon Bulaklak", Decimal("85.00"), "Snack"),
            ("Isaw", Decimal("90.00"), "Snack"),
            ("Takoyaki", Decimal("95.00"), "Snack"),
            ("Halo-Halo", Decimal("90.00"), "Snack"),
            ("Leche Flan", Decimal("80.00"), "Snack"),
            ("Banana Cue", Decimal("50.00"), "Snack"),
            ("Hot Americano", Decimal("60.00"), "Beverages"),
            ("Hot Latte", Decimal("80.00"), "Beverages"),
            ("Hot Mocha", Decimal("95.00"), "Beverages"),
            ("Hot Chocolate", Decimal("100.00"), "Beverages"),
            ("Iced Americano", Decimal("65.00"), "Beverages"),
            ("Iced Latte", Decimal("95.00"), "Beverages"),
            ("Iced Mocha", Decimal("110.00"), "Beverages"),
            ("Iced Chocolate", Decimal("110.00"), "Beverages"),
            ("Pineapple Juice", Decimal("60.00"), "Beverages"),
            ("Calamansi Juice", Decimal("60.00"), "Beverages"),
            ("Orange Juice", Decimal("65.00"), "Beverages"),
            ("Mango Shake", Decimal("90.00"), "Beverages"),
            ("Banana Milk", Decimal("75.00"), "Beverages"),
            ("Coke", Decimal("35.00"), "Beverages"),
            ("Royal", Decimal("35.00"), "Beverages"),
            ("Sprite", Decimal("35.00"), "Beverages"),
            ("Juice", Decimal("30.00"), "Beverages"),
            ("Coffee", Decimal("40.00"), "Beverages"),
        ]
        to_add = []
        for name, price, category in seed_items:
            if name in existing_names:
                continue
            to_add.append(MenuItem(name=name, price=price, category=category))
        if to_add:
            db.session.add_all(to_add)
        db.session.commit()

        if not User.query.filter_by(username="admin").first():
            admin = User(full_name="System Admin", username="admin", role="admin", job_role="admin")
            admin.set_password("Admin123!@#$")
            db.session.add(admin)
            db.session.commit()

        for dept_name in ("Operations", "Finance", "Technology"):
            if not Department.query.filter_by(_name=dept_name).first():
                db.session.add(Department(_name=dept_name))
        db.session.commit()

        if FinanceBudget.query.count() == 0:
            db.session.add(FinanceBudget(_name="Main Budget", _total_budget=Decimal("0.00"), _allocated=Decimal("0.00")))
            db.session.commit()

        if Idea.query.count() == 0:
            owner = User.query.filter_by(username="admin").first()
            departments = Department.query.order_by(Department.id.asc()).all()
            sample = [
                ("Queue Improvement", "Improve checkout queue handoff.", "pending"),
                ("Self-order Kiosk", "Add guided ordering tablets.", "approved"),
                ("Supplier Alerts", "Email alert for low stock.", "pending"),
                ("Expense Auto-tagging", "Auto-categorize finance entries.", "rejected"),
                ("Loyalty Program", "Points for returning lounge users.", "approved"),
            ]
            for idx, (title, desc, status) in enumerate(sample):
                dept = departments[idx % len(departments)] if departments else None
                db.session.add(
                    Idea(
                        _title=title,
                        _description=desc,
                        _status=status,
                        _user_id=owner.id,
                        _department_id=dept.id if dept else None,
                    )
                )
            db.session.commit()
