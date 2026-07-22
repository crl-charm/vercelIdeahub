from __future__ import annotations

from flask import Blueprint, jsonify, request, render_template, session

from app.core import get_notifier
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService
from app.utils.auth import admin_required
from app.models.menu_item import MenuItem
from app import db, csrf
from app.core.socketio_handlers import emit_inventory_update

inventory_bp = Blueprint("inventory", __name__, url_prefix="/admin/inventory")

_service = InventoryService(repo=InventoryRepository())


@inventory_bp.route("", methods=["GET"])
@admin_required
def list_items() -> str:
    items = _service.list_all()
    return render_template("admin/inventory.html", items=items)


@inventory_bp.route("/api/items", methods=["GET"])
@admin_required
def api_list_items() -> tuple:
    items = _service.list_all()
    return jsonify({"success": True, "data": items}), 200


@inventory_bp.route("/api/items", methods=["POST"])
@admin_required
@csrf.exempt
def api_create_item() -> tuple:
    data = request.get_json()
    menu_item_id = data.get("menu_item_id")
    ingredient_name = (data.get("ingredient_name") or "").strip()
    if not menu_item_id and ingredient_name:
        existing = MenuItem.query.filter(MenuItem.name.ilike(ingredient_name)).first()
        if existing:
            menu_item_id = existing.id
        else:
            created = MenuItem(name=ingredient_name, price=0, category="ingredient", is_available=True)
            db.session.add(created)
            db.session.flush()
            menu_item_id = created.id
    if not menu_item_id:
        return jsonify({"success": False, "error": "Select an item or provide ingredient_name"}), 400
    result = _service.create(
        menu_item_id=menu_item_id,
        stock_qty=int(data.get("stock_qty", 0)),
        low_stock_threshold=int(data.get("low_stock_threshold", 10)),
        unit=data.get("unit", "pieces"),
    )
    if result.get("success"):
        emit_inventory_update('create', result.get("data", {}))
    return jsonify(result), 201


@inventory_bp.route("/api/items/<int:item_id>/stock", methods=["PATCH"])
@admin_required
@csrf.exempt
def api_update_stock(item_id: int) -> tuple:
    data = request.get_json()
    result = _service.update_stock(
        item_id=item_id,
        new_qty=int(data.get("new_qty")),
        reason=data.get("reason", "Manual adjustment"),
        user_id=session.get("user_id"),
    )
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        emit_inventory_update('stock_change', {'item_id': item_id, 'new_qty': data.get("new_qty")})
    return jsonify(result), 200


@inventory_bp.route("/api/menu-items/<int:menu_item_id>/stock", methods=["PATCH"])
@admin_required
@csrf.exempt
def api_update_stock_by_menu_item(menu_item_id: int) -> tuple:
    data = request.get_json()
    result = _service.update_stock(
        item_id=None,
        menu_item_id=menu_item_id,
        new_qty=int(data.get("new_qty")),
        reason=data.get("reason", "Manual adjustment"),
        user_id=session.get("user_id"),
    )
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        inv_id = result.get("data", {}).get("inventory_item_id")
        emit_inventory_update('stock_change', {'item_id': inv_id, 'new_qty': data.get("new_qty")})
    return jsonify(result), 200


@inventory_bp.route("/api/items/<int:item_id>/logs", methods=["GET"])
@admin_required
def api_get_logs(item_id: int) -> tuple:
    logs = _service.get_logs(item_id)
    return jsonify({"success": True, "data": logs}), 200


@inventory_bp.route("/api/low-stock", methods=["GET"])
@admin_required
def api_low_stock() -> tuple:
    items = _service.get_low_stock()
    return jsonify({"success": True, "data": items}), 200


