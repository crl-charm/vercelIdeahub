# ⚡ Quick Reference: Import Safety Card

## Before Committing Code
```bash
# 1. Validate all imports
python scripts/validate_imports.py

# 2. Check for typos
grep -r "StaffPerformance[^L]" app/
```

## Before Deploying to Production
```bash
# 1. Full validation
python scripts/validate_imports.py

# 2. Start app
python app.py

# 3. Test critical features
# - Login to admin
# - Test staff deletion
# - Verify no errors in logs
```

## Model Names - Copy/Paste Reference

### Correct Names to Use:
```python
# ✓ CORRECT - Use these names
from app.models import (
    StaffPerformanceLog,        # NOT StaffPerformance
    InventoryItem,              # NOT Inventory
    SoftBalanceEntry,           # NOT SoftBalance
    BoardroomBooking,           # NOT BoardroomBook
    LoungeBooking,              # NOT LoungeBook
    OrderItem,                  # NOT OrderItems
    DailySalesReport,           # NOT DailySalesReports
    SpacePriceHistory,          # NOT SpacePriceHistories
    User, Order, SpaceType,     # Standard names
)
```

## Quick Debugging

### If you get `ImportError: cannot import name 'X'`
```python
# Step 1: Check what's available
from app.models import __all__
print(__all__)  # Shows all available exports

# Step 2: Check if it's a typo
# Common mistakes: StaffPerformance → StaffPerformanceLog

# Step 3: Use IDE autocomplete
# Type: from app.models import <press Ctrl+Space>

# Step 4: Run validation
python scripts/validate_imports.py
```

## Common Patterns

### ✓ Correct Import Pattern
```python
# At the top of the file
from app.models import StaffPerformanceLog, User, Order

# In a function
def delete_user(user_id):
    logs = StaffPerformanceLog.query.filter_by(user_id=user_id).delete()
```

### ❌ Wrong Import Patterns
```python
# DON'T: Typo in name
from app.models import StaffPerformance  # Wrong name!

# DON'T: Bury imports in function
def delete_user(user_id):
    from app.models import StaffPerformanceLog  # Bad practice

# DON'T: Import from specific module
from app.models.staff_performance import StaffPerformanceLog  # Wrong location
```

## Pre-Deployment Checklist (Short Version)

- [ ] `python scripts/validate_imports.py` - All ✓ PASSED
- [ ] App starts: `python app.py` - No errors
- [ ] Test deletion - Works without errors
- [ ] Check logs - No import errors
- [ ] Ready to deploy - All clear ✓

## Emergency: If Import Error in Production

```bash
# 1. STOP the deployment immediately

# 2. Check the error message
# Example: "cannot import name 'StaffPerformance'"
# This tells you: the name is wrong or doesn't exist

# 3. Find the bad import
grep -r "import.*StaffPerformance[^L]" app/

# 4. Fix the name
# Change to: StaffPerformanceLog

# 5. Validate
python scripts/validate_imports.py

# 6. Test
python app.py

# 7. Redeploy
```

## Key Files to Know

| File | Purpose |
|------|---------|
| `app/models/__init__.py` | List of all available models in `__all__` |
| `scripts/validate_imports.py` | Run validation before deploying |
| `MD-Folders/COMMON_IMPORT_MISTAKES.md` | Detailed error reference |
| `MD-Folders/PRODUCTION_DEPLOYMENT_CHECKLIST.md` | Full deployment guide |

## One-Liner Checks

```bash
# Check if StaffPerformanceLog can be imported
python -c "from app.models import StaffPerformanceLog; print('✓ OK')"

# Test full app initialization
python -c "from app import create_app; create_app(); print('✓ OK')"

# Find bad StaffPerformance imports
grep -r "import.*StaffPerformance[^L]" app/
```

## Remember
- **IDE autocomplete** = your friend
- **Validation script** = catch errors early
- **Read error messages** = tells you exactly what's wrong
- **Copy from __all__** = never make typos

---

**Last Updated:** 2026-05-18  
**Keep this handy!** 📋
