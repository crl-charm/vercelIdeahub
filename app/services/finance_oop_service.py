from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func

from app.models.finance import FinanceBudget, FinanceTransaction
from app.services.export_service import ExportService


class FinanceService(ExportService):
    """Handles finance summary, transactions, and reporting."""

    def get_summary(self) -> dict:
        total_budget = self._db.session.query(func.sum(FinanceBudget._total_budget)).scalar() or Decimal("0.00")
        allocated = self._db.session.query(func.sum(FinanceBudget._allocated)).scalar() or Decimal("0.00")
        spent = self._db.session.query(func.sum(FinanceTransaction._amount)).filter(FinanceTransaction._type == "expense").scalar() or Decimal("0.00")
        transactions = (
            FinanceTransaction.query.order_by(FinanceTransaction.created_at.desc()).limit(20).all()
        )
        remaining = Decimal(total_budget) - Decimal(spent)
        return {
            "total_budget": float(total_budget),
            "allocated": float(allocated),
            "spent": float(spent),
            "remaining": float(remaining),
            "transactions": [
                {
                    "id": txn.id,
                    "type": txn._type,
                    "amount": float(txn._amount),
                    "description": txn._description,
                    "created_at": txn.created_at.isoformat(),
                }
                for txn in transactions
            ],
        }

    def add_transaction(self, budget_id: int, txn_type: str, amount: float, description: str | None = None) -> dict:
        txn = FinanceTransaction(
            _budget_id=budget_id,
            _type=(txn_type or "expense").strip().lower(),
            _amount=Decimal(str(amount or 0)),
            _description=description,
        )
        self._db.session.add(txn)
        self._db.session.commit()
        return {"id": txn.id}

    def get_report(self) -> dict:
        return self.get_summary()

    def get_dashboard_data(self) -> dict:
        return self.get_summary()
