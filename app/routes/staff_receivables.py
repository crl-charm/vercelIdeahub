from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from app.repositories.receivable_repository import ReceivableRepository
from app.services.receivable_service import ReceivableService
from app.utils.auth import login_required

staff_receivables_bp = Blueprint("staff_receivables", __name__, url_prefix="/receivables-view")

_service = ReceivableService(repo=ReceivableRepository())


@staff_receivables_bp.route("", methods=["GET"])
@login_required
def view_receivables() -> str:
    receivables = _service.list_all()
    return render_template("staff/receivables.html", receivables=receivables)


@staff_receivables_bp.route("/api/receivables", methods=["GET"])
@login_required
def api_list_receivables() -> tuple:
    receivables = _service.list_all()
    return jsonify({"success": True, "data": receivables}), 200


@staff_receivables_bp.route("/api/receivables", methods=["POST"])
@login_required
def api_create_receivable() -> tuple:
    from flask import request, session

    data = request.get_json(silent=True) or {}
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"success": False, "error": "User session not found"}), 400

    try:
        amount = float(data.get("amount_owed"))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid amount"}), 400

    result = _service.create(
        customer_name=data.get("customer_name"),
        customer_contact=data.get("customer_contact"),
        items_description=data.get("items_description"),
        amount_owed=amount,
        due_date=data.get("due_date"),
        created_by=user_id,
        session_id=session.get("session_id"),
        approved_by_staff=data.get("approved_by_staff"),
        incurred_date=data.get("incurred_date"),
    )
    return jsonify(result), 201
