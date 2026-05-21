# Remove Space Reservations — Procedure

This document is the **official procedure** for removing the **Space Reservations** feature from IdeaHub. Follow it phase by phase. Do not skip validation between phases.

---

## Why remove it

IdeaHub’s real space workflow is:

| Space | How it works | Correct tool in app |
|--------|----------------|---------------------|
| **Regular Lounge** | Walk-in only | **Dashboard** → check in |
| **Premium Lounge** | Walk-in only | **Dashboard** → check in |
| **Boardroom** | Book time slot ahead | **Boardroom Booking** → book → **Start** when they arrive |

**Space Reservations** (`/admin/reservations`) is a separate admin-only list. It does **not**:

- Check customers in on the dashboard  
- Block seats or time conflicts  
- Create orders or checkout  
- Connect to boardroom booking  

It duplicates intent without operational logic. Removing it reduces staff confusion.

**Do not remove:** Dashboard check-in, **Boardroom Booking**, or `space_types` (still used for pricing, capacity, and sessions).

---

## What stays after removal

- Dashboard check-in (Regular / Premium / Boardroom walk-in path via sessions)  
- Boardroom Booking page and APIs  
- `space_types` table and admin space pricing  
- All finance, orders, inventory, receivables, etc.

---

## Phase 1 — Hide from UI (safe, reversible)

**Goal:** Staff no longer see or open Reservations. Backend can remain temporarily.

### 1.1 Remove navigation links

| File | Action |
|------|--------|
| `app/templates/layout.html` | Remove sidebar button linking to `/admin/reservations` (Management section) |
| `app/templates/partials/mobile_drawer_nav.html` | Remove drawer item for Reservations |

### 1.2 Update staff documentation

| File | Action |
|------|--------|
| `MD-Folders/STAFF_QUICK_START.md` | Remove “Reservations” from the admin-only list |

### 1.3 Validation (Phase 1)

- [ ] Log in as admin — **Reservations** not visible in sidebar or mobile menu  
- [ ] Dashboard check-in still works  
- [ ] Boardroom Booking still works  
- [ ] Direct URL `/admin/reservations` may still load (acceptable until Phase 2)

**Stop after Phase 1** if you only want to hide the feature. Continue to Phase 2 for full removal.

---

## Phase 2 — Remove application code

**Goal:** No routes, services, or templates for space reservations.

### 2.1 Unregister blueprint

**File:** `app/__init__.py`

- Remove: `from app.routes.reservations import reservations_bp`  
- Remove: `app.register_blueprint(reservations_bp)`

### 2.2 Delete feature files

Delete these files (entire files):

```
app/routes/reservations.py
app/services/reservation_service.py
app/repositories/reservation_repository.py
app/models/reservation.py
app/templates/admin/reservations.html
```

### 2.3 Clean model exports

**File:** `app/models/__init__.py`

- Remove: `from .reservation import Reservation`  
- Remove: `'Reservation'` from `__all__`

**File:** `app/models/space_type.py`

- No change required. SQLAlchemy `backref="reservations"` on `Reservation` goes away when the model is deleted.

### 2.4 Update tooling / tests

| File | Action |
|------|--------|
| `scripts/validate_imports.py` | Remove `Reservation` from model import test; remove `reservation_repository` and `reservation_service` from import checks |
| `scripts/route_smoke_test.py` | Remove routes: `GET /admin/reservations`, `GET/POST /admin/reservations/api/reservations` |

### 2.5 Do not change (false positives)

| File | Note |
|------|------|
| `app/services/booking_service.py` | Line *"Only booked reservations can be started"* refers to **boardroom bookings**, not the `Reservation` model. **Keep as-is** (optional: reword to *"Only booked boardroom slots can be started"* for clarity). |

### 2.6 Validation (Phase 2)

```bash
python scripts/validate_imports.py
python app.py
```

- [ ] App starts with no import errors  
- [ ] `/admin/reservations` returns **404**  
- [ ] Dashboard, boardroom, orders, admin panel still work  
- [ ] `python scripts/route_smoke_test.py` passes (after updating script)

---

## Phase 3 — Database (optional, production-safe)

**Goal:** Drop unused `reservations` table. Only after Phase 2 is deployed and verified.

### 3.1 Backup first

Export or backup `reservations` rows if any production data must be kept.

### 3.2 Migration SQL (MySQL)

```sql
-- Run only after code no longer references reservations
DROP TABLE IF EXISTS reservations;
```

**Do not drop** `space_types` — still required for lounge/boardroom and sessions.

### 3.3 Optional: update SQL dump

If you maintain `database/ideahub_pos (new).sql`, remove the `reservations` table definition, indexes, and FK blocks in a future dump refresh.

### 3.4 Validation (Phase 3)

- [ ] App still starts  
- [ ] No errors on dashboard or boardroom pages  
- [ ] `SHOW TABLES` no longer lists `reservations` (if dropped)

---

## File checklist (quick reference)

### Remove or edit

| Path | Phase |
|------|-------|
| `app/templates/layout.html` | 1 |
| `app/templates/partials/mobile_drawer_nav.html` | 1 |
| `MD-Folders/STAFF_QUICK_START.md` | 1 |
| `app/__init__.py` | 2 |
| `app/routes/reservations.py` | 2 (delete) |
| `app/services/reservation_service.py` | 2 (delete) |
| `app/repositories/reservation_repository.py` | 2 (delete) |
| `app/models/reservation.py` | 2 (delete) |
| `app/templates/admin/reservations.html` | 2 (delete) |
| `app/models/__init__.py` | 2 |
| `scripts/validate_imports.py` | 2 |
| `scripts/route_smoke_test.py` | 2 |
| MySQL `reservations` table | 3 (optional) |

### Keep

| Path | Reason |
|------|--------|
| `app/routes/boardroom_routes.py` | Boardroom scheduling |
| `app/services/booking_service.py` | Boardroom lifecycle |
| `app/models/boardroom_booking.py` | Boardroom data |
| `app/models/space_type.py` | Space types for all flows |
| `app/routes/session_routes.py` / dashboard | Walk-in check-in |

---

## Staff messaging (after removal)

Tell the team:

1. **Regular / Premium** — always use **Dashboard** when the customer arrives.  
2. **Boardroom** — use **Boardroom Booking** for advance slots; **Start** when they arrive.  
3. There is **no** separate “Reservations” screen anymore.

---

## Rollback

- **Phase 1:** Restore sidebar links from git history.  
- **Phase 2:** Restore deleted files and blueprint registration from git.  
- **Phase 3:** Restore table from database backup if dropped.

---

## Sign-off

| Phase | Done by | Date | Notes |
|-------|---------|------|-------|
| 1 — UI hidden | Antigravity | 2026-05-21 | UI hidden successfully (sidebar & mobile menu) |
| 2 — Code removed | Antigravity | 2026-05-21 | Routes, models, controllers, templates removed |
| 3 — DB dropped (optional) | Antigravity | 2026-05-21 | Obsolete reservations table dropped from database |

---

*Last updated: procedure aligned with IdeaHub walk-in (Regular/Premium) + boardroom booking-only model.*
