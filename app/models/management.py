from __future__ import annotations

from enum import Enum

from app import db
from app.models.base_model import BaseModel


class UserRole(str, Enum):
    """Supported application-level user roles."""

    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class Department(db.Model, BaseModel):
    """Department grouping used by management and idea assignment."""

    __tablename__ = "departments"

    _name = db.Column("name", db.String(120), nullable=False, unique=True)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = (value or "").strip()
