from __future__ import annotations

from datetime import datetime, timedelta
from typing import TypedDict, Optional

from sqlalchemy import func, and_

from app.models import Transaction, OrderItem, MenuItem, Order
from app.services.export_service import ExportService


class AnalyticsSummary(TypedDict):
    daily_sales: list[dict]
    top_foods: list[dict]
    date_range: dict


class AnalyticsReportService(ExportService):
    """Admin analytics page: daily sales summary, top foods, PDF export."""

    def get_summary(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> AnalyticsSummary:
        """Get daily sales and top food analytics."""
        # Default to last 30 days if not specified
        if not end_date:
            end_date = datetime.utcnow().date()
        else:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except:
                end_date = datetime.utcnow().date()
        
        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except:
                start_date = end_date - timedelta(days=30)

        # Get daily sales data
        daily_sales_rows = (
            self._db.session.query(
                func.date(Transaction.created_at).label("date"),
                func.sum(Transaction.total_bill).label("revenue"),
                func.count(Transaction.id).label("transactions"),
            )
            .filter(
                and_(
                    func.date(Transaction.created_at) >= start_date,
                    func.date(Transaction.created_at) <= end_date,
                )
            )
            .group_by(func.date(Transaction.created_at))
            .order_by(func.date(Transaction.created_at))
            .all()
        )
        
        daily_sales = [
            {
                "date": str(row.date),
                "revenue": float(row.revenue or 0),
                "transactions": int(row.transactions or 0),
            }
            for row in daily_sales_rows
        ]

        # Get top selling foods
        top_foods_rows = (
            self._db.session.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * OrderItem.price).label("total_revenue"),
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(
                and_(
                    func.date(Order.created_at) >= start_date,
                    func.date(Order.created_at) <= end_date,
                )
            )
            .group_by(MenuItem.id, MenuItem.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(10)
            .all()
        )
        
        top_foods = [
            {
                "name": row.name,
                "quantity": int(row.total_quantity or 0),
                "revenue": float(row.total_revenue or 0),
            }
            for row in top_foods_rows
        ]

        return {
            "daily_sales": daily_sales,
            "top_foods": top_foods,
            "date_range": {
                "start": str(start_date),
                "end": str(end_date),
            },
        }

    def get_dashboard_data(self) -> dict:
        return self.get_summary()


# Backward-compatible alias (deprecated name)
AnalyticsService = AnalyticsReportService
