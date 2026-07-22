from flask import Blueprint, jsonify, request

from app.core.clock import SystemClock
from app.repositories.sales_repository import SalesRepository
from app.services.sales_service import SalesService
from app.utils.auth import admin_required


sales_bp = Blueprint("sales_routes", __name__)
_service = SalesService(repo=SalesRepository(), clock=SystemClock())


@sales_bp.route("/api/daily-sales")
@admin_required
def daily_sales():
    return jsonify(_service.daily_sales())


@sales_bp.route("/api/sales-summary")
@admin_required
def sales_summary():
    period = request.args.get("period", "today")
    return jsonify(_service.sales_summary(period))


@sales_bp.route("/api/sales-compare")
@admin_required
def sales_compare():
    return jsonify(_service.sales_compare())
