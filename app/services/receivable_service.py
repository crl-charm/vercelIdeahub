from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Optional

from app.repositories.receivable_repository import ReceivableRepository


@dataclass(frozen=True)
class ReceivableService:
    repo: ReceivableRepository

    def list_all(self) -> list[dict[str, Any]]:
        receivables = self.repo.list_all()
        return [
            {
                "id": r.id,
                "customer_name": r.customer_name,
                "customer_contact": r.customer_contact,
                "items": r.items_description,
                "amount_owed": float(r.amount_owed),
                "partial_paid": float(r.partial_paid),
                "due_date": r.due_date.strftime("%Y-%m-%d"),
                "paid": r.paid,
                "created_by": r.created_by_user.username if r.created_by_user else "Unknown",
            }
            for r in receivables
        ]

    def list_unpaid(self) -> list[dict[str, Any]]:
        receivables = self.repo.list_unpaid()
        return [
            {
                "id": r.id,
                "customer_name": r.customer_name,
                "amount_owed": float(r.amount_owed),
                "partial_paid": float(r.partial_paid),
                "due_date": r.due_date.strftime("%Y-%m-%d"),
            }
            for r in receivables
        ]

    def create(
        self,
        customer_name: str,
        customer_contact: str,
        items_description: str,
        amount_owed: float,
        due_date: str,
        created_by: int,
        session_id: Optional[int],
    ) -> dict[str, Any]:
        due = date.fromisoformat(due_date)
        receivable = self.repo.create(
            customer_name, customer_contact, items_description, amount_owed, due, created_by, session_id
        )
        self.repo.save()
        return {"success": True, "data": {"id": receivable.id}}

    def mark_paid(self, receivable_id: int) -> dict[str, Any] | tuple[dict[str, Any], int]:
        success = self.repo.mark_paid(receivable_id)
        if not success:
            return {"error": "Receivable not found"}, 404
        self.repo.save()
        from app.core.socketio_handlers import emit_receivable_marked_paid

        emit_receivable_marked_paid(receivable_id)
        return {"success": True}

    def emit_due_reminders(self) -> None:
        due_today = self.repo.list_due_today()
        for r in due_today:
            from app.core.socketio_handlers import emit_debt_due_reminder

            emit_debt_due_reminder({
                "receivable_id": r.id,
                "customer_name": r.customer_name,
                "amount_owed": float(r.amount_owed),
            })
