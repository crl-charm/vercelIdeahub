from __future__ import annotations

from enum import Enum

from app import db
from app.models.base_model import BaseModel


class UserRole(str, Enum):
    """Supported application-level user roles."""

    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


