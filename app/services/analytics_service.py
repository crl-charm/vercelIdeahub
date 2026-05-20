from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.repositories.analytics_repository import AnalyticsRepository


@dataclass(frozen=True)
class AnalyticsChartService:
    """Chart.js datasets for /api/analytics/* chart endpoints."""

    repo: AnalyticsRepository

    def daily_revenue(self, days: int = 30) -> dict[str, Any]:
        data = self.repo.daily_revenue(days)
        return {
            "labels": [d["date"] for d in data],
            "datasets": [
                {
                    "label": "Revenue (₱)",
                    "data": [d["revenue"] for d in data],
                    "borderColor": "#c9a43a",
                    "backgroundColor": "rgba(201, 164, 58, 0.1)",
                }
            ],
        }

    def top_menu_items(self, limit: int = 10) -> dict[str, Any]:
        data = self.repo.top_menu_items(limit)
        return {
            "labels": [d["name"] for d in data],
            "datasets": [
                {
                    "label": "Orders",
                    "data": [d["count"] for d in data],
                    "backgroundColor": "#3b82f6",
                }
            ],
        }

    def space_utilization(self) -> dict[str, Any]:
        data = self.repo.space_utilization()
        return {
            "labels": [f"Space {d['space_id']}" for d in data],
            "datasets": [
                {
                    "label": "Utilization",
                    "data": [1 for _ in data],
                    "backgroundColor": ["#10b981", "#3b82f6", "#f59e0b"],
                }
            ],
        }

    def peak_hours(self) -> dict[str, Any]:
        data = self.repo.peak_hours()
        return {
            "labels": [f"{d['hour']}:00" for d in data],
            "datasets": [
                {
                    "label": "Transactions",
                    "data": [d["count"] for d in data],
                    "backgroundColor": "#ef4444",
                }
            ],
        }
