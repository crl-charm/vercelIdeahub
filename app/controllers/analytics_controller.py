from __future__ import annotations

from flask import Blueprint, Response, render_template, request

from app.controllers.base_controller import BaseController
from app.dto.api_response import api_ok
from app.services.analytics_oop_service import AnalyticsReportService
from app.utils.auth import admin_required


class AnalyticsController(BaseController):
    """Serves analytics pages and analytics API endpoints."""

    def __init__(self, db) -> None:
        self._service = AnalyticsReportService(db)
        self.blueprint = Blueprint("analytics_page", __name__)
        self._register_routes()

    def _register_routes(self) -> None:
        @self.blueprint.get("/analytics")
        @admin_required
        def analytics_page():
            data = self._service.get_summary()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return render_template("analytics/_content.html", **data)
            return render_template("analytics/index.html", **data)

        @self.blueprint.get("/api/analytics/summary")
        @admin_required
        def analytics_summary():
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            data = self._service.get_summary(start_date=start_date, end_date=end_date)
            return api_ok(data)

        @self.blueprint.get("/api/analytics/export")
        @admin_required
        def analytics_export():
            pdf = self._service.render_pdf_bytes("analytics/_content.html", **self._service.get_summary())
            return Response(
                pdf,
                mimetype="application/pdf",
                headers={"Content-Disposition": "attachment; filename=analytics-summary.pdf"},
            )

    def get_dashboard_data(self) -> dict:
        return self._service.get_dashboard_data()
