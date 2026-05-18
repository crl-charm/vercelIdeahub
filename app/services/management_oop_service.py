from __future__ import annotations

from app.models.management import Department, UserRole
from app.models.user import User
from app.services.base_service import BaseService


class ManagementService(BaseService):
    """Handles user/department administration operations."""

    def get_users(self, page: int = 1, per_page: int = 20) -> dict:
        result = self.paginate(User.query.order_by(User.id.asc()), page=page, per_page=per_page)
        return {
            "items": [
                {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role,
                    "job_role": user.job_role,
                }
                for user in result.items
            ],
            "page": result.page,
            "pages": result.pages,
            "total": result.total,
        }

    def update_role(self, user_id: int, role: str) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        normalized = (role or "").strip().lower()
        if normalized not in {r.value for r in UserRole}:
            return False
        user.role = normalized
        user.job_role = normalized
        self._db.session.commit()
        return True

    def get_departments(self) -> list[dict]:
        return [{"id": d.id, "name": d.name} for d in Department.query.order_by(Department._name.asc()).all()]

    def get_summary(self) -> dict:
        return {"users": User.query.count(), "departments": Department.query.count()}

    def get_dashboard_data(self) -> dict:
        return self.get_summary()
