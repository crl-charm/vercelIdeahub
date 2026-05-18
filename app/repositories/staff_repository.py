from __future__ import annotations

from datetime import date
from typing import Optional
from decimal import Decimal

from app import db
from app.models.staff_performance import StaffPerformanceLog


class StaffRepository:
    def get_log(self, log_id: int) -> Optional[StaffPerformanceLog]:
        return StaffPerformanceLog.query.filter_by(id=log_id).first()

    def get_by_user_and_date(
        self, user_id: int, shift_date: date
    ) -> Optional[StaffPerformanceLog]:
        return StaffPerformanceLog.query.filter_by(
            user_id=user_id, shift_date=shift_date
        ).first()

    def list_all(self) -> list[StaffPerformanceLog]:
        return StaffPerformanceLog.query.order_by(
            StaffPerformanceLog.score.desc()
        ).all()

    def list_by_date(self, shift_date: date) -> list[StaffPerformanceLog]:
        return StaffPerformanceLog.query.filter_by(shift_date=shift_date).order_by(
            StaffPerformanceLog.score.desc()
        ).all()

    def list_by_user(self, user_id: int) -> list[StaffPerformanceLog]:
        return StaffPerformanceLog.query.filter_by(user_id=user_id).order_by(
            StaffPerformanceLog.shift_date.desc()
        ).all()

    def create(
        self,
        user_id: int,
        shift_date: date,
        customers_served: int,
        admin_note: Optional[str] = None,
    ) -> StaffPerformanceLog:
        log = StaffPerformanceLog(
            user_id=user_id,
            shift_date=shift_date,
            customers_served=customers_served,
            admin_note=admin_note,
        )
        log.score = log.calculate_score()
        db.session.add(log)
        db.session.flush()
        return log

    def save(self) -> None:
        db.session.commit()
