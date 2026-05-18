-- Migration: Add description field to menu_items table
ALTER TABLE menu_items ADD COLUMN description TEXT NULL;
