from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import selectinload

from app import db
from app.models import CustomerSession, Order, OrderItem, SpaceType, StaffAttendance, User


class AdminRepository:
    def list_staff_paginated(self, page: int, per_page: int):
        return (
            User.query.filter_by(role="staff")
            .order_by(User.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    def list_online_staff_ids(self) -> set[int]:
        rows = StaffAttendance.query.with_entities(StaffAttendance.user_id).filter(
            StaffAttendance.time_out.is_(None)
        )
        return {row.user_id for row in rows.all()}

    def get_staff_user(self, user_id: int):
        return User.query.filter_by(id=user_id, role="staff").first()

    def username_exists_for_other(self, username: str, user_id: int) -> bool:
        existing = User.query.filter_by(username=username).first()
        return bool(existing and existing.id != user_id)

    def delete_staff_attendance(self, user_id: int) -> None:
        StaffAttendance.query.filter_by(user_id=user_id).delete()

    def clear_user_orders(self, user_id: int) -> None:
        Order.query.filter_by(handled_by=user_id).update({"handled_by": None})

    def list_customer_sessions(self) -> list[CustomerSession]:
        return (
            CustomerSession.query.options(
                selectinload(CustomerSession.orders)
                .selectinload(Order.items)
                .selectinload(OrderItem.menu_item),
                selectinload(CustomerSession.space_type),
            )
            .order_by(CustomerSession.time_in.desc())
            .all()
        )

    def list_staff_attendance(self) -> list[StaffAttendance]:
        return (
            StaffAttendance.query.options(selectinload(StaffAttendance.user))
            .order_by(StaffAttendance.time_in.desc())
            .all()
        )

    def list_spaces_with_occupancy(self):
        return (
            db.session.query(
                SpaceType.id,
                SpaceType.name,
                SpaceType.capacity,
                func.coalesce(func.sum(CustomerSession.number_of_people), 0).label("occupied"),
            )
            .outerjoin(
                CustomerSession,
                (CustomerSession.space_type_id == SpaceType.id)
                & (CustomerSession.status == "active"),
            )
            .group_by(SpaceType.id, SpaceType.name, SpaceType.capacity)
            .all()
        )

    def get_space(self, space_id: int):
        return SpaceType.query.get(space_id)

    def staff_analytics(self):
        return (
            db.session.query(
                User.id,
                User.full_name,
                User.job_role,
                func.count(Order.id).label("orders_count"),
                func.count(func.distinct(Order.customer_session_id)).label("customers_count"),
            )
            .outerjoin(Order, Order.handled_by == User.id)
            .filter(User.role == "staff")
            .group_by(User.id, User.full_name, User.job_role)
            .all()
        )

    def save(self) -> None:
        db.session.commit()

    def add(self, obj) -> None:
        db.session.add(obj)
