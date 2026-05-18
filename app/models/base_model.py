from __future__ import annotations

from datetime import datetime

from app import db


class BaseModel:
    """Reusable timestamped primary-key mixin for SQLAlchemy models."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
