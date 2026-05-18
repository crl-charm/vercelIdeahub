from __future__ import annotations

from dataclasses import dataclass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.db.migrator import SchemaMigrator
from app.db.seeder import DatabaseSeeder
from app.models.user import User


@dataclass
class CheckResult:
    method: str
    path: str
    status: int | None
    ok: bool
    error: str | None = None


def run() -> int:
    app = create_app()
    results: list[CheckResult] = []

    with app.app_context():
        SchemaMigrator(db, app).run()
        DatabaseSeeder(db, app).run()
        admin = User.query.filter_by(username="admin").first() or User.query.first()

    if not admin:
        print("ERROR: no user record available for authenticated route checks.")
        return 2

    test_matrix = [
        ("GET", "/admin/daily-balance"),
        ("GET", "/admin/daily-balance/api/reports"),
        ("POST", "/admin/daily-balance/api/reports"),
        ("GET", "/admin/daily-balance/api/soft-balances"),
        ("POST", "/admin/daily-balance/api/soft-balances"),
        ("GET", "/admin/expenses"),
        ("GET", "/admin/expenses/api/expenses"),
        ("POST", "/admin/expenses/api/expenses"),
        ("GET", "/admin/inventory"),
        ("GET", "/admin/inventory/api/items"),
        ("POST", "/admin/inventory/api/items"),
        ("GET", "/admin/menu"),
        ("GET", "/admin/menu/api/items/all"),
        ("POST", "/admin/menu/api/items"),
        ("GET", "/admin/reservations"),
        ("GET", "/admin/reservations/api/reservations"),
        ("POST", "/admin/reservations/api/reservations"),
        ("GET", "/admin/staff-performance"),
        ("GET", "/admin/staff-performance/api/logs"),
        ("POST", "/admin/staff-performance/api/logs"),
        ("GET", "/analytics"),
        ("GET", "/api/analytics/summary"),
        ("GET", "/api/analytics/export"),
        ("GET", "/performance"),
        ("GET", "/api/performance/metrics"),
        ("GET", "/finance"),
        ("GET", "/finance/budget"),
        ("GET", "/finance/expenses"),
        ("GET", "/finance/reports"),
        ("GET", "/api/finance/summary"),
        ("POST", "/api/finance/transaction"),
        ("GET", "/api/finance/export"),
        ("GET", "/management"),
        ("GET", "/management/users"),
        ("GET", "/management/departments"),
        ("GET", "/management/settings"),
        ("GET", "/api/management/users"),
        ("POST", f"/api/management/users/{admin.id}/role"),
        ("GET", "/api/management/departments"),
    ]

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"] = admin.id
            sess["role"] = "admin"
            sess["job_role"] = "admin"

        for method, path in test_matrix:
            try:
                if method == "GET":
                    resp = client.get(path)
                else:
                    payload = {"budget_id": 1, "type": "expense", "amount": 10, "description": "smoke-test"}
                    if path == "/admin/daily-balance/api/reports":
                        payload = {"report_date": "2026-05-08", "notes": "smoke"}
                    if path == "/admin/daily-balance/api/soft-balances":
                        payload = {"balance_date": "2026-05-08", "period": "AM", "notes": "smoke"}
                    if path == "/admin/expenses/api/expenses":
                        payload = {"category": "supplies", "description": "test", "amount": 10, "expense_date": "2026-05-08"}
                    if path == "/admin/inventory/api/items":
                        payload = {"ingredient_name": "chicken test", "stock_qty": 10, "low_stock_threshold": 2, "unit": "kg"}
                    if path == "/admin/menu/api/items":
                        payload = {"name": "Smoke Menu", "category": "Test", "price": 1}
                    if path == "/admin/reservations/api/reservations":
                        payload = {"customer_name": "Smoke", "customer_contact": "0912", "space_type_id": 1, "reserved_date": "2026-05-08", "reserved_time": "10:00", "duration_minutes": 60, "number_of_people": 1}
                    if path == "/admin/staff-performance/api/logs":
                        payload = {"user_id": admin.id, "shift_date": "2026-05-08", "orders_handled": 1, "avg_order_minutes": 1, "sessions_managed": 1, "upsell_count": 0, "admin_note": "smoke"}
                    if "/role" in path:
                        payload = {"role": "admin"}
                    resp = client.post(path, json=payload)
                ok = 200 <= resp.status_code < 400
                results.append(CheckResult(method, path, resp.status_code, ok))
            except Exception as exc:  # pragma: no cover - diagnostic-only path
                results.append(CheckResult(method, path, None, False, str(exc)))

    failed = [r for r in results if not r.ok]
    for r in results:
        status = r.status if r.status is not None else "ERR"
        suffix = f" ({r.error})" if r.error else ""
        print(f"[{'PASS' if r.ok else 'FAIL'}] {r.method} {r.path} -> {status}{suffix}")

    print(f"\nSummary: {len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())
