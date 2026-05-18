from __future__ import annotations

from datetime import date
from typing import Optional
from decimal import Decimal

from sqlalchemy import func

from app import db
from app.models import Transaction, DailySalesReport, Order, CustomerSession, Expense, SoftBalanceEntry


class SalesRepository:
    def summary_for_range(self, start_date: date, end_date: date):
        return (
            Transaction.query.with_entities(
                func.count(Transaction.id).label("transactions"),
                func.coalesce(func.sum(Transaction.total_bill), 0).label("total_revenue"),
                func.coalesce(func.sum(Transaction.time_bill), 0).label("space_revenue"),
                func.coalesce(func.sum(Transaction.food_bill), 0).label("food_revenue"),
            )
            .filter(func.date(Transaction.created_at) >= start_date)
            .filter(func.date(Transaction.created_at) <= end_date)
            .first()
        )

    def summary_for_day(self, target_date: date):
        return self.summary_for_range(target_date, target_date)

    def get_daily_report(self, report_date: date) -> Optional[DailySalesReport]:
        return DailySalesReport.query.filter_by(report_date=report_date).first()

    def list_reports(self) -> list[DailySalesReport]:
        return DailySalesReport.query.order_by(DailySalesReport.report_date.desc()).all()

    def create_report(
        self,
        report_date: date,
        total_revenue: Decimal,
        total_expenses: Decimal,
        net_balance: Decimal,
        total_orders: int,
        total_sessions: int,
        generated_by: int,
        notes: Optional[str],
    ) -> DailySalesReport:
        report = DailySalesReport(
            report_date=report_date,
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            net_balance=net_balance,
            total_orders=total_orders,
            total_sessions=total_sessions,
            generated_by=generated_by,
            notes=notes,
        )
        db.session.add(report)
        db.session.flush()
        return report

    def get_daily_transactions(self, report_date: date) -> list[Transaction]:
        return (
            Transaction.query.filter(
                func.date(Transaction.created_at) == report_date
            )
            .order_by(Transaction.created_at)
            .all()
        )

    def get_daily_orders(self, report_date: date) -> list[Order]:
        return (
            Order.query.join(CustomerSession)
            .filter(func.date(CustomerSession.time_in) == report_date)
            .all()
        )

    def get_daily_sessions(self, report_date: date) -> list[CustomerSession]:
        return (
            CustomerSession.query.filter(
                func.date(CustomerSession.time_in) == report_date
            )
            .all()
        )

    def save(self) -> None:
        db.session.commit()

    def sum_expenses_for_day(self, target_date: date) -> Decimal:
        value = (
            db.session.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.expense_date == target_date)
            .scalar()
        )
        return Decimal(str(value or 0))

    def list_soft_balances(self) -> list[SoftBalanceEntry]:
        return SoftBalanceEntry.query.order_by(SoftBalanceEntry.balance_date.desc(), SoftBalanceEntry.period.asc()).all()

    def create_soft_balance(
        self,
        balance_date: date,
        period: str,
        total_revenue: Decimal,
        total_expenses: Decimal,
        net_balance: Decimal,
        generated_by: int,
        notes: Optional[str],
    ) -> SoftBalanceEntry:
        entry = SoftBalanceEntry(
            balance_date=balance_date,
            period=period,
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            net_balance=net_balance,
            generated_by=generated_by,
            notes=notes,
        )
        db.session.add(entry)
        db.session.flush()
        return entry
