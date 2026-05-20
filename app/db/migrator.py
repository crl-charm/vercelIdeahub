from __future__ import annotations

from sqlalchemy import text
from app.models.idea import Idea, IdeaVote
from app.models.finance import FinanceBudget, FinanceTransaction
from app.models.management import Department
from app.models.soft_balance import SoftBalanceEntry
from app.models.space_price_history import SpacePriceHistory


class SchemaMigrator:
    """Runs ALTER TABLE statements in an idempotent way."""

    def __init__(self, db, app) -> None:
        self._db = db
        self._app = app

    def run(self) -> None:
        db = self._db
        _ = (Idea, IdeaVote, FinanceBudget, FinanceTransaction, Department, SoftBalanceEntry, SpacePriceHistory)
        try:
            db.create_all()
        except Exception as e:
            print(f"⚠ Database migration skipped (database unavailable): {e}")
            return
        checks = [
            (
                "orders",
                "status",
                "ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'preparing'",
            ),
            (
                "order_items",
                "status",
                "ALTER TABLE order_items ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'preparing'",
            ),
            ("space_types", "capacity", "ALTER TABLE space_types ADD COLUMN capacity INT NULL"),
            (
                "users",
                "job_role",
                "ALTER TABLE users ADD COLUMN job_role VARCHAR(50) NOT NULL DEFAULT 'general'",
            ),
            ("orders", "handled_by", "ALTER TABLE orders ADD COLUMN handled_by INT NULL"),
            (
                "customer_sessions",
                "number_of_people",
                "ALTER TABLE customer_sessions ADD COLUMN number_of_people INT NOT NULL DEFAULT 1",
            ),
            ("boardroom_bookings", "session_id", "ALTER TABLE boardroom_bookings ADD COLUMN session_id INT NULL"),
            ("boardroom_bookings", "started_at", "ALTER TABLE boardroom_bookings ADD COLUMN started_at DATETIME NULL"),
            (
                "boardroom_bookings",
                "expected_end_at",
                "ALTER TABLE boardroom_bookings ADD COLUMN expected_end_at DATETIME NULL",
            ),
            ("boardroom_bookings", "ended_at", "ALTER TABLE boardroom_bookings ADD COLUMN ended_at DATETIME NULL"),
            (
                "boardroom_bookings",
                "extended_minutes",
                "ALTER TABLE boardroom_bookings ADD COLUMN extended_minutes INT NOT NULL DEFAULT 0",
            ),
            ("boardroom_bookings", "course", "ALTER TABLE boardroom_bookings ADD COLUMN course VARCHAR(100) NULL"),
            (
                "customer_sessions",
                "payment_method",
                "ALTER TABLE customer_sessions ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cash'",
            ),
            (
                "transactions",
                "payment_method",
                "ALTER TABLE transactions ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cash'",
            ),
            (
                "customer_sessions",
                "amount_tendered",
                "ALTER TABLE customer_sessions ADD COLUMN amount_tendered DECIMAL(10,2) NULL",
            ),
            (
                "menu_items",
                "is_available",
                "ALTER TABLE menu_items ADD COLUMN is_available BOOLEAN DEFAULT TRUE",
            ),
            (
                "space_types",
                "qr_token",
                "ALTER TABLE space_types ADD COLUMN qr_token VARCHAR(50) NULL UNIQUE",
            ),
            (
                "staff_performance_logs",
                "customers_served",
                "ALTER TABLE staff_performance_logs ADD COLUMN customers_served INT NOT NULL DEFAULT 0",
            ),
        ]
        for table_name, column_name, ddl in checks:
            has_col = db.session.execute(
                text(
                    """
                SELECT COLUMN_NAME
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = :table_name
                AND COLUMN_NAME = :column_name
            """
                ),
                {"table_name": table_name, "column_name": column_name},
            ).fetchall()
            if has_col:
                continue
            try:
                db.session.execute(text(ddl))
                db.session.commit()
            except Exception:
                db.session.rollback()

        self._ensure_indexes(db)

    def _ensure_indexes(self, db) -> None:
        """Create performance indexes idempotently (MySQL)."""
        indexes = [
            (
                "transactions",
                "idx_transactions_created_at",
                "CREATE INDEX idx_transactions_created_at ON transactions (created_at)",
            ),
            (
                "transactions",
                "idx_transactions_payment_method",
                "CREATE INDEX idx_transactions_payment_method ON transactions (payment_method)",
            ),
            (
                "customer_sessions",
                "idx_customer_sessions_time_in",
                "CREATE INDEX idx_customer_sessions_time_in ON customer_sessions (time_in)",
            ),
            (
                "orders",
                "idx_orders_session_status",
                "CREATE INDEX idx_orders_session_status ON orders (customer_session_id, status, id)",
            ),
            (
                "order_items",
                "idx_order_items_order_id",
                "CREATE INDEX idx_order_items_order_id ON order_items (order_id)",
            ),
            (
                "boardroom_bookings",
                "idx_bookings_status_end",
                "CREATE INDEX idx_bookings_status_end ON boardroom_bookings (status, expected_end_at)",
            ),
        ]
        for table_name, index_name, ddl in indexes:
            exists = db.session.execute(
                text(
                    """
                SELECT INDEX_NAME
                FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = :table_name
                AND INDEX_NAME = :index_name
                LIMIT 1
            """
                ),
                {"table_name": table_name, "index_name": index_name},
            ).fetchone()
            if exists:
                continue
            try:
                db.session.execute(text(ddl))
                db.session.commit()
                print(f"✓ Created index {index_name} on {table_name}")
            except Exception as exc:
                db.session.rollback()
                print(f"⚠ Index {index_name} skipped: {exc}")
