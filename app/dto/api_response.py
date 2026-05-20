from __future__ import annotations

from typing import Any

from flask import jsonify


def api_ok(data: Any = None, status: int = 200):
    """Standard success envelope for JSON APIs."""
    body: dict[str, Any] = {"success": True}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def api_error(message: str, status: int = 400, **extra: Any):
    """Standard error envelope for JSON APIs."""
    body: dict[str, Any] = {"success": False, "error": message}
    if extra:
        body.update(extra)
    return jsonify(body), status
