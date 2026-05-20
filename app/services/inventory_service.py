from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.repositories.inventory_repository import InventoryRepository


@dataclass(frozen=True)
class InventoryService:
    repo: InventoryRepository

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
        item = self.repo.create(menu_item_id, stock_qty, low_stock_threshold, unit)
        self.repo.save()
        return {"success": True, "data": {"id": item.id}}

    def update_stock(
        self,
        item_id: int,
        new_qty: int,
        reason: str,
        user_id: Optional[int],
    ) -> dict[str, Any] | tuple[dict[str, Any], int]:
        item = self.repo.get_item(item_id)
        if not item:
            return {"error": "Inventory item not found"}, 404
        old_qty = item.stock_qty
        change = new_qty - old_qty
        if change > 0:
            self.repo.add(item_id, change, reason, user_id)
        elif change < 0:
            self.repo.deduct(item_id, abs(change), reason, user_id)
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
        item = self.repo.get_by_menu_item_id(menu_item_id)
        if not item:
            return False
        success = self.repo.deduct(item.id, qty, "Order deduction", None)
        if success:
            self.repo.save()
            if item.stock_qty < item.low_stock_threshold:
                from app.core.socketio_handlers import emit_inventory_low_stock

                emit_inventory_low_stock({
                    "item_id": item.id,
                    "menu_item": item.menu_item.name,
                    "stock_qty": item.stock_qty,
                    "threshold": item.low_stock_threshold,
                })
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
