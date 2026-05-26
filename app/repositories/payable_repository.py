from __future__ import annotations

from datetime import date
from typing import Optional

from app import db
from app.models.payable import Payable


class PayableRepository:
    def get(self, payable_id: int) -> Optional[Payable]:
        return Payable.query.filter_by(id=payable_id).first()

    def list_all(self) -> list[Payable]:
        return Payable.query.order_by(Payable.due_date.asc()).all()

    def create(
        self,
        creditor_name: str,
        items_description: str,
        amount_owed: float,
        due_date: date,
        incurred_date: date,
        created_by: int,
    ) -> Payable:
        payable = Payable(
            creditor_name=creditor_name,
            items_description=items_description,
            amount_owed=amount_owed,
            due_date=due_date,
            incurred_date=incurred_date,
            created_by=created_by,
            status="Unpaid",
            partial_paid=0.00
        )
        db.session.add(payable)
        db.session.flush()
        return payable

    def mark_paid(self, payable_id: int) -> bool:
        payable = self.get(payable_id)
        if not payable:
            return False
        payable.status = "Paid"
        return True

    def save(self) -> None:
        db.session.commit()
