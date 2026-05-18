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

        existing_names = {name for (name,) in db.session.query(MenuItem.name).all()}
        seed_items = [
            ("Tapsilog", Decimal("95.00"), "MainDish - Silog"),
            ("Longsilog", Decimal("95.00"), "MainDish - Silog"),
            ("Hotsilog", Decimal("90.00"), "MainDish - Silog"),
            ("Tocilog", Decimal("90.00"), "MainDish - Silog"),
            ("Chicksilog", Decimal("105.00"), "MainDish - Silog"),
            ("Spamsilog", Decimal("95.00"), "MainDish - Silog"),
            ("Cornsilog", Decimal("85.00"), "MainDish - Silog"),
            ("Bangsilog", Decimal("120.00"), "MainDish - Silog"),
            ("Sisig Silog", Decimal("115.00"), "MainDish - Silog"),
            ("Adobo", Decimal("60.00"), "MainDish - Main Meals"),
            ("Fried Chicken", Decimal("110.00"), "MainDish - Main Meals"),
            ("Grilled Liempo", Decimal("130.00"), "MainDish - Main Meals"),
            ("Kare-Kare", Decimal("120.00"), "MainDish - Main Meals"),
            ("Bulalo", Decimal("140.00"), "MainDish - Main Meals"),
            ("Beef Caldereta", Decimal("125.00"), "MainDish - Main Meals"),
            ("Burger", Decimal("50.00"), "MainDish - Modern Meals"),
            ("Chicken Sandwich", Decimal("85.00"), "MainDish - Modern Meals"),
            ("Sisig Bowl", Decimal("140.00"), "MainDish - Modern Meals"),
            ("Chicken Alfredo Bowl", Decimal("130.00"), "MainDish - Modern Meals"),
            ("Pesto Chicken Bowl", Decimal("120.00"), "MainDish - Modern Meals"),
            ("Pancit Canton", Decimal("75.00"), "Snacks - Pancit"),
            ("Pancit Bihon", Decimal("75.00"), "Snacks - Pancit"),
            ("Pancit Malabon", Decimal("95.00"), "Snacks - Pancit"),
            ("Fries", Decimal("35.00"), "Snacks - Fries & Sides"),
            ("Garlic Fries", Decimal("55.00"), "Snacks - Fries & Sides"),
            ("Onion Rings", Decimal("60.00"), "Snacks - Fries & Sides"),
            ("Chicken Nuggets", Decimal("80.00"), "Snacks - Fries & Sides"),
            ("Siomai", Decimal("70.00"), "Snacks - Fries & Sides"),
            ("Kikiam", Decimal("65.00"), "Snacks - Fries & Sides"),
            ("Lumpia Shanghai", Decimal("80.00"), "Snacks - Appetizers"),
            ("Chicharon Bulaklak", Decimal("85.00"), "Snacks - Appetizers"),
            ("Isaw", Decimal("90.00"), "Snacks - Appetizers"),
            ("Takoyaki", Decimal("95.00"), "Snacks - Appetizers"),
            ("Halo-Halo", Decimal("90.00"), "Snacks - Desserts"),
            ("Leche Flan", Decimal("80.00"), "Snacks - Desserts"),
            ("Banana Cue", Decimal("50.00"), "Snacks - Desserts"),
            ("Hot Americano", Decimal("60.00"), "Drinks - Coffee (Hot)"),
            ("Hot Latte", Decimal("80.00"), "Drinks - Coffee (Hot)"),
            ("Hot Mocha", Decimal("95.00"), "Drinks - Coffee (Hot)"),
            ("Hot Chocolate", Decimal("100.00"), "Drinks - Coffee (Hot)"),
            ("Iced Americano", Decimal("65.00"), "Drinks - Coffee (Cold)"),
            ("Iced Latte", Decimal("95.00"), "Drinks - Coffee (Cold)"),
            ("Iced Mocha", Decimal("110.00"), "Drinks - Coffee (Cold)"),
            ("Iced Chocolate", Decimal("110.00"), "Drinks - Coffee (Cold)"),
            ("Pineapple Juice", Decimal("60.00"), "Drinks - Juices"),
            ("Calamansi Juice", Decimal("60.00"), "Drinks - Juices"),
            ("Orange Juice", Decimal("65.00"), "Drinks - Juices"),
            ("Mango Shake", Decimal("90.00"), "Drinks - Juices"),
            ("Banana Milk", Decimal("75.00"), "Drinks - Juices"),
            ("Coke", Decimal("35.00"), "Drinks - Soft Drinks"),
            ("Royal", Decimal("35.00"), "Drinks - Soft Drinks"),
            ("Sprite", Decimal("35.00"), "Drinks - Soft Drinks"),
            ("Juice", Decimal("30.00"), "Drinks - Juices"),
            ("Coffee", Decimal("40.00"), "Drinks - Coffee (Cold)"),
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
            admin.set_password("admin123")
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
