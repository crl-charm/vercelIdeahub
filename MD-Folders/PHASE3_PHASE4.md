# Phase 3–4 Summary

## Phase 3 — Database optimization

Indexes are created **idempotently** on app startup via [`app/db/migrator.py`](../app/db/migrator.py) `_ensure_indexes()`:

| Index | Table | Columns |
|-------|-------|---------|
| `idx_transactions_created_at` | transactions | created_at |
| `idx_transactions_payment_method` | transactions | payment_method |
| `idx_customer_sessions_time_in` | customer_sessions | time_in |
| `idx_orders_session_status` | orders | customer_session_id, status, id |
| `idx_order_items_order_id` | order_items | order_id |
| `idx_bookings_status_end` | boardroom_bookings | status, expected_end_at |

No destructive DDL. Existing data preserved.

## Phase 4 — API standardization

- **Response helpers:** [`app/dto/api_response.py`](../app/dto/api_response.py) — `api_ok()`, `api_error()`
- **Analytics naming:**
  - `AnalyticsChartService` — Chart.js `/api/analytics/daily-revenue` etc.
  - `AnalyticsReportService` — admin page `/api/analytics/summary` + PDF
- **Adopted on:** daily balance APIs, analytics chart routes, analytics controller summary
- **Chart routes** now return `{ success, data: { labels, datasets } }` (wrap only; no template used these yet)

## Smoke test

1. Restart app — watch terminal for `Created index ...` messages (first run only)
2. Daily Balance → load reports + export PDF
3. Analytics page → Update charts
4. `python scripts/validate_imports.py`
