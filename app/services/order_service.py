from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from typing import Any, Optional

from app.core.interfaces import Notifier
from app.models import MenuItem
from app.repositories.order_repository import OrderRepository


def _normalize_item_status(status: str | None) -> str:
    if status in {None, "preparin"}:
        return "preparing"
    return status or "preparing"


def _item_is_ready(status: str | None) -> bool:
    return _normalize_item_status(status) == "done"


@dataclass(frozen=True)
class OrderService:
    repo: OrderRepository
    notifier: Notifier

    def _order_has_preparing_items(self, order) -> bool:
        return any(not _item_is_ready(item.status) for item in order.items)

    def _session_preparing_item_count(self, session_id: int) -> int:
        orders = self.repo.list_orders_for_session(session_id, include_done=False)
        return sum(
            1
            for order in orders
            for item in order.items
            if not _item_is_ready(item.status)
        )

    def list_menu(self) -> list[dict[str, Any]]:
        from app.services.inventory_service import InventoryService
        from app.repositories.inventory_repository import InventoryRepository

        inv_service = InventoryService(repo=InventoryRepository())
        try:
            inv_items = inv_service.build_recipe_inventory_items()
            inv_data = {item["id"]: item for item in inv_items}
        except Exception:
            inv_data = {}

        items = self.repo.list_menu_items()
        results = []
        for i in items:
            inv_info = inv_data.get(i.id, {})
            # If item is not in inventory database, default capacity to a high number (e.g. 99)
            # or treat it as direct item. Since build_recipe_inventory_items includes all non-ingredient items,
            # they should normally be present.
            capacity = inv_info.get("capacity", 99.0)
            is_low = inv_info.get("is_low", False)
            
            # Out of stock if capacity is 0 or less
            is_out_of_stock = capacity <= 0
            
            results.append(
                {
                    "id": i.id,
                    "name": i.name,
                    "price": float(i.price),
                    "category": i.category,
                    "description": i.description,
                    "image_url": i.image_url,
                    "is_available": bool(i.is_available) and not is_out_of_stock,
                    "is_low_stock": is_low,
                    "is_out_of_stock": is_out_of_stock,
                    "capacity": float(capacity),
                }
            )
        return results

    def add_order(self, *, session_id: int, items: list[dict], handled_by: Optional[int]) -> dict[str, Any] | tuple[dict[str, Any], int]:
        sess = self.repo.get_session(session_id)
        if not sess:
            return {"error": "Session not found"}, 404

        for item in items:
            menu_item_id = item.get("menu_item_id")
            if not menu_item_id:
                return {"error": "Invalid menu item in order"}, 400

            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item or menu_item.status == "deleted":
                return {"error": "One or more items are no longer on the menu"}, 400
            if not menu_item.is_available:
                return {"error": f"{menu_item.name} is not available"}, 400

        # Validate ingredient stock availability
        from app.models.menu_item import MenuItemIngredient
        from app.models.inventory import InventoryItem

        ingredient_needs = {}
        for item in items:
            menu_item_id = item.get("menu_item_id")
            qty = float(item.get("quantity", 1))
            menu_item = MenuItem.query.get(menu_item_id)

            recipe = MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()
            if recipe:
                for comp in recipe:
                    ratio = float(comp.conversion_ratio or 1.0)
                    needed = qty * float(comp.quantity_required) * ratio
                    if comp.ingredient_item_id not in ingredient_needs:
                        ingredient_needs[comp.ingredient_item_id] = [0.0, []]
                    ingredient_needs[comp.ingredient_item_id][0] += needed
                    ingredient_needs[comp.ingredient_item_id][1].append(menu_item.name)
            else:
                inv = InventoryItem.query.filter_by(menu_item_id=menu_item_id).first()
                if inv:
                    if menu_item_id not in ingredient_needs:
                        ingredient_needs[menu_item_id] = [0.0, []]
                    ingredient_needs[menu_item_id][0] += qty
                    ingredient_needs[menu_item_id][1].append(menu_item.name)

        for ing_id, (needed_qty, meals) in ingredient_needs.items():
            inv = InventoryItem.query.filter_by(menu_item_id=ing_id).first()
            current_stock = float(inv.stock_qty) if inv else 0.0
            if current_stock < needed_qty:
                ing_item = MenuItem.query.get(ing_id)
                ing_name = ing_item.name if ing_item else "Ingredient"
                meal_list = ", ".join(set(meals))
                return {"error": f"Insufficient stock for '{ing_name}' (Need {needed_qty:.2f}, Have {current_stock:.2f}) to prepare {meal_list}."}, 400

        order_id = self.repo.add_order_with_items(session_id=session_id, handled_by=handled_by, items=items)
        
        # Deduct inventory for each item in the order
        from app.repositories.inventory_repository import InventoryRepository
        from app.services.inventory_service import InventoryService
        from app import socketio
        
        inv_repo = InventoryRepository()
        inv_service = InventoryService(repo=inv_repo)
        
        for item in items:
            menu_item_id = item.get("menu_item_id")
            qty = item.get("quantity", 1)
            if menu_item_id:
                inv_service.deduct_on_order(menu_item_id, qty)
        
        self.notifier.order_status_changed({"order_id": order_id, "status": "preparing", "session_id": session_id})
        return {"message": "Order added successfully", "order_id": order_id}

    def update_order_status(self, *, order_id: int, new_status: str) -> dict[str, Any] | tuple[dict[str, Any], int]:
        if new_status not in {"preparin", "preparing", "serving", "done"}:
            return {"error": "Invalid status"}, 400

        order = self.repo.get_order(order_id)
        if not order:
            return {"error": "Order not found"}, 404

        sess = self.repo.get_session(order.customer_session_id)
        if not sess or sess.status != "active":
            return {"error": "Cannot update inactive session orders"}, 400

        if new_status == "serving":
            if order.status not in {"preparin", "preparing"}:
                return {"error": "Order must be in preparing before serving"}, 400
            if self._order_has_preparing_items(order):
                return {
                    "error": "All items must be marked Done before this order can be served"
                }, 400
        elif new_status == "done":
            if order.status != "serving":
                return {"error": "Order must be in serving before done"}, 400
        else:
            return {"error": "This action is not supported"}, 400

        order.status = new_status
        self.repo.commit()
        self.notifier.order_status_changed(
            {"order_id": order_id, "status": order.status, "session_id": order.customer_session_id}
        )
        return {"message": "Order status updated", "order_id": order_id, "status": order.status}

    def get_session_orders(self, *, session_id: int, include_done: bool) -> dict[str, Any]:
        sess = self.repo.get_session(session_id)
        if not sess or sess.status != "active":
            return {
                "session_id": session_id,
                "customer_name": sess.customer_name if sess else None,
                "space_type": sess.space_type.name if sess and sess.space_type else None,
                "time_in": (sess.time_in + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p") if sess and sess.time_in else None,
                "orders": [],
                "food_total": 0.0,
                "preparing_count": 0,
                "can_serve": False,
            }

        orders = self.repo.list_orders_for_session(session_id, include_done=include_done)
        order_list: list[dict[str, Any]] = []
        food_total = Decimal("0.00")

        for order in orders:
            for item in order.items:
                total_price = item.quantity * item.price
                food_total += total_price
                order_list.append(
                    {
                        "id": item.id,
                        "order_id": order.id,
                        "order_status": order.status,
                        "item_status": item.status if item.status else "preparing",
                        "handled_by_name": order.handler.full_name if order.handler else "N/A",
                        "item_name": item.menu_item.name,
                        "quantity": item.quantity,
                        "price": float(item.price),
                        "total": float(total_price),
                    }
                )

        preparing_count = sum(
            1 for row in order_list if not _item_is_ready(row.get("item_status"))
        )

        return {
            "session_id": session_id,
            "customer_name": sess.customer_name,
            "space_type": sess.space_type.name if sess.space_type else None,
            "time_in": (sess.time_in + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p") if sess.time_in else None,
            "orders": order_list,
            "food_total": float(food_total),
            "preparing_count": preparing_count,
            "can_serve": len(order_list) > 0 and preparing_count == 0,
        }

    def pending_count(self) -> dict[str, int]:
        return self.repo.pending_counts()

    def session_orders_list_view(self) -> list[dict[str, Any]]:
        sessions = self.repo.list_active_session_orders_summary()
        result: list[dict[str, Any]] = []
        for sess in sessions:
            orders = [o for o in sess.orders if o.status != "done"]
            if not orders:
                continue
            item_count = 0
            food_total = Decimal("0.00")
            latest_status = "preparing"
            for order in orders:
                latest_status = order.status
                for item in order.items:
                    item_count += 1
                    food_total += item.quantity * item.price
            if latest_status == "preparin":
                latest_status = "preparing"
            result.append(
                {
                    "session_id": sess.id,
                    "customer_name": sess.customer_name,
                    "space_type": sess.space_type.name if sess.space_type else "N/A",
                    "time_in": (sess.time_in + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p")
                    if sess.time_in
                    else "N/A",
                    "orders_count": item_count,
                    "food_total": float(food_total),
                    "active_order_status": latest_status,
                }
            )
        return result

    def mark_session_served(self, session_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        sess = self.repo.get_session(session_id)
        if not sess:
            return {"error": "Session not found"}, 404
        if sess.status != "active":
            return {"error": "Session is not active"}, 400

        preparing_count = self._session_preparing_item_count(session_id)
        if preparing_count > 0:
            return {
                "error": (
                    f"Cannot mark as served: {preparing_count} item(s) still preparing. "
                    "Mark every item as Done first."
                )
            }, 400

        self.repo.mark_session_served(session_id)
        self.notifier.order_status_changed({"session_id": session_id, "status": "done"})
        return {"message": "Session marked as served", "session_id": session_id}

    def void_item(self, item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        item = self.repo.get_order_item(item_id)
        if not item:
            return {"error": "Item not found"}, 404
        if item.quantity > 1:
            item.quantity -= 1
        else:
            from app import db
            db.session.delete(item)
        self.repo.commit()
        return {"message": "One item voided successfully"}

    def create_from_qr(self, order_data: dict[str, Any]) -> dict[str, Any]:
        space_type_id = order_data.get("space_type_id")
        customer_name = order_data.get("customer_name", "Walk-in")
        items = order_data.get("items", [])

        if not items:
            return {"error": "No items in order"}

        from app.models import CustomerSession, SpaceType
        space = self.repo.db.session.query(SpaceType).filter_by(id=space_type_id).first()
        if not space:
            return {"error": "Space not found"}

        session = CustomerSession(
            customer_name=customer_name,
            space_type_id=space_type_id,
            number_of_people=1,
        )
        self.repo.db.session.add(session)
        self.repo.db.session.flush()

        order_id = self.repo.add_order_with_items(
            session_id=session.id,
            handled_by=None,
            items=items,
        )
        self.repo.db.session.commit()
        self.notifier.order_status_changed(
            {"order_id": order_id, "status": "preparing", "session_id": session.id}
        )
        return {"success": True, "data": {"order_id": order_id, "session_id": session.id}}

    def toggle_order_item_status(self, item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        item = self.repo.get_order_item(item_id)
        if not item:
            return {"error": "Item not found"}, 404
        if _item_is_ready(item.status):
            item.status = "preparing"
        else:
            item.status = "done"
        self.repo.commit()
        self.notifier.order_status_changed(
            {"order_id": item.order_id, "item_id": item.id, "status": item.status}
        )
        return {"message": "Item status updated", "item_id": item_id, "status": item.status}