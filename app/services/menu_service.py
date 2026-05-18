from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.repositories.menu_repository import MenuRepository


@dataclass(frozen=True)
class MenuService:
    repo: MenuRepository

    def list_all(self) -> list[dict[str, Any]]:
        items = self.repo.list_all()
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": float(item.price),
                "category": item.category,
                "is_available": item.is_available,
                "image_url": item.image_url,
            }
            for item in items
        ]

    def list_available(self) -> list[dict[str, Any]]:
        items = self.repo.list_available()
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": float(item.price),
                "category": item.category,
                "image_url": item.image_url,
            }
            for item in items
        ]

    def create(self, name: str, price: float, category: str, description: Optional[str] = None, image_url: Optional[str] = None) -> dict[str, Any]:
        item = self.repo.create(name, price, category)
        if description:
            item.description = description
        if image_url:
            item.image_url = image_url
        self.repo.save()
        return {"success": True, "data": {"id": item.id}}

    def update(
        self, item_id: int, name: Optional[str] = None, price: Optional[float] = None, 
        category: Optional[str] = None, description: Optional[str] = None, image_url: Optional[str] = None
    ) -> dict[str, Any] | tuple[dict[str, Any], int]:
        success = self.repo.update(item_id, name, price, category)
        if not success:
            return {"error": "Menu item not found"}, 404
        
        item = self.repo.get(item_id)
        if description is not None:
            item.description = description
        if image_url:
            item.image_url = image_url
        
        self.repo.save()
        return {"success": True}

    def toggle_availability(
        self, item_id: int
    ) -> dict[str, Any] | tuple[dict[str, Any], int]:
        success = self.repo.toggle_availability(item_id)
        if not success:
            return {"error": "Menu item not found"}, 404
        self.repo.save()
        item = self.repo.get(item_id)
        return {"success": True, "is_available": item.is_available}

    def delete(self, item_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        success = self.repo.delete(item_id)
        if not success:
            return {"error": "Menu item not found"}, 404
        self.repo.save()
        return {"success": True}
