from __future__ import annotations

from flask import Blueprint, jsonify, request, render_template, session

from app.repositories.payable_repository import PayableRepository
from app.services.payable_service import PayableService
from app.utils.auth import admin_required

payables_bp = Blueprint("payables", __name__, url_prefix="/admin/payables")

_service = PayableService(repo=PayableRepository())


@payables_bp.route("", methods=["GET"])
@admin_required
def list_payables() -> str:
    return render_template("admin/payables.html")


@payables_bp.route("/api/payables", methods=["GET"])
@admin_required
def api_list_payables() -> tuple:
    payables = _service.list_all()
    return jsonify({"success": True, "data": payables}), 200


@payables_bp.route("/api/payables", methods=["POST"])
@admin_required
def api_create_payable() -> tuple:
    data = request.get_json() or {}
    result = _service.create(
        creditor_name=data.get("creditor_name"),
        items_description=data.get("items_description"),
        amount_owed=float(data.get("amount_owed") or 0),
        due_date=data.get("due_date"),
        incurred_date=data.get("incurred_date"),
        created_by=session.get("user_id"),
    )
    return jsonify(result), 201


@payables_bp.route("/api/payables/<int:p_id>/mark-paid", methods=["PATCH"])
@admin_required
def api_mark_paid(p_id: int) -> tuple:
    result = _service.mark_paid(p_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@payables_bp.route("/api/due-count", methods=["GET"])
@admin_required
def api_due_count() -> tuple:
    count = _service.get_due_count()
    return jsonify({"success": True, "count": count}), 200
