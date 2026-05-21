from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import func

from app import db
from app.models import BoardroomBooking, CustomerSession, SpaceType


class BookingRepository:
    def get_booking(self, booking_id: int) -> Optional[BoardroomBooking]:
        return BoardroomBooking.query.filter_by(id=booking_id).first()

    def list_bookings(self, selected_date: Optional[date], status_filter: str) -> list[BoardroomBooking]:
        query = BoardroomBooking.query
        if selected_date:
            query = query.filter(BoardroomBooking.date == selected_date)
        if status_filter == "active":
            query = query.filter(BoardroomBooking.status == "active")
        elif status_filter == "booked":
            query = query.filter(BoardroomBooking.status == "booked")
        elif status_filter == "open":
            query = query.filter(BoardroomBooking.status.in_(["booked", "active"]))
        return query.order_by(BoardroomBooking.date, BoardroomBooking.start_time).all()

    def list_overdue_active(self, now: datetime) -> list[BoardroomBooking]:
        return (
            BoardroomBooking.query.filter(BoardroomBooking.status == "active")
            .filter(BoardroomBooking.expected_end_at.isnot(None))
            .filter(BoardroomBooking.expected_end_at <= now)
            .all()
        )

    def find_conflict(self, selected_date: date, start_time: time, end_time: time) -> Optional[BoardroomBooking]:
        rows = BoardroomBooking.query.filter(
            BoardroomBooking.date == selected_date,
            BoardroomBooking.status.in_(["booked", "active"]),
            BoardroomBooking.start_time < end_time,
            BoardroomBooking.end_time > start_time,
        ).all()
        return rows[0] if rows else None

    def find_conflict_excluding(
        self,
        booking_id: int,
        selected_date: date,
        start_time: time,
        end_time: time,
    ) -> Optional[BoardroomBooking]:
        rows = BoardroomBooking.query.filter(
            BoardroomBooking.id != booking_id,
            BoardroomBooking.date == selected_date,
            BoardroomBooking.status.in_(["booked", "active"]),
            BoardroomBooking.start_time < end_time,
            BoardroomBooking.end_time > start_time,
        ).all()
        return rows[0] if rows else None

    def get_boardroom_space(self) -> Optional[SpaceType]:
        return SpaceType.query.filter_by(name="Boardroom").first()

    def sum_active_boardroom_occupancy(self, boardroom_space_id: int) -> int:
        occupied = (
            db.session.query(func.coalesce(func.sum(CustomerSession.number_of_people), 0))
            .filter(
                CustomerSession.space_type_id == boardroom_space_id,
                CustomerSession.status == "active",
            )
            .scalar()
        ) or 0
        return int(occupied)

    def create_customer_session_for_booking(
        self,
        booking: BoardroomBooking,
        boardroom_space_id: int,
        started_at: datetime,
    ) -> CustomerSession:
        session = CustomerSession(
            customer_name=booking.customer_name,
            school="Boardroom Booking",
            course=booking.course or "N/A",
            number_of_people=booking.number_of_people or 1,
            space_type_id=boardroom_space_id,
            time_in=started_at,
            status="active",
        )
        db.session.add(session)
        db.session.flush()
        return session

    def save(self) -> None:
        db.session.commit()

    def add(self, obj) -> None:
        db.session.add(obj)
