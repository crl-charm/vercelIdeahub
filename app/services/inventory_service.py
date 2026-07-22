from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from sqlalchemy import func

from app.repositories.inventory_repository import InventoryRepository

DEFAULT_LOW_STOCK_THRESHOLD = 10
DEFAULT_UNIT = "pieces"


@dataclass(frozen=True)
class InventoryService:
    repo: InventoryRepository

    @staticmethod
    def compute_stock_status(stock_qty: int, threshold: int) -> dict[str, bool]:
        is_out_of_stock = stock_qty == 0
        if threshold <= 0:
            return {
                "is_low": is_out_of_stock,
                "is_warning": False,
                "is_out_of_stock": is_out_of_stock,
            }
        is_low = stock_qty < threshold
        stock_ratio = stock_qty / threshold
        is_warning = not is_low and stock_ratio < 1.5
        return {
            "is_low": is_low,
            "is_warning": is_warning,
            "is_out_of_stock": is_out_of_stock,
        }

    @staticmethod
    def snapshot_from_row(
        menu_item_id: int, inv: Any | None
    ) -> dict[str, Any]:
        if inv is not None:
            return {
                "menu_item_id": menu_item_id,
                "inventory_item_id": inv.id,
                "stock_qty": inv.stock_qty,
                "low_stock_threshold": inv.low_stock_threshold,
                "unit": inv.unit,
                "persisted": True,
            }
        return {
            "menu_item_id": menu_item_id,
            "inventory_item_id": None,
            "stock_qty": 0,
            "low_stock_threshold": DEFAULT_LOW_STOCK_THRESHOLD,
            "unit": DEFAULT_UNIT,
            "persisted": False,
        }

    def resolve_inventory_snapshot(
        self, menu_item_id: int, inventory_map: dict[int, Any] | None = None
    ) -> dict[str, Any]:
        if inventory_map is not None:
            return self.snapshot_from_row(menu_item_id, inventory_map.get(menu_item_id))
        inv = self.repo.get_by_menu_item_id(menu_item_id)
        return self.snapshot_from_row(menu_item_id, inv)

    def ensure_inventory_row(
        self,
        menu_item_id: int,
        stock_qty: int = 0,
        low_stock_threshold: int = DEFAULT_LOW_STOCK_THRESHOLD,
        unit: str = DEFAULT_UNIT,
    ) -> Any:
        existing = self.repo.get_by_menu_item_id(menu_item_id)
        if existing:
            return existing
        item = self.repo.create(menu_item_id, stock_qty, low_stock_threshold, unit)
        self.repo.save()
        return item

    def _build_inventory_map(self, menu_item_ids: list[int]) -> dict[int, Any]:
        return self.repo.list_by_menu_item_ids(menu_item_ids)

    def build_direct_stock_items(self) -> list[dict[str, Any]]:
        from app.models.menu_item import MenuItem, MenuItemIngredient

        ingredients = MenuItem.query.filter(
            MenuItem.category == "ingredient",
            MenuItem.status != "deleted",
        ).all()
        if not ingredients:
            return []

        ingredient_ids = [i.id for i in ingredients]
        inventory_map = self._build_inventory_map(ingredient_ids)

        recipe_counts = dict(
            MenuItemIngredient.query.with_entities(
                MenuItemIngredient.ingredient_item_id,
                func.count(MenuItemIngredient.id),
            )
            .filter(MenuItemIngredient.ingredient_item_id.in_(ingredient_ids))
            .group_by(MenuItemIngredient.ingredient_item_id)
            .all()
        )

        mappings = MenuItemIngredient.query.filter(
            MenuItemIngredient.ingredient_item_id.in_(ingredient_ids)
        ).all()
        meals_by_ingredient: dict[int, list[str]] = {iid: [] for iid in ingredient_ids}
        for m in mappings:
            if m.menu_item and m.menu_item.name:
                meals_by_ingredient.setdefault(m.ingredient_item_id, []).append(
                    m.menu_item.name
                )

        results: list[dict[str, Any]] = []
        for ing in ingredients:
            snap = self.resolve_inventory_snapshot(ing.id, inventory_map)
            status = self.compute_stock_status(
                snap["stock_qty"], snap["low_stock_threshold"]
            )
            count = recipe_counts.get(ing.id, 0)
            results.append(
                {
                    "id": ing.id,
                    "menu_item_id": ing.id,
                    "name": ing.name,
                    "inventory_item_id": snap["inventory_item_id"],
                    "stock_qty": snap["stock_qty"],
                    "unit": snap["unit"],
                    "low_stock_threshold": snap["low_stock_threshold"],
                    "persisted": snap["persisted"],
                    "recipe_count": count,
                    "is_linked": count > 0,
                    "linked_meal_names": meals_by_ingredient.get(ing.id, []),
                    **status,
                }
            )
        return results

    def build_recipe_inventory_items(self) -> list[dict[str, Any]]:
        from app.models.menu_item import MenuItem, MenuItemIngredient

        meals = MenuItem.query.filter(
            MenuItem.category != "ingredient",
            MenuItem.status != "deleted",
        ).all()
        if not meals:
            return []

        meal_ids = [m.id for m in meals]
        all_mappings = MenuItemIngredient.query.filter(
            MenuItemIngredient.menu_item_id.in_(meal_ids)
        ).all()
        mappings_by_meal: dict[int, list[Any]] = {mid: [] for mid in meal_ids}
        ingredient_ids: set[int] = set()
        for m in all_mappings:
            mappings_by_meal.setdefault(m.menu_item_id, []).append(m)
            ingredient_ids.add(m.ingredient_item_id)

        direct_meal_ids = [
            m.id
            for m in meals
            if not mappings_by_meal.get(m.id)
        ]
        inventory_map = self._build_inventory_map(
            list(ingredient_ids) + direct_meal_ids
        )

        data: list[dict[str, Any]] = []
        for meal in meals:
            ingredients = mappings_by_meal.get(meal.id, [])
            has_recipe = len(ingredients) > 0

            meal_data: dict[str, Any] = {
                "id": meal.id,
                "name": meal.name,
                "category": meal.category,
                "has_recipe": has_recipe,
                "is_low": False,
                "is_warning": False,
                "capacity": 0,
            }

            if has_recipe:
                caps: list[int] = []
                for m in ingredients:
                    snap = self.resolve_inventory_snapshot(
                        m.ingredient_item_id, inventory_map
                    )
                    ing_status = self.compute_stock_status(
                        snap["stock_qty"], snap["low_stock_threshold"]
                    )
                    if ing_status["is_low"]:
                        meal_data["is_low"] = True
                    elif ing_status["is_warning"]:
                        meal_data["is_warning"] = True

                    qty_req = float(m.quantity_required)
                    if qty_req > 0:
                        caps.append(int(snap["stock_qty"] / qty_req))
                    else:
                        caps.append(0)

                meal_data["capacity"] = min(caps) if caps else 0
            else:
                snap = self.resolve_inventory_snapshot(meal.id, inventory_map)
                status = self.compute_stock_status(
                    snap["stock_qty"], snap["low_stock_threshold"]
                )
                meal_data["is_low"] = status["is_low"]
                meal_data["is_warning"] = status["is_warning"]
                meal_data["inventory_item_id"] = snap["inventory_item_id"]
                meal_data["stock_qty"] = snap["stock_qty"]
                meal_data["unit"] = snap["unit"]
                meal_data["low_stock_threshold"] = snap["low_stock_threshold"]
                meal_data["persisted"] = snap["persisted"]
                meal_data["capacity"] = snap["stock_qty"]

            data.append(meal_data)

        return data

    def build_recipe_detail(self, menu_item_id: int) -> list[dict[str, Any]]:
        from app.models.menu_item import MenuItemIngredient

        mappings = MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()
        if not mappings:
            return []

        ingredient_ids = [m.ingredient_item_id for m in mappings]
        inventory_map = self._build_inventory_map(ingredient_ids)

        data: list[dict[str, Any]] = []
        for m in mappings:
            snap = self.resolve_inventory_snapshot(m.ingredient_item_id, inventory_map)
            data.append(
                {
                    "id": m.id,
                    "menu_item_id": m.menu_item_id,
                    "ingredient_item_id": m.ingredient_item_id,
                    "ingredient_name": m.ingredient.name if m.ingredient else "Unknown",
                    "quantity_required": float(m.quantity_required),
                    "stock_qty": snap["stock_qty"],
                    "unit": snap["unit"],
                    "inventory_item_id": snap["inventory_item_id"],
                    "persisted": snap["persisted"],
                }
            )
        return data

    def list_ingredients_for_picker(
        self, query: str | None = None
    ) -> list[dict[str, Any]]:
        from app.models.menu_item import MenuItem, MenuItemIngredient

        q = MenuItem.query.filter_by(category="ingredient")
        if query and query.strip():
            q = q.filter(MenuItem.name.ilike(f"%{query.strip()}%"))
        ingredients = q.order_by(MenuItem.name).all()
        if not ingredients:
            return []

        ingredient_ids = [i.id for i in ingredients]
        inventory_map = self._build_inventory_map(ingredient_ids)
        recipe_counts = dict(
            MenuItemIngredient.query.with_entities(
                MenuItemIngredient.ingredient_item_id,
                func.count(MenuItemIngredient.id),
            )
            .filter(MenuItemIngredient.ingredient_item_id.in_(ingredient_ids))
            .group_by(MenuItemIngredient.ingredient_item_id)
            .all()
        )

        results: list[dict[str, Any]] = []
        for ing in ingredients:
            snap = self.resolve_inventory_snapshot(ing.id, inventory_map)
            results.append(
                {
                    "id": ing.id,
                    "name": ing.name,
                    "recipe_count": recipe_counts.get(ing.id, 0),
                    "stock_qty": snap["stock_qty"],
                    "unit": snap["unit"],
                    "low_stock_threshold": snap["low_stock_threshold"],
                }
            )
        return results

    def list_all(self) -> list[dict[str, Any]]:
        items = self.repo.list_all()
        return [
            {
                "id": item.id,
                "menu_item_id": item.menu_item_id,
                "menu_item_name": item.menu_item.name if item.menu_item else "Unknown",
                "stock_qty": item.stock_qty,
                "low_stock_threshold": item.low_stock_threshold,
                "unit": item.unit,
                "is_low": item.stock_qty < item.low_stock_threshold,
            }
            for item in items
        ]

    def get_item(self, item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        item = self.repo.get_item(item_id)
        if not item:
            return {"error": "Inventory item not found"}, 404
        return {
            "id": item.id,
            "menu_item_id": item.menu_item_id,
            "menu_item_name": item.menu_item.name,
            "stock_qty": item.stock_qty,
            "low_stock_threshold": item.low_stock_threshold,
            "unit": item.unit,
        }

    def create(
        self, menu_item_id: int, stock_qty: int, low_stock_threshold: int, unit: str
    ) -> dict[str, Any]:
        existing = self.repo.get_by_menu_item_id(menu_item_id)
        if existing:
            return {"success": True, "data": {"id": existing.id}}
        item = self.repo.create(menu_item_id, stock_qty, low_stock_threshold, unit)
        self.repo.save()
        return {"success": True, "data": {"id": item.id}}

    def update_stock(
        self,
        item_id: int | None,
        new_qty: int,
        reason: str,
        user_id: Optional[int],
        menu_item_id: int | None = None,
    ) -> dict[str, Any] | tuple[dict[str, Any], int]:
        if item_id:
            item = self.repo.get_item(item_id)
        elif menu_item_id is not None:
            item = self.ensure_inventory_row(menu_item_id)
        else:
            return {"error": "Inventory item not found"}, 404

        if not item:
            return {"error": "Inventory item not found"}, 404

        if new_qty < 0:
            return {"error": "Stock quantity cannot be less than zero"}, 400

        old_qty = item.stock_qty
        change = new_qty - old_qty

        from app.models.user import User

        user = User.query.get(user_id) if user_id else None
        username = user.username if user else "System"

        formatted_reason = f"{username} adjusted {change:+} ({old_qty} → {new_qty}) - {reason}"
        formatted_reason = formatted_reason[:100]

        if change > 0:
            self.repo.add(item.id, change, formatted_reason, user_id)
        elif change < 0:
            self.repo.deduct(item.id, abs(change), formatted_reason, user_id)

        self.repo.save()
        return {"success": True, "data": {"inventory_item_id": item.id}}

    def delete_raw_ingredient(
        self, menu_item_id: int
    ) -> dict[str, Any] | tuple[dict[str, Any], int]:
        from app.models.menu_item import MenuItem, MenuItemIngredient

        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item or menu_item.category != "ingredient":
            return {"error": "Raw ingredient not found"}, 404
        if menu_item.status == "deleted":
            return {"error": "Raw ingredient not found"}, 404

        recipe_count = MenuItemIngredient.query.filter_by(
            ingredient_item_id=menu_item_id
        ).count()
        if recipe_count > 0:
            return {
                "error": (
                    f"Cannot delete: ingredient is used in {recipe_count} "
                    "recipe(s). Remove recipe links first."
                )
            }, 400

        inv = self.repo.get_by_menu_item_id(menu_item_id)
        if inv:
            self.repo.delete(inv.id)

        menu_item.status = "deleted"
        menu_item.is_available = False
        self.repo.save()
        return {"success": True}

    def delete(self, item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        item = self.repo.get_item(item_id)
        if not item:
            return {"error": "Inventory item not found"}, 404
        success = self.repo.delete(item_id)
        if success:
            self.repo.save()
            return {"success": True}
        return {"error": "Failed to delete inventory item"}, 500

    def deduct_on_order(self, menu_item_id: int, qty: int) -> bool:
        from app.models.menu_item import MenuItemIngredient
        from app.core.socketio_handlers import emit_inventory_low_stock

        ingredients = MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()

        if ingredients:
            success = True
            for recipe_component in ingredients:
                total_deduction = int(qty * recipe_component.quantity_required)
                item = self.repo.get_by_menu_item_id(recipe_component.ingredient_item_id)
                if item:
                    deducted = self.repo.deduct(
                        item.id,
                        total_deduction,
                        f"Order deduction for {recipe_component.menu_item.name}",
                        None,
                    )
                    if deducted:
                        if item.stock_qty < item.low_stock_threshold:
                            emit_inventory_low_stock(
                                {
                                    "item_id": item.id,
                                    "menu_item": item.menu_item.name,
                                    "stock_qty": item.stock_qty,
                                    "threshold": item.low_stock_threshold,
                                }
                            )
                    else:
                        success = False
            if success:
                self.repo.save()
            return success
        else:
            item = self.repo.get_by_menu_item_id(menu_item_id)
            if not item:
                return False
            success = self.repo.deduct(item.id, qty, "Order deduction", None)
            if success:
                self.repo.save()
                if item.stock_qty < item.low_stock_threshold:
                    emit_inventory_low_stock(
                        {
                            "item_id": item.id,
                            "menu_item": item.menu_item.name,
                            "stock_qty": item.stock_qty,
                            "threshold": item.low_stock_threshold,
                        }
                    )
            return success

    def get_low_stock(self) -> list[dict[str, Any]]:
        items = self.repo.list_low_stock()
        return [
            {
                "id": item.id,
                "menu_item": item.menu_item.name,
                "stock_qty": item.stock_qty,
                "threshold": item.low_stock_threshold,
            }
            for item in items
        ]

    def get_logs(self, item_id: int) -> list[dict[str, Any]]:
        logs = self.repo.get_logs(item_id)
        return [
            {
                "id": log.id,
                "change_qty": log.change_qty,
                "reason": log.reason,
                "changed_by": log.changed_by_user.username if log.changed_by_user else "System",
                "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for log in logs
        ]
