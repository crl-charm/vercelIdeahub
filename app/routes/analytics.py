from __future__ import annotations

from flask import Blueprint

from app.repositories.analytics_repository import AnalyticsRepository
from app.dto.api_response import api_ok
from app.services.analytics_service import AnalyticsChartService
from app.utils.auth import login_required

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")

_service = AnalyticsChartService(repo=AnalyticsRepository())


@analytics_bp.route("/daily-revenue", methods=["GET"])
@login_required
def daily_revenue() -> tuple:
    return api_ok(_service.daily_revenue(30))


@analytics_bp.route("/top-items", methods=["GET"])
@login_required
def top_items() -> tuple:
    return api_ok(_service.top_menu_items(10))


@analytics_bp.route("/space-utilization", methods=["GET"])
@login_required
def space_utilization() -> tuple:
    return api_ok(_service.space_utilization())


@analytics_bp.route("/peak-hours", methods=["GET"])
@login_required
def peak_hours() -> tuple:
    return api_ok(_service.peak_hours())
