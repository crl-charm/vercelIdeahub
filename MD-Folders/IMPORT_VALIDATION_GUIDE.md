# Production Safety: Import Validation

## Issue Fixed
**Import Error:** `ImportError: cannot import name 'StaffPerformance'`
- **Cause:** Incorrect model name used in import statement
- **Correct Name:** `StaffPerformanceLog` (not `StaffPerformance`)
- **Location:** Fixed in `app/repositories/admin_repository.py` line 7

## Prevention Strategy

### 1. Explicit Exports (__all__)
All models in `app/models/__init__.py` now have an explicit `__all__` list that:
- Lists every exported model
- Prevents accidental imports of wrong names
- Makes IDE autocomplete more accurate
- Catches typos at import time

### 2. Validation Script
Created `scripts/validate_imports.py` that:
- Tests all model imports
- Tests all repository imports
- Tests all service imports
- Tests route initialization
- Can be run locally before committing
- Can be run in CI/CD before deployment

### 3. How to Use Before Deployment

**Local Testing:**
```bash
python scripts/validate_imports.py
```

**Expected Output (Success):**
```
============================================================
IMPORT VALIDATION - Pre-Production Check
============================================================
Testing model imports...
✓ All models imported successfully

Testing repository imports...
  ✓ app.repositories.admin_repository
  ✓ app.repositories.analytics_repository
  ...

Testing service imports...
  ✓ app.services.admin_service
  ...

Testing route imports...
✓ App created successfully (all routes imported)

============================================================
VALIDATION SUMMARY
============================================================
Models.................................... ✓ PASSED
Repositories............................. ✓ PASSED
Services................................ ✓ PASSED
Routes.................................. ✓ PASSED

✓ All imports validated successfully - Safe for deployment
```

### 4. Common Model Names Reference

| Correct Name | Incorrect Name (Avoid) |
|---|---|
| `StaffPerformanceLog` | `StaffPerformance` |
| `InventoryItem` | `Inventory` |
| `SoftBalanceEntry` | `SoftBalance` |
| `BoardroomBooking` | `BoardroomBook` |
| `LoungeBooking` | `LoungeBook` |

### 5. Git Pre-commit Hook (Recommended)

Create `.git/hooks/pre-commit` to automatically validate imports:

```bash
#!/bin/bash
echo "Running import validation..."
python scripts/validate_imports.py
if [ $? -ne 0 ]; then
    echo "✗ Import validation failed. Cannot commit."
    exit 1
fi
echo "✓ Imports validated. Proceeding with commit."
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### 6. CI/CD Pipeline Integration

For GitHub Actions, GitLab CI, or Jenkins, run before deploying to production:

```yaml
# Example for GitHub Actions
- name: Validate Imports
  run: python scripts/validate_imports.py
  
- name: Run Tests
  run: pytest
```

### 7. IDE Configuration (VS Code)

Add to `.vscode/settings.json`:
```json
{
  "python.linting.pylintArgs": [
    "--disable=missing-module-docstring",
    "--load-plugins=pylint.extensions.docparams"
  ],
  "python.analysis.extraPaths": ["./app"],
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

### 8. Testing Best Practices

Before production deployment:

1. ✓ Run `python scripts/validate_imports.py` locally
2. ✓ Verify all tests pass: `pytest`
3. ✓ Check linting: `pylint app/`
4. ✓ Verify app starts: `python app.py`
5. ✓ Test deletion functionality in admin panel
6. ✓ Review database migration logs

### 9. Deployment Checklist

- [ ] All imports validated with `validate_imports.py`
- [ ] No Python import errors
- [ ] Database migrations completed
- [ ] All tests passing
- [ ] App starts without errors
- [ ] Admin panel functions correctly
- [ ] Staff deletion works without errors
- [ ] No foreign key constraint violations

## Key Takeaways

**For Developers:**
- Always use the exact model name from `app.models.__all__`
- Run validation script before committing
- Check IDE autocomplete for correct names
- Review changes to `app/models/__init__.py` carefully

**For Deployment Teams:**
- Run `python scripts/validate_imports.py` before deploying
- Check CI/CD pipeline validates imports
- Monitor logs for import errors in production
- Keep this documentation updated

---

**Last Updated:** 2026-05-18  
**Fixed By:** Import validation and explicit exports  
**Status:** ✓ Production Ready
