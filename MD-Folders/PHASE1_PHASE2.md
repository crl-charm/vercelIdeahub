# Phase 1–2 Summary (IdeaHub POS)

## Architecture map

| Layer | Location |
|-------|----------|
| Entry (dev) | `app.py` — migrator, seeder, `socketio.run` |
| Entry (Vercel) | `api/index.py` — no migrator; `NoopNotifier` |
| Factory | `app/__init__.py` |
| Routes | `app/routes/` (19 blueprints) |
| Controllers | `app/controllers/` (analytics, finance, performance, management) |
| Services | `app/services/` |
| Repositories | `app/repositories/` |
| Models | `app/models/` |
| DB patches | `app/db/migrator.py` (no Alembic) |
| Real-time | `app/core/socketio_handlers.py`, `app/core/notifiers.py` |
| Auth | `app/utils/auth.py` |

## Phase 1 changes

- **Daily balance exports** moved to `app/services/daily_balance_export_service.py`; `app/routes/sales_balance.py` is thin (~95 lines).
- **Socket.IO** domain events centralized in `socketio_handlers.py` (`emit_inventory_low_stock`, `emit_daily_sales_closed`, etc.).
- **Menu/inventory/expenses/receivables routes** already used `emit_*_update` helpers (unchanged).

## Orphan blueprints (not registered — defer to Phase 8)

| File | Prefix | Status |
|------|--------|--------|
| `app/routes/staff_menu.py` | `/menu-view` | Not in `create_app()` |
| `app/routes/staff_inventory.py` | `/inventory` | Conflicts with admin inventory prefix if registered blindly |
| `app/routes/staff_expenses.py` | `/expenses-view` | Not registered |

Templates under `app/templates/staff/` exist; wire or remove in Phase 8.

## Phase 2 changes

- **Production `SECRET_KEY`**: required when `FLASK_ENV=production` (`config/config.py`).
- **Admin API JSON auth**: `/admin/.../api/...` paths return JSON 401/403 instead of redirects (`app/utils/auth.py`).
- **CSRF exemptions documented** in `app/__init__.py`: login + `/admin/menu/api/*` only.

## Known follow-ups (Phase 3+)

- Dual analytics stacks (`analytics_service` vs `analytics_oop_service`).
- Wire `app/migrations/add_indexes.sql` into migrator.
- Register or delete `staff_*.py` blueprints.

## Smoke test checklist

1. `python app.py` starts
2. Admin login → Daily Balance → Export PDF / Excel / CSV
3. Menu CRUD + socket refresh on order page
4. Checkout Cash/GCash
