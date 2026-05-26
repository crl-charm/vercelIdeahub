from flask import Blueprint, render_template, session, redirect
from app.utils.auth import login_required

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@bp.route("/checkout-records")
@login_required
def checkout_records_page():
    return render_template("checkout_records.html")


@bp.route("/daily-sales")
@login_required
def daily_sales_page():
    return redirect("/admin/daily-balance")