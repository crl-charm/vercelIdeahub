from __future__ import annotations

from app import db
from app.models.base_model import BaseModel


class Idea(db.Model, BaseModel):
    """Stores innovation ideas submitted by users."""

    __tablename__ = "ideas"

    _title = db.Column("title", db.String(200), nullable=False)
    _description = db.Column("description", db.Text, nullable=True)
    _status = db.Column("status", db.String(30), nullable=False, default="pending")
    _department_id = db.Column("department_id", db.Integer, db.ForeignKey("departments.id"))
    _user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="ideas")
    department = db.relationship("Department", backref="ideas")

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = (value or "").strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = (value or "pending").strip().lower()


class IdeaVote(db.Model, BaseModel):
    """Stores one user vote for one idea."""

    __tablename__ = "idea_votes"

    _idea_id = db.Column("idea_id", db.Integer, db.ForeignKey("ideas.id"), nullable=False)
    _user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False)
    _is_upvote = db.Column("is_upvote", db.Boolean, nullable=False, default=True)

    idea = db.relationship("Idea", backref="votes")
    user = db.relationship("User", backref="idea_votes")
