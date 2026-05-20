from functools import wraps
from flask import session, redirect, jsonify, flash, request, current_app
from datetime import datetime, timedelta
import logging

security_logger = logging.getLogger('security')


def _expects_json_response() -> bool:
    """True for API/fetch calls that should receive JSON instead of redirects."""
    path = request.path or ""
    if path.startswith("/api/") or "/api/" in path:
        return True
    if path.startswith("/admin/") and "/api/" in path:
        return True
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return True
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    return best == "application/json" and best is not None


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in
        if "user_id" not in session:
            if _expects_json_response():
                return jsonify({"success": False, "error": "Unauthorized"}), 401
            flash("Please log in first!", "danger")
            return redirect("/login")

        # Check session timeout
        last_activity = session.get('last_activity')
        if last_activity:
            session_timeout = current_app.config.get('PERMANENT_SESSION_LIFETIME', 3600 * 24)
            if datetime.utcnow().timestamp() - last_activity > session_timeout:
                security_logger.warning(f"Session timeout for user {session.get('username')} from {request.remote_addr}")
                session.clear()
                if _expects_json_response():
                    return jsonify({"success": False, "error": "Session expired"}), 401
                flash("Your session has expired. Please log in again.", "warning")
                return redirect("/login")

        # Update last activity
        session['last_activity'] = datetime.utcnow().timestamp()

        return view_func(*args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # Check authentication first
        if "user_id" not in session:
            if _expects_json_response():
                return jsonify({"success": False, "error": "Unauthorized"}), 401
            flash("Please log in first!", "danger")
            return redirect("/login")

        # Check session timeout
        last_activity = session.get('last_activity')
        if last_activity:
            session_timeout = current_app.config.get('PERMANENT_SESSION_LIFETIME', 3600 * 24)
            if datetime.utcnow().timestamp() - last_activity > session_timeout:
                security_logger.warning(f"Session timeout for admin user {session.get('username')} from {request.remote_addr}")
                session.clear()
                if _expects_json_response():
                    return jsonify({"success": False, "error": "Session expired"}), 401
                flash("Your session has expired. Please log in again.", "warning")
                return redirect("/login")

        # Check admin role
        role = (session.get("role") or "").lower()
        if role not in {"admin", "manager"}:
            security_logger.warning(f"Unauthorized admin access attempt by {session.get('username')} from {request.remote_addr}")
            if _expects_json_response():
                return jsonify({"success": False, "error": "Forbidden"}), 403
            flash("Admin access required.", "danger")
            return redirect("/dashboard")

        # Update last activity
        session['last_activity'] = datetime.utcnow().timestamp()

        return view_func(*args, **kwargs)
    return wrapper


def sanitize_input(input_string):
    """Sanitize user input to prevent XSS"""
    if not input_string:
        return input_string

    # Basic HTML escaping
    return (input_string
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;')
            .replace('/', '&#x2F;'))