@inventory_bp.route("/api/items/<int:item_id>", methods=["DELETE"])
@admin_required
@csrf.exempt
def api_delete_item(item_id: int) -> tuple:
    result = _service.delete(item_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        emit_inventory_update('delete', {'item_id': item_id})
    return jsonify(result), 200


@inventory_bp.route("/api/direct-stock", methods=["GET"])
@admin_required
def api_direct_stock() -> tuple:
    return jsonify({"success": True, "data": _service.build_direct_stock_items()}), 200


@inventory_bp.route("/api/recipe-inventory", methods=["GET"])
@admin_required
def api_recipe_inventory() -> tuple:
    return jsonify({"success": True, "data": _service.build_recipe_inventory_items()}), 200


@inventory_bp.route("/api/dashboard-items", methods=["GET"])
@admin_required
def api_dashboard_items() -> tuple:
    return jsonify(
        {
            "success": True,
            "data": _service.build_recipe_inventory_items(),
            "direct_stock": _service.build_direct_stock_items(),
        }
    ), 200


@inventory_bp.route("/api/recipes/<int:menu_item_id>", methods=["GET"])
@admin_required
def get_recipe(menu_item_id: int) -> tuple:
    return jsonify({"success": True, "data": _service.build_recipe_detail(menu_item_id)}), 200


@inventory_bp.route("/api/recipes", methods=["POST"])
@admin_required
@csrf.exempt
def add_recipe_ingredient() -> tuple:
    from app.models.menu_item import MenuItemIngredient

    data = request.get_json() or {}
    menu_item_id = data.get("menu_item_id")
    ingredient_item_id = data.get("ingredient_item_id")
    qty = float(data.get("quantity_required", 1.0))

    if not menu_item_id or not ingredient_item_id:
        return jsonify({"success": False, "error": "Missing menu_item_id or ingredient_item_id"}), 400

    if menu_item_id == ingredient_item_id:
        return jsonify({"success": False, "error": "A meal cannot be linked to itself as an ingredient"}), 400

    ingredient = MenuItem.query.get(ingredient_item_id)
    if not ingredient or ingredient.category != "ingredient":
        return jsonify({"success": False, "error": "ingredient_item_id must be a raw ingredient"}), 400

    meal = MenuItem.query.get(menu_item_id)
    if not meal or meal.category == "ingredient":
        return jsonify({"success": False, "error": "menu_item_id must be a sellable meal"}), 400

    _service.ensure_inventory_row(int(ingredient_item_id))

    existing = MenuItemIngredient.query.filter_by(
        menu_item_id=menu_item_id,
        ingredient_item_id=ingredient_item_id,
    ).first()
    if existing:
        existing.quantity_required = qty
    else:
        new_map = MenuItemIngredient(
            menu_item_id=menu_item_id,
            ingredient_item_id=ingredient_item_id,
            quantity_required=qty,
        )
        db.session.add(new_map)
    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@inventory_bp.route("/api/recipes/<int:recipe_id>", methods=["DELETE"])
@admin_required
@csrf.exempt
def delete_recipe_ingredient(recipe_id: int) -> tuple:
    from app.models.menu_item import MenuItemIngredient

    mapping = MenuItemIngredient.query.get(recipe_id)
    if not mapping:
        return jsonify({"success": False, "error": "Recipe component not found"}), 404
    try:
        db.session.delete(mapping)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@inventory_bp.route("/api/ingredients/<int:menu_item_id>", methods=["DELETE"])
@admin_required
@csrf.exempt
def api_delete_ingredient(menu_item_id: int) -> tuple:
    result = _service.delete_raw_ingredient(menu_item_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        emit_inventory_update("delete", {"menu_item_id": menu_item_id})
    return jsonify(result), 200


@inventory_bp.route("/api/ingredients", methods=["GET"])
@admin_required
def list_ingredients() -> tuple:
    q = request.args.get("q")
    data = _service.list_ingredients_for_picker(q)
    return jsonify({"success": True, "data": data}), 200


@inventory_bp.route("/api/meals", methods=["GET"])
@admin_required
def list_meals() -> tuple:
    q = request.args.get("q", "").strip()
    query = MenuItem.query.filter(
        MenuItem.category != "ingredient",
        MenuItem.status != "deleted",
    )
    if q:
        query = query.filter(MenuItem.name.ilike(f"%{q}%"))
    meals = query.order_by(MenuItem.name).all()
    data = [{"id": m.id, "name": m.name} for m in meals]
    return jsonify({"success": True, "data": data}), 200
