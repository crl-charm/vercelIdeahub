# Production Deployment Checklist

Use this checklist before deploying any changes to production to prevent import errors and other issues.

## Pre-Deployment Validation

### Code Quality & Imports
- [ ] **Import Validation:** Run `python scripts/validate_imports.py` - should show all ✓
- [ ] **No Import Errors:** Check that no `ImportError` exceptions are present
- [ ] **Model Names:** Verify correct model names (e.g., `StaffPerformanceLog`, not `StaffPerformance`)
- [ ] **Check __all__ list:** Ensure `app/models/__init__.py` has updated __all__ list
- [ ] **Review imports:** Check all new imports use names from the __all__ list

### Dependency Management
- [ ] **Requirements updated:** `pip freeze > requirements.txt` (if any new dependencies)
- [ ] **No conflicting versions:** Check for dependency conflicts
- [ ] **Dependencies tested:** Verify all required packages are installable
- [ ] **Lock file created:** Use `pip-tools` or similar for reproducible installs

### Database
- [ ] **Migrations reviewed:** All pending migrations checked and tested
- [ ] **Backup created:** Database backed up before any schema changes
- [ ] **Foreign keys verified:** Check that cascade delete rules are correct
- [ ] **No orphaned records:** Verify no foreign key constraint violations
- [ ] **Data integrity:** Run data validation queries if applicable

### Testing
- [ ] **Unit tests pass:** `pytest tests/` (if tests exist)
- [ ] **Integration tests pass:** Test critical workflows (e.g., staff deletion)
- [ ] **Admin panel tested:** Verify staff deletion works without errors
- [ ] **Error handling tested:** Check that errors are handled gracefully
- [ ] **Database operations tested:** Verify CRUD operations work

### Security
- [ ] **No hardcoded secrets:** Check for API keys, passwords in code
- [ ] **Auth verified:** Login and permission checks work correctly
- [ ] **SQL injection prevented:** All queries use parameterized statements
- [ ] **Rate limiting configured:** Flask-Limiter properly configured
- [ ] **CORS configured:** CORS settings appropriate for production

### Environment Configuration
- [ ] **Environment variables set:** All required .env variables configured
- [ ] **Database URL correct:** Production database connection verified
- [ ] **Secret keys updated:** Flask secret keys rotated if needed
- [ ] **Debug mode disabled:** `FLASK_ENV=production`
- [ ] **Logging configured:** Proper logging levels for production

### Application Startup
- [ ] **App initializes:** `python -c "from app import create_app; create_app()"`
- [ ] **No errors on startup:** Flask app starts without any errors
- [ ] **Database connects:** Database connection successful
- [ ] **All routes registered:** All endpoints accessible
- [ ] **Static files served:** CSS, JS, images load correctly

### Deployment Infrastructure
- [ ] **Server resources:** Adequate CPU, memory, disk space
- [ ] **Port available:** Target port not in use by other services
- [ ] **Network access:** Firewall rules allow necessary connections
- [ ] **SSL/TLS configured:** HTTPS enabled if required
- [ ] **Health check endpoint:** Endpoint available to monitor app health

### Deployment Process
- [ ] **Deployment script tested:** Deployment automation verified in staging
- [ ] **Rollback plan ready:** Know how to revert to previous version
- [ ] **Downtime planned:** Minimal downtime scheduled if required
- [ ] **Team notification:** Relevant team members informed of deployment
- [ ] **Monitoring enabled:** Application monitoring and alerts active

### Post-Deployment Validation
- [ ] **App accessible:** Application loads in browser
- [ ] **Features work:** Critical features (login, deletion, etc.) function
- [ ] **No errors in logs:** Check application and server logs for errors
- [ ] **Database responsive:** Database queries execute without issues
- [ ] **Response times acceptable:** Page load times within acceptable range

### Critical Workflows to Test in Production
1. **Admin Login:** `admin` / `admin123` (then change to production credentials)
2. **Staff Deletion:** 
   - Navigate to admin panel
   - Click delete on a test staff member
   - Confirm deletion completes without errors
   - Verify staff removed from database
3. **Staff Attendance:** Record time in/out for a staff member
4. **Order Processing:** Create and handle customer orders
5. **Reports:** Generate sales reports and analytics

## Specific Safety Checks for This Release

### StaffPerformanceLog Import Fix
- [ ] `StaffPerformanceLog` is used (not `StaffPerformance`)
- [ ] `app/models/__init__.py` exports `StaffPerformanceLog`
- [ ] `app/repositories/admin_repository.py` line 7 has correct import
- [ ] `app/repositories/admin_repository.py` line 32 uses `StaffPerformanceLog`
- [ ] Staff deletion works without foreign key errors

### Foreign Key Constraints Verified
- [ ] `staff_performance_logs.user_id` cascade delete checked
- [ ] `staff_attendance.user_id` deletion handled
- [ ] `orders.handled_by` set to NULL on user deletion
- [ ] No orphaned records after deletion

## Sign-Off

| Role | Name | Date | Sign |
|------|------|------|------|
| Developer | | | |
| QA Tester | | | |
| DevOps Lead | | | |
| Product Owner | | | |

## Emergency Rollback

If issues occur:

1. **Stop current deployment:** Kill Flask process
2. **Restore previous version:** `git revert <commit-hash>`
3. **Restart application:** `python app.py`
4. **Verify rollback:** Test critical features
5. **Notify team:** Alert team of rollback

## Documentation

- [Import Validation Guide](IMPORT_VALIDATION_GUIDE.md)
- [CI/CD Workflow](.github/workflows/deployment-check.yml)
- [Staff Deletion Fix Details](../app/repositories/admin_repository.py)

---

**Last Updated:** 2026-05-18  
**For Questions:** Contact DevOps Team
