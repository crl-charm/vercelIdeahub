from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from app import db
from app.models.receivable import Receivable


class ReceivableRepository:
    def get(self, receivable_id: int) -> Optional[Receivable]:
        return Receivable.query.filter_by(id=receivable_id).first()

    def list_all(self) -> list[Receivable]:
        return Receivable.query.order_by(Receivable.due_date).all()

    def list_unpaid(self) -> list[Receivable]:
        return Receivable.query.filter(
            Receivable.paid == False,
            Receivable.due_date <= date.today(),
        ).order_by(Receivable.due_date).all()

    def list_due_today(self) -> list[Receivable]:
        return Receivable.query.filter(
            Receivable.due_date == date.today(),
            Receivable.paid == False,
        ).all()

    def create(
        self,
        customer_name: str,
        customer_contact: str,
        items_description: str,
        amount_owed: float,
        due_date: date,
        created_by: int,
        session_id: Optional[int],
    ) -> Receivable:
        receivable = Receivable(
            customer_name=customer_name,
            customer_contact=customer_contact,
            items_description=items_description,
            amount_owed=amount_owed,
            due_date=due_date,
            created_by=created_by,
            session_id=session_id,
        )
        db.session.add(receivable)
        db.session.flush()
        return receivable

    def mark_paid(self, receivable_id: int) -> bool:
        receivable = self.get(receivable_id)
        if not receivable:
            return False
        receivable.paid = True
        return True

    def mark_partial_paid(self, receivable_id: int, amount: float) -> bool:
        receivable = self.get(receivable_id)
        if not receivable:
            return False
        receivable.partial_paid = amount
        return True

    def save(self) -> None:
        db.session.commit()
