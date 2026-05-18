from flask import Blueprint, jsonify, render_template, session, redirect
from app.models import User
from app.utils.auth import login_required, admin_required

user_bp = Blueprint("user_routes", __name__)

@user_bp.route("/api/profile/<int:user_id>")
@login_required
def get_profile(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Staff not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.full_name,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at
    })


@user_bp.route("/profile")
@login_required
def profile_page():

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user:
        session.clear()
        return redirect("/login")

    return render_template("profile.html", user=user)


@user_bp.route("/api/users")
@admin_required
def list_users():
    users = User.query.order_by(User.username.asc()).all()
    data = [{"id": u.id, "username": u.username, "role": u.role} for u in users]
    return jsonify({"success": True, "data": data})