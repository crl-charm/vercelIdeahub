#!/usr/bin/env python
"""Database migration script to add description column to menu_items"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    try:
        # Check if column exists
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('menu_items')]
        
        print(f"Current columns in menu_items: {columns}", file=sys.stderr)
        
        if 'description' not in columns:
            print("Adding description column to menu_items...")
            db.session.execute(text("ALTER TABLE menu_items ADD COLUMN description TEXT NULL"))
            db.session.commit()
            print("✓ Description column added successfully!")
        else:
            print("✓ Description column already exists!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
