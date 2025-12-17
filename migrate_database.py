#!/usr/bin/env python3
"""
Migrate existing database to add image_url column
"""
import sqlite3
import os

def migrate_database():
    """Add image_url column to existing database"""

    # Check if database exists
    if not os.path.exists('seen_items.db'):
        print("✓ No existing database - will be created by scraper with correct schema")
        return

    conn = sqlite3.connect('seen_items.db')
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seen_items'")
    if not cursor.fetchone():
        print("✓ No seen_items table yet - will be created by scraper with correct schema")
        conn.close()
        return

    # Check if image_url column exists
    cursor.execute("PRAGMA table_info(seen_items)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'image_url' not in columns:
        print("Adding image_url column to database...")
        cursor.execute('ALTER TABLE seen_items ADD COLUMN image_url TEXT DEFAULT ""')
        conn.commit()
        print("✓ Migration complete!")
    else:
        print("✓ Database already has image_url column")

    conn.close()

if __name__ == '__main__':
    migrate_database()
