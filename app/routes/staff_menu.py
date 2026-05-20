from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from app.repositories.menu_repository import MenuRepository
from app.services.menu_service import MenuService
from app.utils.auth import login_required

staff_menu_bp = Blueprint("staff_menu", __name__, url_prefix="/menu-view")

_service = MenuService(repo=MenuRepository())


@staff_menu_bp.route("", methods=["GET"])
@login_required
def view_menu() -> str:
    items = _service.list_for_ordering()
    return render_template("staff/menu.html", items=items)


@staff_menu_bp.route("/api/items", methods=["GET"])
@login_required
def api_list_items() -> tuple:
    items = _service.list_for_ordering()
    return jsonify({"success": True, "data": items}), 200
