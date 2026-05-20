# Common Import Mistakes & Prevention

This guide documents common import errors and how to prevent them in production.

## Issue #1: Incorrect Model Name (FIXED ✓)

### The Problem
```python
# ❌ WRONG - This will cause ImportError
from app.models import StaffPerformance
```

### Why It Fails
- The model is named `StaffPerformanceLog`, not `StaffPerformance`
- Python cannot find `StaffPerformance` in the models
- Error: `ImportError: cannot import name 'StaffPerformance'`

### The Solution
```python
# ✓ CORRECT
from app.models import StaffPerformanceLog
```

### How to Avoid
1. **Check the __all__ list:** Look at `app/models/__init__.py` for exact names
2. **Use IDE autocomplete:** VS Code will suggest correct names
3. **Run validation script:** `python scripts/validate_imports.py`
4. **Search existing code:** Look for similar imports in codebase

## Common Model Name Mistakes

| Correct | Incorrect | Error |
|---------|-----------|-------|
| `StaffPerformanceLog` | `StaffPerformance` | ImportError |
| `InventoryItem` | `Inventory` | ImportError |
| `SoftBalanceEntry` | `SoftBalance` | ImportError |
| `OrderItem` | `OrderItems` | ImportError |
| `BoardroomBooking` | `BoardroomBook` | ImportError |

## Issue #2: Importing from Wrong Module

### The Problem
```python
# ❌ WRONG - Trying to import from specific module instead of __init__
from app.models.staff_performance import StaffPerformanceLog
```

### Why It's Bad
- Couples code tightly to module structure
- Makes refactoring harder
- Not following package conventions

### The Solution
```python
# ✓ CORRECT
from app.models import StaffPerformanceLog
```

## Issue #3: Partial Imports Not Catching Errors

### The Problem
```python
# ❌ WRONG - Won't catch import errors if typo in one of many imports
from app.models import User, Order, StaffPerformence  # typo!
```

The error might not be caught in development but fail in production.

### The Solution
```python
# ✓ CORRECT - Use explicit imports or run validation
from app.models import User, Order, StaffPerformanceLog

# ALWAYS run validation script before deploying
python scripts/validate_imports.py
```

## Issue #4: Late-Binding Imports (Anti-pattern)

### The Problem
```python
# ❌ POOR PRACTICE - Imports buried in function
def delete_user(user_id):
    from app.models import StaffPerformanceLog  # Hidden import!
    records = StaffPerformanceLog.query.filter_by(user_id=user_id).delete()
```

Problems:
- Import error only caught when function is called
- Hard to debug
- Not following Python conventions

### The Solution
```python
# ✓ CORRECT - Import at module level
from app.models import StaffPerformanceLog

def delete_user(user_id):
    records = StaffPerformanceLog.query.filter_by(user_id=user_id).delete()
```

## Issue #5: Circular Imports

### The Problem
```python
# models/user.py
from app.repositories import UserRepository  # ❌ Creates circular import

# repositories/user_repository.py
from app.models import User  # Tries to import back
```

### The Solution
```python
# models/user.py
from app.models import BaseModel  # Only import models, not repositories

# repositories/user_repository.py
from app.models import User  # Fine, no circular dependency
```

## Prevention Checklist

### Before Writing Code
- [ ] Check `app/models/__init__.py` for correct model names
- [ ] Look at similar imports in existing codebase
- [ ] Verify IDE shows autocomplete suggestions

### Before Committing Code
- [ ] Run `python scripts/validate_imports.py`
- [ ] Check for typos in import statements
- [ ] Ensure imports are at module level (not buried in functions)
- [ ] Avoid circular imports

### Before Deploying to Production
- [ ] All imports validated with script
- [ ] No late-binding imports in critical paths
- [ ] No circular import dependencies
- [ ] CI/CD validation passes

## Testing for Import Errors

### Quick Test in Python REPL
```python
# Test if import works
python -c "from app.models import StaffPerformanceLog; print('✓ Success')"

# Test app initialization
python -c "from app import create_app; app = create_app(); print('✓ Success')"
```

### Validation Script
```bash
# Run comprehensive validation
python scripts/validate_imports.py

# Look for specific import errors
grep -r "ImportError\|cannot import name" app/
```

## Debugging Import Errors in Production

If an import error occurs in production:

1. **Read the error message carefully:**
   ```
   ImportError: cannot import name 'StaffPerformance' from 'app.models'
   ```
   - "cannot import name" = name doesn't exist
   - Check: Is it spelled correctly?

2. **Check what's available:**
   ```python
   from app import models
   print(dir(models))  # Lists all available exports
   print(models.__all__)  # Lists explicit exports
   ```

3. **Look at the imports:**
   - Find the line with the error
   - Check the name against `app/models/__init__.py`
   - Look at similar imports in other files

4. **Run validation:**
   ```bash
   python scripts/validate_imports.py
   ```

## Key Takeaways

✓ **DO:**
- Import from `app.models` (not specific modules)
- Check model names in `__all__` list
- Use IDE autocomplete
- Run validation script before deploying
- Import at module level

✗ **DON'T:**
- Use incorrect model names (e.g., `StaffPerformance`)
- Bury imports in functions
- Create circular import dependencies
- Skip validation before deployment
- Import from specific model modules

## Getting Help

When you encounter an import error:

1. **Check this guide** for similar issues
2. **Run validation script:** `python scripts/validate_imports.py`
3. **Read the error message** carefully
4. **Search existing imports** for similar code
5. **Use IDE autocomplete** for correct names
6. **Ask the team** if unsure

---

**Last Updated:** 2026-05-18  
**Related:** [Import Validation Guide](IMPORT_VALIDATION_GUIDE.md)
