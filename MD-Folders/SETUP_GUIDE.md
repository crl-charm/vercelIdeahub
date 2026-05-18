# Setup Guide for New Features

## Prerequisites
- Python 3.8+
- MySQL/MariaDB
- Flask with required extensions
- Node.js (optional, for frontend tools)

---

## 1. Database Setup

### Apply Migration
The new features require one database migration. Run this SQL command:

```sql
-- Add description field to menu_items
ALTER TABLE menu_items ADD COLUMN description TEXT NULL;
```

**Location of migration file:**
```
app/migrations/add_description_to_menu.sql
```

### Execute Migration
Option A: Manual execution
```bash
mysql -u root -p ideahub_pos < app/migrations/add_description_to_menu.sql
```

Option B: Using Python migration runner
```python
# The migration system will auto-run on app startup if configured
# Check app/db/migrator.py for automatic migration execution
```

---

## 2. Directory Structure Setup

### Ensure Upload Directory Exists
```bash
# Create uploads directory for menu images
mkdir -p app/static/uploads/menu

# Set proper permissions
chmod 755 app/static/uploads/menu
```

### Required Directories
```
app/
├── static/
│   └── uploads/
│       └── menu/          # Menu item images go here
├── templates/
│   ├── menu.html          # NEW: Public menu page
│   ├── admin/
│   │   ├── menu.html      # UPDATED: Modern admin menu
│   │   └── inventory.html # UPDATED: New grid layout
```

---

## 3. Dependencies Check

### Python Packages
Ensure these are installed:
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-socketio
pip install python-socketio
pip install python-engineio
pip install werkzeug  # For file upload handling
```

### Installation
```bash
# If using requirements.txt
pip install -r requirements.txt

# If using virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Configuration Check

### Verify Configuration
File: `config.py`

Required settings:
```python
# Upload settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'app/static/uploads/menu'

# Database
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:pass@localhost/ideahub_pos"
```

---

## 5. Testing the Implementation

### Start the Application
```bash
# From project root
python app.py

# Or with Flask CLI
export FLASK_APP=app.py
flask run
```

### Access the Features

#### Admin Menu Management
```
URL: http://localhost:5000/admin/menu
- Create new menu items with images and descriptions
- Edit existing items
- Upload and manage images
- Toggle item availability
```

#### Admin Inventory Management
```
URL: http://localhost:5000/admin/inventory
- View inventory in modern grid layout
- Check low stock alerts
- Update stock levels
- View inventory change logs
```

#### Public Menu Browsing
```
URL: http://localhost:5000/menu
- Browse menu as customer
- Filter by category
- View detailed item information
- (Cart functionality ready for implementation)
```

---

## 6. Testing Inventory Deduction

### Manual Test
1. Open Admin Menu: Create a menu item named "Test Item"
2. Open Admin Inventory: Add the item with stock = 10
3. Open Orders page: Create an order with "Test Item" qty = 2
4. Go back to Inventory: Stock should be 8
5. Check notification: Should show "Low Stock" if under threshold

### WebSocket Test
1. Open inventory page in one browser tab
2. Open orders page in another tab
3. Create an order
4. Watch inventory page auto-update in real-time

---

## 7. Image Upload Testing

### Test Steps
1. Go to Admin Menu
2. Click "+ Add Menu Item"
3. Fill in name, category, price
4. Add description
5. Select an image file (drag-drop or browse)
6. See preview render
7. Click "Create Item"
8. Image should appear in menu card

### Supported Formats
- PNG (Recommended)
- JPG/JPEG
- GIF
- WebP

### Max File Size
- Default: 16MB
- Can be changed in config.py

---

## 8. Real-time Updates Testing

### SocketIO Connection Test
```javascript
// Open browser console and run:
socket.on('connect', () => {
  console.log('Connected to WebSocket');
});

socket.on('menu_item_updated', (data) => {
  console.log('Menu updated:', data);
});
```

