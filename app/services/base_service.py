from __future__ import annotations


class BaseService:
    """Base service with shared DB helpers."""

    def __init__(self, db) -> None:
        self._db = db

    def paginate(self, query, page: int, per_page: int):
        """Paginate SQLAlchemy query objects consistently."""
        return query.paginate(page=page, per_page=per_page, error_out=False)
