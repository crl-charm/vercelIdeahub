from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import func, and_
from app import db
from app.models import Order, User
from app.repositories.staff_repository import StaffRepository


@dataclass(frozen=True)
class StaffPerformanceService:
    repo: StaffRepository

    def list_all(self) -> list[dict[str, Any]]:
        logs = self.repo.list_all()
        return [
            {
                "id": log.id,
                "user_id": log.user_id,
                "username": log.user.username if log.user else "Unknown",
                "shift_date": log.shift_date.strftime("%Y-%m-%d"),
                "customers_served": log.customers_served,
                "score": float(log.score),
                "admin_note": log.admin_note,
            }
            for log in logs
        ]

    def list_by_date(self, shift_date: str) -> list[dict[str, Any]]:
        date_obj = date.fromisoformat(shift_date)
        logs = self.repo.list_by_date(date_obj)
        return [
            {
                "id": log.id,
                "username": log.user.username,
                "customers_served": log.customers_served,
                "score": float(log.score),
            }
            for log in logs
        ]

    def list_by_user(self, user_id: int) -> list[dict[str, Any]]:
        logs = self.repo.list_by_user(user_id)
        return [
            {
                "id": log.id,
                "shift_date": log.shift_date.strftime("%Y-%m-%d"),
                "customers_served": log.customers_served,
                "score": float(log.score),
            }
            for log in logs
        ]

    def create(
        self,
        user_id: int,
        shift_date: str,
        customers_served: int,
        admin_note: Optional[str] = None,
    ) -> dict[str, Any]:
        date_obj = date.fromisoformat(shift_date)
        log = self.repo.create(
            user_id,
            date_obj,
            customers_served,
            admin_note,
        )
        self.repo.save()
        return {"success": True, "data": {"id": log.id, "score": float(log.score)}}

    def calculate_customer_count(self, user_id: int, shift_date: date) -> int:
        """Calculate unique customers served by a staff member on a shift date."""
        count = db.session.query(
            func.count(func.distinct(Order.customer_session_id))
        ).filter(
            and_(
                Order.handled_by == user_id,
                func.date(Order.created_at) == shift_date,
            )
        ).scalar() or 0
        return int(count)
