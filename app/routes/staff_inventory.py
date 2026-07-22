from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService
from app.utils.auth import login_required

staff_inventory_bp = Blueprint("staff_inventory", __name__, url_prefix="/inventory")

_service = InventoryService(repo=InventoryRepository())


@staff_inventory_bp.route("", methods=["GET"])
@login_required
def view_inventory() -> str:
    return render_template("staff/inventory.html")


@staff_inventory_bp.route("/api/items", methods=["GET"])
@login_required
def api_list_items() -> tuple:
    items = _service.list_all()
    return jsonify({"success": True, "data": items}), 200


@staff_inventory_bp.route("/api/dashboard-items", methods=["GET"])
@login_required
def api_dashboard_items() -> tuple:
    return jsonify(
        {
            "success": True,
            "data": _service.build_recipe_inventory_items(),
            "direct_stock": _service.build_direct_stock_items(),
        }
    ), 200
