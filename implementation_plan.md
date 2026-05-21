# Implementation Plan - Core Bug Fixes

This plan details the step-by-step engineering instructions to address the three core bugs identified in the IdeaHub POS system.

## User Review Required

> [!IMPORTANT]
> **Database Category Migration**: To clean up the database without losing historical order/analytics records, we will run an idempotent SQL update block inside the database seeder on application startup. This will transparently update all existing menu items with old category suffixes (e.g., `"MainDish - Silog"`, `"Snacks - Desserts"`) to the clean standard categories (`"Main Dish"`, `"Snack"`, `"Beverages"`).

## Open Questions

*No open questions are pending. The scope of changes is strictly bounded to the 3 core bugs requested by the user, and the solutions align with existing patterns in the codebase.*

---

## Proposed Changes

### Database Schema Component

#### [MODIFY] [space_type.py](file:///c:/Users/hi/OneDrive/Desktop/vercelIdeahub/app/models/space_type.py)
Add the missing `qr_token` column to the `SpaceType` SQLAlchemy model. This ensures standard SQLAlchemy mapping works correctly and aligns with the column added dynamically in `migrator.py`.

```python
    capacity = db.Column(db.Integer, nullable=True)  # None = unlimited
    qr_token = db.Column(db.String(50), nullable=True, unique=True)
```

---

### Data Repository Component

#### [MODIFY] [session_repository.py](file:///c:/Users/hi/OneDrive/Desktop/vercelIdeahub/app/repositories/session_repository.py)
Implement the missing `get_all_spaces(self)` method in `SessionRepository` to resolve the `AttributeError` crash on the `/qr/spaces` route.

```python
    def get_all_spaces(self) -> list[SpaceType]:
        return SpaceType.query.all()
```

#### [MODIFY] [analytics_repository.py](file:///c:/Users/hi/OneDrive/Desktop/vercelIdeahub/app/repositories/analytics_repository.py)
Fix the defective self-join query in `top_menu_items`. The new query will join `MenuItem` with `OrderItem` to aggregate real sales quantity (`count`) and total revenue (`total`), ordered by popularity.

```python
    def top_menu_items(self, limit: int = 10) -> list[dict[str, Any]]:
        from app.models import OrderItem
        result = (
            db.session.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label("count"),
                func.sum(OrderItem.quantity * OrderItem.price).label("total"),
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .group_by(MenuItem.id, MenuItem.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "name": row.name,
                "count": int(row.count or 0),
                "total": float(row.total or 0),
            }
            for row in result
        ]
```

---

### Database Seeder Component

#### [MODIFY] [seeder.py](file:///c:/Users/hi/OneDrive/Desktop/vercelIdeahub/app/db/seeder.py)
1. Clean up `seed_items` definitions to use standard categories:
   - Map `"MainDish - ..."` categories to `"Main Dish"`.
   - Map `"Snacks - ..."` categories to `"Snack"`.
   - Map `"Drinks - ..."` categories to `"Beverages"`.
2. Add an idempotent category migration block inside `run()` to update any existing items in the database:
   ```python
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
   ```

---

## Verification Plan

### Automated/Local Testing
- Start the server using: `python app.py` (which runs schema migrations and the seeder update).
- Verify the server starts successfully without errors.
- Test `/qr/spaces` API using a curl command or web browser to verify it returns QR tokens and details without crashing.
- Inspect the menu list on the admin page (`/admin/menu`) to ensure all pre-seeded items are correctly categorized under `Main Dish`, `Snack`, or `Beverages`.
- Attempt editing an existing menu item via the admin panel and confirm it succeeds without validation errors.
- Create a test order and verify the analytics endpoint (`/api/analytics/top-menu-items`) correctly reflects the order in the top items chart.
