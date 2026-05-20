from __future__ import annotations

from datetime import date
from typing import Any

from flask import Blueprint, request, render_template, session

from app.dto.api_response import api_error, api_ok

from app import db
from app.repositories.sales_repository import SalesRepository
from app.services.daily_balance_export_service import DailyBalanceExportService
from app.services.sales_service import SalesService
from app.utils.auth import admin_required

sales_bp = Blueprint("sales_admin", __name__, url_prefix="/admin/daily-balance")

_service = SalesService(repo=SalesRepository())
_export = DailyBalanceExportService(db)


@sales_bp.route("", methods=["GET"])
@admin_required
def list_reports() -> str:
    reports = _service.list_reports()
    soft_entries = _service.list_soft_balances()
    return render_template("admin/daily_balance.html", reports=reports, soft_entries=soft_entries)


@sales_bp.route("/api/reports", methods=["GET"])
@admin_required
def api_list_reports() -> tuple:
    reports = _service.list_reports()
    return api_ok(reports)


@sales_bp.route("/api/reports", methods=["POST"])
@admin_required
def api_generate_report() -> tuple:
    data = request.get_json()
    report_date = date.fromisoformat(data.get("report_date"))
    result = _service.generate_report(
        report_date=report_date,
        generated_by=session.get("user_id"),
        notes=data.get("notes"),
    )
    return api_ok(result.get("data"), status=201)


@sales_bp.route("/api/reports/export-csv", methods=["GET"])
@admin_required
def api_export_csv() -> Any:
    reports = _service.list_reports()
    return _export.export_csv(reports)


@sales_bp.route("/api/reports/export-pdf", methods=["GET"])
@admin_required
def api_export_pdf() -> Any:
    try:
        reports = _service.list_reports()
        soft_entries = _service.list_soft_balances()
        return _export.export_pdf(reports, soft_entries)
    except Exception as e:
        return api_error(f"Failed to export PDF: {str(e)}", status=500)


@sales_bp.route("/api/reports/export-excel", methods=["GET"])
@admin_required
def api_export_excel() -> Any:
    try:
        reports = _service.list_reports()
        return _export.export_excel(reports)
    except Exception as e:
        return api_error(f"Failed to export Excel: {str(e)}", status=500)


@sales_bp.route("/api/soft-balances", methods=["GET"])
@admin_required
def api_list_soft_balances() -> tuple:
    entries = _service.list_soft_balances()
    return api_ok(entries)


@sales_bp.route("/api/soft-balances", methods=["POST"])
@admin_required
def api_create_soft_balance() -> tuple:
    data = request.get_json()
    balance_date = date.fromisoformat(data.get("balance_date"))
    period = (data.get("period") or "AM").upper()
    result = _service.create_soft_balance(
        balance_date=balance_date,
        period=period,
        generated_by=session.get("user_id"),
        notes=data.get("notes"),
    )
    return api_ok(result.get("data"), status=201)