### Event Types
- `menu_item_created` - New item created
- `menu_item_updated` - Item modified
- `menu_item_deleted` - Item deleted
- `inventory_low_stock` - Stock alert

---

## 9. Troubleshooting Common Issues

### Issue: Images Not Uploading
**Solution:**
```bash
# Check directory permissions
ls -la app/static/uploads/

# Should show: drwxr-xr-x
# If not, run:
chmod 755 app/static/uploads/menu
```

### Issue: Database Migration Fails
**Solution:**
```sql
-- Check if column already exists
DESCRIBE menu_items;

-- If description column exists, you're good
-- If not, run the migration manually
ALTER TABLE menu_items ADD COLUMN description TEXT NULL;
```

### Issue: WebSocket Not Connecting
**Solution:**
1. Check browser console for errors
2. Verify SocketIO is initialized in Flask app
3. Check firewall/proxy settings
4. Verify correct WebSocket protocol (ws://)

### Issue: Inventory Not Deducting on Order
**Solution:**
```python
# Verify inventory item exists for menu item
SELECT * FROM inventory_items WHERE menu_item_id = 1;

# If empty, create inventory item first in admin panel
# Then place order
```

---

## 10. Performance Optimization

### Image Optimization
```bash
# Consider using image compression on upload
# Install Pillow for image handling
pip install Pillow

# In menu routes, add image optimization:
from PIL import Image
```

### Database Indexes
```sql
-- Consider adding indexes for frequently queried columns
CREATE INDEX idx_menu_category ON menu_items(category);
CREATE INDEX idx_inventory_stock ON inventory_items(stock_qty);
```

### Caching
```python
# Consider caching menu items in Redis
# For frequently accessed data
pip install redis
```

---

## 11. Deployment Checklist

- [ ] Database migration applied
- [ ] Upload directory created and permissions set
- [ ] All Python dependencies installed
- [ ] Configuration updated for production
- [ ] Images optimized for web
- [ ] WebSocket configured for production server
- [ ] SocketIO working correctly
- [ ] Tested order placement with inventory deduction
- [ ] Real-time updates working
- [ ] Admin menu page loads correctly
- [ ] Public menu page accessible
- [ ] Inventory grid displays properly
- [ ] All modals functioning
- [ ] Mobile responsive design tested

---

## 12. Quick Reference Commands

### Start Development Server
```bash
python app.py
```

### Run Migrations Manually
```bash
mysql -u root -p < app/migrations/add_description_to_menu.sql
```

### Create Test Data
```python
# In Python shell
from app import create_app, db
from app.models.menu_item import MenuItem

app = create_app()
with app.app_context():
    item = MenuItem(
        name="Grilled Chicken",
        description="Perfectly grilled chicken breast",
        price=250.00,
        category="Main Dish",
        is_available=True
    )
    db.session.add(item)
    db.session.commit()
```

### Check Database Schema
```bash
mysql -u root -p -e "DESCRIBE ideahub_pos.menu_items;"
```

---

## 13. Additional Resources

### Documentation Files
- `FEATURE_IMPLEMENTATION.md` - Detailed feature documentation
- `README.md` - Project overview
- Code comments in each modified file

### Related Files
- Model: `app/models/menu_item.py`
- Service: `app/services/menu_service.py`
- Routes: `app/routes/menu.py`, `app/routes/order_routes.py`
- Templates: `app/templates/menu.html`, `app/templates/admin/menu.html`

---

## 14. Support & Next Steps

### For Issues
1. Check browser console for JavaScript errors
2. Check Flask terminal for Python errors
3. Verify database connectivity
4. Review logs in `app/routes/` files

### For Enhancement
1. Implement shopping cart
2. Add order history page
3. Create analytics dashboard
4. Implement user ratings/reviews

### Contact & Help
Refer to:
- Inline code comments
- This setup guide
- Feature implementation documentation

---

**Setup Date:** May 10, 2026
**Status:** Ready for Deployment ✅
