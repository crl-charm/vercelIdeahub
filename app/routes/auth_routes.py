from flask import Blueprint, render_template, request, jsonify, session, redirect
from app.models import User, StaffAttendance
from app import db, limiter, csrf
from datetime import datetime
import logging

bp = Blueprint("auth", __name__)

security_logger = logging.getLogger('security')


def get_redirect_by_role(role):
    if role == "admin":
        return "/admin"
    return "/dashboard"


@bp.route("/login")
def login_page():

    if "user_id" in session:
        return redirect(get_redirect_by_role(session.get("role")))

    return render_template("login.html")


@bp.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
@csrf.exempt
def login_api():
    """Secure login with rate limiting and account lockout"""
    try:
        data = request.get_json()

        # Input validation
        if not data or not isinstance(data, dict):
            security_logger.warning("Invalid login request format")
            return jsonify({"error": "Invalid request format"}), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            security_logger.warning(f"Missing credentials for login attempt: {request.remote_addr}")
            return jsonify({"error": "Username and password are required"}), 400

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user:
            security_logger.warning(f"Login attempt for non-existent user: {username} from {request.remote_addr}")
            return jsonify({"error": "Invalid credentials"}), 401

        # Check if account is locked
        if user.is_locked():
            security_logger.warning(f"Login attempt on locked account: {username} from {request.remote_addr}")
            return jsonify({"error": "Account is temporarily locked due to too many failed attempts"}), 429

        # Verify password
        if user.check_password(password):
            # Clear existing session and start a fresh one
            session.clear()
            session.modified = True

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            session["job_role"] = user.job_role

            # Log attendance
            attendance = StaffAttendance(user_id=user.id, time_in=datetime.utcnow())
            db.session.add(attendance)
            db.session.commit()
            session["attendance_id"] = attendance.id

            security_logger.info(f"Successful login: {username} from {request.remote_addr}")
            return jsonify({
                "message": "Login successful",
                "redirect": get_redirect_by_role(user.role)
            })
        else:
            security_logger.warning(f"Failed login attempt: {username} from {request.remote_addr}")
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        security_logger.exception(f"Login error: {str(e)} from {request.remote_addr}")
        db.session.rollback()
        return jsonify({"error": "Login failed"}), 500


@bp.route("/logout")
def logout():
    """Secure logout with session cleanup"""
    try:
        attendance_id = session.get("attendance_id")
        if attendance_id:
            attendance = StaffAttendance.query.get(attendance_id)
            if attendance and attendance.time_out is None:
                attendance.time_out = datetime.utcnow()
                db.session.commit()

        username = session.get("username", "unknown")
        security_logger.info(f"Logout: {username} from {request.remote_addr}")
        session.clear()
        return redirect("/login")
    except Exception as e:
        security_logger.error(f"Logout error: {str(e)}")
        session.clear()
        return redirect("/login")