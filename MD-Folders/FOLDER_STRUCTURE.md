# 📁 Project Folder Structure - Organized

## Overview
The IdeaHub project has been reorganized for better file management and maintainability.

## Root Level
```
vercelIdeahub/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── vercel.json                     # Vercel deployment config
│
├── app/                            # Main application (core system)
│   ├── __init__.py
│   ├── controllers/                # Business logic controllers
│   ├── core/                       # Core utilities (Clock, Notifier, etc)
│   ├── db/                         # Database (migrations, seeding)
│   ├── dto/                        # Data Transfer Objects
│   ├── models/                     # Database models
│   ├── repositories/               # Data access layer
│   ├── routes/                     # API endpoints
│   ├── services/                   # Business services
│   ├── static/                     # Static files (CSS, uploads)
│   └── templates/                  # HTML templates
│
├── config/                         # 🆕 Application configuration
│   ├── __init__.py
│   └── config.py                   # Flask configuration (moved from root)
│
├── scripts/                        # 🆕 Utility & maintenance scripts
│   ├── validate_imports.py         # Import validation script
│   ├── route_smoke_test.py         # Route testing script
│   └── add_security_fields.py      # Database utility (moved from root)
│
├── database/                       # 🆕 Database files & migrations
│   ├── __init__.py
│   └── run_migration.py            # Migration script (moved from root)
│
├── tests/                          # 🆕 Test files
│   ├── __init__.py
│   └── test_db.py                  # Database tests (moved from root)
│
├── MD-Folders/                     # Documentation
│   ├── QUICK_REFERENCE.md
│   ├── IMPORT_VALIDATION_GUIDE.md
│   ├── PRODUCTION_DEPLOYMENT_CHECKLIST.md
│   ├── COMMON_IMPORT_MISTAKES.md
│   ├── PRODUCTION_SAFETY_SUMMARY.md
│   ├── IMPLEMENTATION_OVERVIEW.md
│   └── (other documentation files)
│
└── .github/
    └── workflows/
        └── deployment-check.yml    # CI/CD automation
```

## What Moved Where

### Configuration
- **Before:** `config.py` at root
- **After:** `config/config.py`
- **Why:** Better organization, grouped with other configs

### Scripts
- **Before:** `add_security_fields.py` at root
- **After:** `scripts/add_security_fields.py`
- **Why:** Separates utility scripts from core files

### Database
- **Before:** `run_migration.py` at root
- **After:** `database/run_migration.py`
- **Why:** Groups database-related tools together

### Tests
- **Before:** `test_db.py` at root
- **After:** `tests/test_db.py`
- **Why:** Standard Python testing directory convention

## Updated Imports

If you moved `config.py`, the import in `app/__init__.py` is already updated:
```python
# app/__init__.py
from config import Config
app.config.from_object(Config)
```

## How to Run Things

### Start the application
```bash
python app.py
```

### Validate imports before deployment
```bash
python scripts/validate_imports.py
```

### Run database migrations
```bash
python database/run_migration.py
```

### Run database tests
```bash
python -m pytest tests/test_db.py
# or
python tests/test_db.py
```

### Add security fields (if needed)
```bash
python scripts/add_security_fields.py
```

## Benefits of This Structure

✅ **Cleaner Root:** Only essential files at root level
✅ **Better Organization:** Related files grouped together
✅ **Scalability:** Easier to add new modules
✅ **Standard Layout:** Follows Python project conventions
✅ **Maintainability:** Clear separation of concerns
✅ **CI/CD Ready:** Scripts easily discoverable for automation

## Still at Root (Intentional)

These files remain at root as they're entry points or essential configs:
- `app.py` - Main entry point
- `requirements.txt` - Dependency list
- `vercel.json` - Deployment config
- `.github/` - CI/CD workflows
- `MD-Folders/` - Team documentation

## Legacy Files (Can Remove)

If you don't need these, they can be deleted:
- `ideahubV5/` - Old version backup
- `api/` - Old API folder (if not in use)

## File Path Quick Reference

| What | Old Path | New Path |
|------|----------|----------|
| Config file | `config.py` | `config/config.py` |
| Add security utility | `add_security_fields.py` | `scripts/add_security_fields.py` |
| Database migration | `run_migration.py` | `database/run_migration.py` |
| Database tests | `test_db.py` | `tests/test_db.py` |
| Import validation | N/A | `scripts/validate_imports.py` |

---

**Last Updated:** 2026-05-18  
**Status:** ✅ Folder structure organized and ready for production
