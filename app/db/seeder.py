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

        # Menu items are now managed through admin interface
        # No hardcoded items seeded on startup

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
