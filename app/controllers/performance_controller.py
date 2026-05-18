from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from app.controllers.base_controller import BaseController
from app.services.performance_oop_service import PerformanceService
from app.utils.auth import admin_required


class PerformanceController(BaseController):
    """Serves performance page and metrics API."""

    def __init__(self, db) -> None:
        self._service = PerformanceService(db)
        self.blueprint = Blueprint("performance_page", __name__)
        self._register_routes()

    def _register_routes(self) -> None:
        @self.blueprint.get("/performance")
        @admin_required
        def performance_page():
            data = self._service.get_summary()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template("performance/_content.html", **data)
            return render_template("performance/index.html", **data)

        @self.blueprint.get("/api/performance/metrics")
        @admin_required
        def performance_metrics():
            return jsonify({"success": True, "data": self._service.get_summary()})

    def get_dashboard_data(self) -> dict:
        return self._service.get_dashboard_data()
