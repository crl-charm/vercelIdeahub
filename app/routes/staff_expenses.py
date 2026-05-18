from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.utils.auth import login_required

staff_expenses_bp = Blueprint("staff_expenses", __name__, url_prefix="/expenses-view")

_service = ExpenseService(repo=ExpenseRepository())

CATEGORIES = ["supplies", "utilities", "food", "transport", "misc"]


@staff_expenses_bp.route("", methods=["GET"])
@login_required
def view_expenses() -> str:
    expenses = _service.list_all()
    return render_template("staff/expenses.html", expenses=expenses, categories=CATEGORIES)


@staff_expenses_bp.route("/api/expenses", methods=["GET"])
@login_required
def api_list_expenses() -> tuple:
    expenses = _service.list_all()
    return jsonify({"success": True, "data": expenses}), 200
