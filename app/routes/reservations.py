from __future__ import annotations

from flask import Blueprint, jsonify, request, render_template

from app.repositories.reservation_repository import ReservationRepository
from app.services.reservation_service import ReservationService
from app.utils.auth import admin_required

reservations_bp = Blueprint("reservations", __name__, url_prefix="/admin/reservations")

_service = ReservationService(repo=ReservationRepository())


@reservations_bp.route("", methods=["GET"])
@admin_required
def list_page() -> str:
    reservations = _service.list_all()
    return render_template("admin/reservations.html", reservations=reservations)


@reservations_bp.route("/api/reservations", methods=["GET"])
@admin_required
def api_list() -> tuple:
    reservations = _service.list_all()
    return jsonify({"success": True, "data": reservations}), 200


@reservations_bp.route("/api/reservations", methods=["POST"])
@admin_required
def api_create() -> tuple:
    data = request.get_json()
    result = _service.create(
        customer_name=data.get("customer_name"),
        customer_contact=data.get("customer_contact"),
        space_type_id=int(data.get("space_type_id")),
        reserved_date=data.get("reserved_date"),
        reserved_time=data.get("reserved_time"),
        duration_minutes=int(data.get("duration_minutes", 60)),
        number_of_people=int(data.get("number_of_people", 1)),
        notes=data.get("notes"),
    )
    return jsonify(result), 201


@reservations_bp.route("/api/reservations/<int:res_id>/status", methods=["PATCH"])
@admin_required
def api_update_status(res_id: int) -> tuple:
    data = request.get_json()
    result = _service.update_status(res_id, data.get("status"))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@reservations_bp.route("/api/reservations/<int:res_id>", methods=["DELETE"])
@admin_required
def api_delete(res_id: int) -> tuple:
    result = _service.delete(res_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@reservations_bp.route("/api/spaces", methods=["GET"])
@admin_required
def api_spaces() -> tuple:
    from app.models import SpaceType

    spaces = SpaceType.query.order_by(SpaceType.name.asc()).all()
    data = [{"id": s.id, "name": s.name} for s in spaces]
    return jsonify({"success": True, "data": data}), 200
